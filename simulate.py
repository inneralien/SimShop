#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os, os.path
from ConfigParser import SafeConfigParser
from optparse import OptionParser
import subprocess
import re

class IcarusVerilogSim():
    """
    This class is given a ConfigParser object that contains
    all of the necessary sections and items to compile a simulation.

    Icarus Verilog Compile Command:
    iverilog <warning_level> -o<output_exe> -I<include_dirs> <files>
    iverilog -Wall -o sim -I rtl/include rtl/test.v

    simulate command
    """
    def __init__(self, env):
        self.env = env
        self.warn = 'all'
        self.outfile = 'sim'
        self.rtl_files = []
        self.rtl_inc_dirs = []
        self.test_files = []
        self.test_inc_dirs = []
        self.defines = []         # -Dmacro or -Dmacor=defn
        self.include_dirs = None
        self.src = None
        self.cmd = None

        self.compile_process = None

        self.buildCmd()

    def buildCmd(self):
        default_items = [   'rtl_files',
                            'rtl_inc_dirs',
                            'test_files',
                            'test_inc_dirs',
                            'defines']

        for item in default_items:
            if(self.env.has_option('DEFAULT', item)):
                setattr(self, item, self.env.get('DEFAULT', item).split())

        proj_root = self.env.get('DEFAULT', 'PROJ_ROOT')
        rel_proj_root = os.path.normpath(self.env.path + "/" + proj_root)

        src_files = self.rtl_files + self.test_files
        inc_dirs = self.rtl_inc_dirs + self.test_inc_dirs

        self.cmd = ['iverilog',
                    '-W%s' % self.warn,
                    '-o%s' % self.outfile,
                   ] \
                    + self.prepend('-D', self.defines) \
                    + self.prepend('-I' + rel_proj_root + "/", inc_dirs) \
                    + self.prepend(rel_proj_root + "/", src_files)

    def prepend(self, flag, items):
        return ["%s%s" % (flag,b) for b in items]

#    def addFlags(self, flag, items):
#        """
#        Prepends the appropriate flag to the list of items.
#        Returns a list
#        """
#        return ["-%s%s" % (flag,b) for b in items]

    def compile(self):
        """
        Build the simulation into an executable
        """
        print "Compiling design"
        if(self.cmd is not None):
            print ' '.join("%s" % i for i in self.cmd)
            self.compile_process = subprocess.Popen(self.cmd)
            self.compile_process.communicate()
        else:
            print "No command given"

    def run(self):
        """Run the generated executable"""
        if(self.compile_process.returncode == 0):
            print "Running Simulation: %s" % self.env.target
            sim_process = subprocess.Popen(['vvp', self.outfile], 
                stdin=subprocess.PIPE)
            # To keep the simulation from running off I catch a keyboard interrupt
            # and terminate the process.
            try:
                sim_process.communicate()
            except KeyboardInterrupt:
                print "KeyboardInterrupt Caught... terminating simulation"
                sim_process.terminate()
        else:
            "Compile didn't complete so simulation can't be run"

class SimEnv(SafeConfigParser):
    """
    This class is used to maintain the simulation environment
    including paths and config files.
    """
    def __init__(self):
        SafeConfigParser.__init__(self)
        self.cfg_files = []
        self.target = None
        self.path = None
        self.test = None

    def getCfg(self, path=None):
        cfg = re.compile(".*\.cfg$")
        if(path is None):
            path = '.'
            self.cfg_files = []
        for directory, subdirs, files in os.walk(path):
            for f in files:
                found = cfg.search(f.strip())
                if(found is not None):
                    if(path is '.'):
                        self.cfg_files.append("%s%s%s" % (directory, os.sep, f))
                    else:
                        cfg_file = "%s%s%s" % (directory, os.sep, f)
                        self.read(cfg_file)

    def listTests(self):
        """
        List all available tests from the current working directory down.
        """
        self.getCfg()
        if(len(self.cfg_files) > 0):
            for config in self.cfg_files:
                self.read(config)
                if(self.has_option('DEFAULT', 'PROJ_ROOT')):
                    proj_root = self.get('DEFAULT', 'PROJ_ROOT')
                else:
                    proj_root = ''
                path = os.path.normpath(os.path.split(config)[0])
                print "- %s" % (path) #, self.cp.get('DEFAULT', 'VARIANT_NAME'))
                for section in self.sections():
                    print "    %s" % section
                print "--------------------------"
        print ""
        print "To run a simulation:"
        print "simulate <path_to/variant>.<test>"

    def verifyTarget(self, target):
        """
        Verify that the name of the target test passed on the command line
        really does exist in the config files.
        """
        print "Verifying Target: %s" % target
        self.target = target
        try:
            (self.path, self.test) = target.split('.')
        except:
            self.path = target
            self.test = ''

        if(os.path.exists(self.path)):
            self.getCfg(self.path)
            if(self.has_section(self.test)):
                print "Generating test file"
            else:
                print "Just compiling files"
        else:
            print "No valid target found"
            sys.exit(1)

#    sys.exit()

if __name__ == '__main__':
    copyright_text = \
"""\
=================================================
 RTLCores Simulation Script - Copyright (C) 2010
=================================================
"""
    print copyright_text
    parser = OptionParser(usage="%prog <options> <testname>", 
        version="%prog v0.1")
    parser.add_option("-l", "--list_tests",
                        action="store_true",
                        dest="list_tests",
                        help="list all available tests")
    parser.add_option("-c", "--compile_only",
                        action="store_true",
                        dest="compile_only",
                        help="compile the simulation but don't run it")

    (options, args) = parser.parse_args()

    env = SimEnv()
    if(options.list_tests):
        env.listTests()
        sys.exit()

    if(len(args) > 0):
        target = args[0]
        env.verifyTarget(target)
        sim = IcarusVerilogSim(env)
        sim.compile()
        sim.run()

#        print env.cfg_files
#        vs = IcarusVerilogSim()
#        vs.run(target)
    else:
        parser.print_help()

