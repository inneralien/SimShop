#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from optparse import OptionParser
import re
import string
import distutils.dir_util

from builders.IcarusVerilog import IcarusVerilog
import SimRun
import SimCfg
import TestFind

__author__ = "Tim Weaver - RTLCores"
__version__ = "v0.6.2 alpha"


if __name__ == '__main__':
    copyright_text = \
"""\

  RTLCores Simulation Script
  Copyright (C) 2010-2011
  %s
""" % __version__
    print copyright_text
    parser = OptionParser(usage="%prog [options] [testname]",
        version="%s" % (__version__))
    parser.add_option("-l", "--list-tests",
                        action="store_true",
                        dest="list_tests",
                        help="list all available tests")
    parser.add_option("-t", "--tabulate",
                        action="store_true",
                        dest="tabulate",
                        help="tabulate errors and warning from the simulations")
    parser.add_option("-n", "--dry-run",
                        action="store_true",
                        dest="dry_run",
                        help="print out the commands that would be executed, but do not execute them")
    parser.add_option("-c", "--compile-only",
                        action="store_true",
                        dest="compile_only",
                        help="compile the simulation but don't run it")
    parser.add_option("-d", "--dumpon",
                        action='store_true',
                        dest="dumpon",
                        help="enable dumping of waveform")
#    parser.add_option("-o", "--output_dir",
#                        dest="output_dir",
#                        help="output build directory")
    parser.add_option("-D", "--defines",
                        action='append',
                        dest="defines",
                        help="pass in extra defines")
    parser.add_option("-p", "--plusarg",
                        action='append',
                        dest="plusargs",
                        default=[],
                        help="""Pass plusargs to the simulation.
                        sim -pDUMPON <testname>""")
    parser.add_option("--clean",
                        action="store_true",
                        dest="clean",
                        help="clean the simbuild directory")

    # List available tools, i.e. iverilog, vcs, modelsim
    # List available builders, i.e. IcarusVerilog

    (options, args) = parser.parse_args()

    sim_cfg = SimCfg.SimCfg()
## TODO Search for default config files in the usuall places.  The
## variant config file can overwrite any value set by a system wide
## or user home config file
##   System Wide Unix: /etc/rtlcores/xxx.cfg?
##   System Wide Windows: c:/rtlcores/xxx.cfg?
##   Users Home: ~/rtlcores/xxx.cfg

    if(options.list_tests):
        t = TestFind.TestFind()
        if(len(args) > 0):
            t.buildTestStruct(args[0])
        else:
            t.buildTestStruct()
        sys.exit()

    defines = ""
    plusargs = ""
    if(options.defines):
        print "DEFINES:", options.defines
        defines = " ".join("%s" % x for x in options.defines)

    if(options.dumpon):
        options.plusargs.append('DUMPON')

    if(options.plusargs):
        print "PLUSARGS:", options.plusargs
        plusargs += " ".join("%s" % x for x in options.plusargs)

    if(len(args) > 0):
        for target in args:
            try:
                sim_cfg.verifyTarget(target)
            except SimCfg.MultipleConfigFiles, info:
                print "==== Error ===="
                print "Either there are multiple .cfg files in the current directory"
                print "or you need to give a path to the variant on which you want to"
                print "run a test."
                print ""
                print "I found the following config files:"
                for i in info.data:
                    print "  %s" % i
                sys.exit(1)
            except SimCfg.InvalidTest, info:
                print "The test '%s' does not exist. Check your spelling." % info.data
                sys.exit(1)
            except SimCfg.InvalidPath, info:
                print "The path '%s' does not exist." % info.data
                sys.exit(1)

            sim_cfg.genAutoTest(options.dry_run, True)
            sim_cfg['defines'] += " " + defines
            sim_cfg['plusargs'] += " " + plusargs
#            sim_cfg['outfile'] = sim_cfg.build_path + '/' + 'sim_' + sim_cfg.variant
#            sim_cfg['outfile'] = sim_cfg.build_path + '/' + 'sim_' + sim_cfg.test
            sim_cfg['outfile'] = sim_cfg.build_path + '/' + 'sim'

            sim = IcarusVerilog(sim_cfg)
            sim.buildCompCmd()
            sim.buildSimCmd()
            if(options.dry_run):
                for cmd in sim.cmds:
                    print " ".join(cmd)
                sys.exit(0)
            if(not options.compile_only):
                try:
                    sim.run(store_stdio=options.tabulate)
                except SimRun.ProcessFail, info:
                    print "The process exited with an error"
            else:
                print "--Compile only--"
                sim.run(0)
    else:
        parser.print_help()
