#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from optparse import OptionParser
import re
import string
import distutils.dir_util
#from distutils import dep_util

from builders.IcarusVerilog import IcarusVerilog
import SimRun
import SimCfg
import DefCfg
import TestFind



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
    parser.add_option("-l", "--list_tests",
                        action="store_true",
                        dest="list_tests",
                        help="list all available tests")
    parser.add_option("-D", "--defines",
                        action='append',
                        dest="defines",
                        help="pass in extra defines")
    parser.add_option("-d", "--dumpon",
                        action='store_true',
                        dest="dumpon",
                        help="enable dumping of waveform")
#    parser.add_option("-o", "--output_dir",
#                        dest="output_dir",
#                        help="output build directory")
    parser.add_option("-c", "--compile_only",
                        action="store_true",
                        dest="compile_only",
                        help="compile the simulation but don't run it")

    # List available tools, i.e. iverilog, vcs, modelsim
    # List available builders, i.e. IcarusVerilog

    (options, args) = parser.parse_args()

#    auto_test_template_file = 'test_template.py'

    sim_cfg = SimCfg.SimCfg()
## Search for default config files in the usuall places.  The
## variant config file can overwrite any value set by a system wide
## or user home config file
##   System Wide Unix: /etc/rtlcores/xxx.cfg?
##   System Wide Windows: c:/rtlcores/xxx.cfg?
##   Users Home: ~/rtlcores/xxx.cfg

    if(options.list_tests):
        t = TestFind.TestFind()
        t.listTests()
        sys.exit()

    if(options.defines):
        print options.defines

    if(len(args) > 0):
        target = args[0]
        sim_cfg.verifyTarget(target)
        sim_cfg.genAutoTest()
        sim_cfg['outfile'] = sim_cfg.auto_test_path + '/' + 'sim_' + sim_cfg.variant

        sim = IcarusVerilog(sim_cfg)
        sim.buildCompCmd()
        sim.buildSimCmd()
        sim.joinCmds()
        print sim.comp_cmd
        if(not options.compile_only):
            sim.run()
    else:
#        print " Available Tests"
#        print "-----------------"
#        sim_cfg.listTests()
        parser.print_help()
