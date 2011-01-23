#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (C) 2010-2011 RTLCores LLC.
# http://rtlcores.com

import sys,os
from optparse import OptionParser
import re
import string
import distutils.dir_util

from builders.IcarusVerilog import IcarusVerilog
import ScoreBoard
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
    parser = OptionParser(usage="%prog [options] [path_to/variant/<testname>]",
        version="%s" % (__version__))
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
    parser.add_option("-d", "--dumpon",
                        action='store_true',
                        dest="dumpon",
                        help="enable dumping of waveform. This is the same as -DDUMPON")
#    parser.add_option("-m", "--match",
#                        action='append',
#                        dest="match",
#                        default=[],
#                        metavar='NAME',
#                        help="run all tests that match the NAME")
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

## TODO Search for default config files in the usual places.  The
## variant config file can overwrite any value set by a system wide
## or user home config file
##   System Wide Unix: /etc/rtlcores/xxx.cfg?
##   System Wide Windows: c:/rtlcores/xxx.cfg?
##   Users Home: ~/rtlcores/xxx.cfg

    if(options.list_tests):
        t = TestFind.TestFind()
        try:
            if(len(args) > 0):
                t.buildTestStruct(args[0])
                t.listTests()
            else:
                t.buildTestStruct()
                t.listTests()
        except TestFind.TestFindError, info:
            print info.error_message
        sys.exit(1)

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
        score_board = ScoreBoard.ScoreBoard()
        score_board.addErrorRegex(re.compile(r'ERROR:'))
        score_board.addWarningRegex(re.compile(r'WARNING:'))
        score_board.setTestBeginRegex(re.compile(r'TEST_BEGIN'))
        score_board.setTestEndRegex(re.compile(r'TEST_END'))

        cfg_list = []
        try:
            for target in args:
                try:
                        # Make a new sim_cfg for each new target
                        # We don't want stale variables from previous runs
                    sim_cfg = SimCfg.SimCfg()
                    cfg_list.append(sim_cfg)
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
                except Exception:
                    print "** Error **"
                    print "Unexpected exception raised:"
                    exctype, value = sys.exc_info()[:2]
                    print exctype
                    print value
                    raise

                sim_cfg.genAutoTest(options.dry_run, True)
                sim_cfg['defines'] += " " + defines
                sim_cfg['plusargs'] += " " + plusargs
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
                        sim.run()
                    except SimRun.ProcessFail, info:
                        print "The process exited with an error"
                else:
                    print "--Compile only--"
                    sim.run(0)
                    print sim.cfg['logfile']
                    print sim.cfg.variant
                    print sim.cfg.test
                    print sim.cfg.path
                    print sim.cfg.build_path
                    print sim.cfg.tasks
        except KeyboardInterrupt:
            print "KeyboardInterrupt Caught... terminating simulation"
        except SystemExit:
            pass
        finally:
            print ""
            print "========================="
            print " Collecting Test Results "
            print "========================="
            for cfg in cfg_list:
                score_board.scoreTestFromCfg(cfg)
            score_board.printASCIIReport()
            os._exit(1)
    else:
        parser.print_help()
