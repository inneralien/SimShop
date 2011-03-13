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
__version__ = "v0.7 Beta"


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

    defines = ""
    plusargs = ""
    if(options.defines):
#        print "DEFINES:", options.defines
        defines = " ".join("%s" % x for x in options.defines)

    if(options.dumpon):
        options.plusargs.append('DUMPON')

    if(options.plusargs):
#        print "PLUSARGS:", options.plusargs
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
#                    except:
#                        pass
#                except:
#                    pass
                finally:
                    score_board.addVariant(sim_cfg.variant)

            for sim_cfg in cfg_list:
#                print sim_cfg
                try:
#                    print "Adding variant: %s" % sim_cfg.variant
#                    score_board.addVariant(sim_cfg.variant)

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
                                pass
                        else:
                            print "--Compile only--"
                            sim.run(0)

                except:
                    raise

        except KeyboardInterrupt:
            print "KeyboardInterrupt Caught... terminating simulation"
        except SystemExit:
            pass
        except Exception:
            tb = sys.exc_info()[2]
            stack = []
            while tb:
                stack.append(tb.tb_frame)
                tb = tb.tb_next
#TODO - Add a logger and push this traceback to a file
            traceback.print_exc()
        finally:
            if(options.compile_only or options.dry_run):
                pass
            else:
                print ""
                for cfg in cfg_list:
                    try:
                        score_board.scoreTestFromCfg(cfg)
                    except Exceptions.LogFileDoesNotExistError, info:
                        print info.error_message
                        if(options.verbose):
                            print info.long_message
                        else:
                            print "(use -v option to print verbose error messages)"
#                    except:
#                        pass
#                        raise

                # Determine longest string for pretty printing the results
                longest = 0
#                for variant in score_board.variant_list:
#                    score = score_board.scores[variant]
                longest_str = score_board.longestString()
#                print longest_str
#                    if(longest_str > longest):
#                        longest = longest_str

                # Pretty print the test results
#                print "TEST SUMMARY"
#                print "-" * (79)
                print ""
                error_count = 0
                warning_count = 0
                incomplete_count = 0
#                for variant in score_board.variant_list:
#                    score = score_board.scores[variant]
                error_count = score_board['error_count']
                warning_count = score_board['warning_count']
                incomplete_count = score_board['incomplete_count']
                total_nodes = score_board['total_nodes']
                score_board.printTree(max_level=score_board.max_level, pad=longest_str+4)
#                print total_nodes, error_count, warning_count, incomplete_count
#                print "Incomplete count: ", score_board['incomplete_count']
#                print "Invalid count:    ", score_board['invalid_count']
#                print "Error count:      ", score_board['error_count']
#                print "Warning count:    ", score_board['warning_count']

                print ""

                variants_failed = 0.
                tests_failed = 0.
                tasks_failed = 0.
                for v in score_board['kids']:
                    if(not v['pass']):
                        variants_failed += 1
                    for t in v['kids']:
                        if(not t['pass']):
                            tests_failed += 1
                        for task in t['kids']:
                            if(not task['pass']):
                                tasks_failed += 1

                total_scores = 0.
                total_failures = 0.
                total_passed = 0.
                for v in score_board['kids']:
                    # if(no kids and didn't pass): increment failures count
                    if(len(v['kids']) == 0):
                        total_scores += 1
                        if(not v['pass']):
                            total_failures += 1
                        else:
                            total_passed += 1
                    for t in v['kids']:
                        if(len(t['kids']) == 0):
                            total_scores += 1
                            if(not t['pass']):
                                total_failures += 1
                            else:
                                total_passed += 1
                        for task in t['kids']:
                            if(len(task['kids']) == 0):
                                total_scores += 1
                                if(not task['pass']):
                                    total_failures += 1
                                else:
                                    total_passed += 1


                tests_passed = score_board.test_count - tests_failed
                tasks_passed = score_board.task_count - tasks_failed
                if(score_board.test_count != 0):
                    tests_percent_passed = float(tests_passed)/float(score_board.test_count)*100.
                else:
                    tests_percent_passed = 0
                tests_percent_failed = 100. - tests_percent_passed

                if(score_board.task_count != 0):
                    tasks_percent_passed = float(tasks_passed)/float(score_board.task_count)*100.
                else:
                    tasks_percent_passed = 0
                tasks_percent_failed = 100. - tasks_percent_passed

#                print "Total Scores  : %d" % total_scores
                print "Passed      %d/%d (%.1f%%)" % (total_passed, total_scores, (total_passed/total_scores)*100.)
                print "Failed      %d/%d (%.1f%%)" % (total_failures, total_scores, (total_failures/total_scores)*100.)
                print "Invalid     %d" % (score_board['invalid_count'])
                print "Incomplete  %d" % (score_board['incomplete_count'])
                print "Errors      %d" % (score_board['error_count'])
                print "Warnings    %d" % (score_board['warning_count'])
#                print ""
#                print "Tests: Failed/Total: %d/%d (%d%%)" % (tests_failed, score_board.test_count, tests_percent_passed)
#                print "Tasks: Failed/Total: %d/%d (%d%%)" % (tasks_failed, score_board.task_count, tasks_percent_passed)
#                print ""
#                print "Tally:"
##                print "%d tasks in %d tests" % (score_board.task_count, score_board.test_count)
#                if(score_board.test_count == 1):
#                    print "%d test with %d recorded tasks" % (score_board.test_count,score_board.task_count)
#                else:
#                    print "%d tests with %d recorded tasks" % (score_board.test_count,score_board.task_count)
##                print "Tasks          : %d" % (score_board.task_count)
##                print "Tests          : %d" % (score_board.test_count)
#                print "Passed         : %d (%.1f%%)" % (tests_passed, tests_percent_passed)
#                print "Failed         : %d (%.1f%%)" % (tests_failed, tests_percent_failed)
#                print "    Invalid    : %d (%.1f%%)" % (score_board['invalid_count'], 0)
#                print "    Incomplete : %d (%.1f%%)" % (score_board['incomplete_count'], 0)
#                print ""
#                print "Total Errors   : %d" % (score_board['error_count'])
#                print "Total Warnings : %d" % (score_board['warning_count'])
#
#                print "--"
#                print "Tests Passed  : %d/%d (%d%%)" % (tests_passed, score_board.test_count, tests_percent_passed)
#                print "Tests Failed  : %d/%d (%d%%)" % (tests_failed, score_board.test_count, tests_percent_failed)
#                print ""
#                print "Tasks Passed  : %d/%d (%d%%)" % (tasks_passed, score_board.task_count, tasks_percent_passed)
#                print "Tasks Failed  : %d/%d (%d%%)" % (tasks_failed, score_board.task_count, tasks_percent_failed)
#                print ""
#                print "Invalid    : %d (%.1f%%)" % (score_board['invalid_count'], 0)
#                print "Incomplete : %d (%.1f%%)" % (score_board['incomplete_count'], 0)
#                print ""

            os._exit(1)
    else:
        parser.print_help()
