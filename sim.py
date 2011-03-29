#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import sys,os
from optparse import OptionParser
import re
import traceback

import Exceptions
import builders.Exceptions
from builders.IcarusVerilog import IcarusVerilog

import ScoreBoard
import SimCfg
import TestFind

__author__ = "Tim Weaver - RTLCores"
__version__ = "v0.9"

# Features to add
#
#   Email HTML results.
#       --email
#       --from=me@gmail.com
#       --to=you@gmail.com
#       --email-cfg email.cfg
#           username=
#           password=
#           css_template=
#           email_template= (HTML)
#


if __name__ == '__main__':
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
                        help="enable dumping of waveform. This is the same as -pDUMPON")
    parser.add_option("-v", "--verbose",
                        action='store_true',
                        dest="verbose",
                        help="display verbose error messages")
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
    parser.add_option("-o", "--output-file",
                        dest="output_file",
                        metavar='FILE',
                        help="""store the scoreboard report to pickle FILE""")
#    parser.add_option("--clean",
#                        action="store_true",
#                        dest="clean",
#                        help="clean the simbuild directory")

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
        except Exceptions.TestFindError, info:
            print info.error_message
            sys.exit(1)
        sys.exit(0)

    defines = ""
    plusargs = ""
    if(options.defines):
        defines = " ".join("%s" % x for x in options.defines)

    if(options.dumpon):
        options.plusargs.append('DUMPON')

    if(options.plusargs):
        plusargs += " ".join("%s" % x for x in options.plusargs)

    if(len(args) > 0):
        score_board = ScoreBoard.ScoreBoard('Simulation Score')
        score_board.addErrorRegex(re.compile(r'ERROR:'))
        score_board.addWarningRegex(re.compile(r'WARNING:'))
        score_board.setTestBeginRegex(re.compile(r'TEST_BEGIN'))
        score_board.setTestEndRegex(re.compile(r'TEST_END'))

        cfg_list = []
        try:
            for target in args:
                # Make a new sim_cfg for each new target
                # We don't want stale variables from previous runs
                sim_cfg = SimCfg.SimCfg()
                cfg_list.append(sim_cfg)
                try:
                    sim_cfg.verifyTarget(target)
                except Exceptions.InvalidTest, info:
                    print "The test '%s' does not exist. Check your spelling." % info.error_message
                except Exceptions.InvalidPath, info:
                    print "The path '%s' does not exist." % info.error_message
                except Exceptions.MultipleConfigFiles, info:
                    print "Multiple Config Files"
                    print "I found the following config files"
                    for i in info.error_message:
                        print " %s" % i
                finally:
                    score_board.addVariant(sim_cfg.variant)

            for sim_cfg in cfg_list:
                try:
                    if(not sim_cfg.invalid):
                        sim_cfg.genAutoTest(options.dry_run, True)
                        sim_cfg['defines'] += " " + defines
                        sim_cfg['plusargs'] += " " + plusargs

                        sim = IcarusVerilog(sim_cfg)

                        sim.buildCompCmd()
                        sim.buildSimCmd()
                        if(options.dry_run):
                            for cmd in sim.cmds:
                                print " ".join(cmd)
                            break
                        if(not options.compile_only):
                            try:
                                stdio = sim.run()
                            except builders.Exceptions.ProcessFail, info:
                                sim_cfg.not_run = True
                                sim_cfg.error_message = info.error_message
                        else:
                            print "--Compile only--"
                            sim.run(0)

                except:
                    raise

        except KeyboardInterrupt:
            print "KeyboardInterrupt Caught... terminating simulation"
            sys.exit(1)
        except SystemExit:
            sys.exit(1)
        except Exception:
            tb = sys.exc_info()[2]
            stack = []
            while tb:
                stack.append(tb.tb_frame)
                tb = tb.tb_next
            sys.exit(1)
#TODO - Add a logger and push this traceback to a file
            traceback.print_exc()
        finally:
            if(options.compile_only or options.dry_run):
                pass
            else:
                print ""
                for cfg in cfg_list:
                    try:
                        if(cfg.not_run is True):
                            score_board.scores[cfg.variant].incNotRun(cfg.error_message)
                        else:
                            score_board.scoreTestFromCfg(cfg)
                    except Exceptions.LogFileDoesNotExistError, info:
                        print info.error_message
                        if(options.verbose):
                            print info.long_message
                        else:
                            print "(use -v option to print verbose error messages)"

                # Determine longest string for pretty printing the results
                longest = 0
                longest_str = score_board.longestString()

                # Pretty print the test results
                print ""
                error_count = 0
                warning_count = 0
                incomplete_count = 0
                error_count = score_board['error_count']
                warning_count = score_board['warning_count']
                incomplete_count = score_board['incomplete_count']
                total_nodes = score_board['total_nodes']
                tree = score_board.asciiTree(max_level=score_board.max_level, pad=longest_str+4, print_html=False)
                tally = score_board.asciiTally()

                if(options.output_file is not None):
                    score_board.writePickleFile(options.output_file)
                sys.stdout.write(tree)
                sys.stdout.write("\n")
                sys.stdout.write(tally)


    else:
        parser.print_help()
