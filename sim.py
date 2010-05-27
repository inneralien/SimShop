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
__version__ = "v0.1"


if __name__ == '__main__':
    copyright_text = \
"""\
=========================================================
 RTLCores Simulation Script (alpha) - Copyright (C) 2010
=========================================================
"""
    print copyright_text
    parser = OptionParser(usage="%prog <options> <testname>", 
        version="%prog alpha v0.1")
    parser.add_option("-l", "--list-tests",
                        action="store_true",
                        dest="list_tests",
                        help="list all available tests")
    parser.add_option("-n", "--dry-run",
                        action="store_true",
                        dest="dry_run",
                        help="print out the commands that would be executed, but do not execute them")
    parser.add_option("-c", "--compile-only",
                        action="store_true",
                        dest="compile_only",
                        help="compile the simulation but don't run it")
#    parser.add_option("-d", "--dumpon",
#                        action='store_true',
#                        dest="dumpon",
#                        help="enable dumping of waveform")
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
                        help="plusargs")

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
        t.listTests()
        sys.exit()

    defines = ""
    plusargs = ""
    if(options.defines):
        print "DEFINES:", options.defines
        defines = " ".join("%s" % x for x in options.defines)

    if(options.plusargs):
        print "PLUSARGS:", options.plusargs
        plusargs = " ".join("%s" % x for x in options.plusargs)
        print plusargs

    if(len(args) > 0):
#        target = args[0]
        for target in args:
            sim_cfg.verifyTarget(target)
            sim_cfg.genAutoTest()
            sim_cfg['defines'] += " " + defines
            sim_cfg['plusargs'] += " " + plusargs
            sim_cfg['outfile'] = sim_cfg.build_path + '/' + 'sim_' + sim_cfg.variant
#            sim_cfg['outfile'] = sim_cfg.build_path + '/' + 'sim_' + sim_cfg.test

            sim = IcarusVerilog(sim_cfg)
            sim.buildCompCmd()
            sim.buildSimCmd()
            if(options.dry_run):
                for cmd in sim.cmds:
                    print ">",
                    print " ".join(cmd)
                sys.exit(0)
            if(not options.compile_only):
                print "IN compile_only"
                sim.run()
            else:
                sim.run(0)
    else:
        parser.print_help()
