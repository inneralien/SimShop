#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from optparse import OptionParser
import re
#from distutils import dep_util
from test_template import test_template

from builders.IcarusVerilog import IcarusVerilog
import SimRun
import SimCfg

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

    cfg = SimCfg.SimCfg()
    if(options.list_tests):
        cfg.listTests()
        sys.exit()

    if(len(args) > 0):
        target = args[0]
        cfg.verifyTarget(target)
        sim = IcarusVerilog(cfg)
        sim.run()
    else:
        parser.print_help()

