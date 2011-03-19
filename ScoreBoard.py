#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import os
import re
import Exceptions
import help
from Score import Score

class ScoreBoard(Score):
    """
    The ScoreBoard class is used to tally test results and generate reports
    of various formats.
    """
    def __init__(self, name='Top'):
        Score.__init__(self, name=name)
        self.scores = {}
        self.variant_list = []
        self.errorRegex = []
        self.warningRegex = []
        self.testBeginRegex = None  # There can be only 1
        self.testEndRegex = None    # There can be only 1
        self.errors = []
        self.warnings = []
        self.error_re = re.compile(r'ERROR')

        self.level = 0
        self.longest_string = 0
        self.max_level = None
        self.test_count = 0
        self.task_count = 0

    def addVariant(self, variant):
        if(variant not in self.variant_list):
            self.variant_list.append(variant)
            self.scores[variant] = self.add(name=variant)

    def addTest(self, test, variant):
        self.test_count += 1
        return self.scores[variant].add(name=test)

    def addTask(self, task, test):
        self.task_count += 1
        return test.add(name=task)

    def setTestBeginRegex(self, regex):
        self.testBeginRegex = regex

    def setTestEndRegex(self, regex):
        self.testEndRegex = regex

    def addWarningRegex(self, regex):
        self.warningRegex.append(regex)

    def addErrorRegex(self, regex):
        self.errorRegex.append(regex)

    def scoreTestFromCfg(self, sim_cfg):
        variant = sim_cfg.variant
        test = sim_cfg.test_section

            # Add a test to the variant
        if(len(self.scores) != 0):
            if(variant in self.scores):
                test_score = self.addTest(test, variant)
            else:
                self.incNotRun()

            # A log file contains 1 variant, 1 test and 0 or more tasks
            # If the sim_cfg is marked as invalid then the test should be
            # scored as such and there's no need to parse the log file
            if(not sim_cfg.invalid):
                self.searchFile(sim_cfg, test_score)
            else:
                test_score.incInvalid()

    def searchFile(self, sim_cfg, test_score):
        """
        Parses a simulation log file who's path is provided by the
        sim_cfg and searches for various expressions.
            - Task names that match the known tasks for a particular test
            - Any number of error expressions set by addErrorRegex
            - Any number of warning expressions set by addWarningRegex
            - Begin and End expressions for test completion checking

        @type   sim_cfg: SimCfg
        @param  sim_cfg: A simulation configuration
        @type   test_score: Score
        @param  test_score: A Score object
        """
        logfile = ''
        prev_score = None
        score = test_score
        try:
            logfile = sim_cfg.build_path + "/" + sim_cfg['logfile']
        except:
            pass
        got_test_begin = False
        task_list = []

        if(not os.path.exists(logfile)):
            score.incNotRun()
            raise Exceptions.LogFileDoesNotExistError('searchFile',
                'The file to be scored does not exist: %s' % logfile,
                help.missing_logfile_help)
        f = open(logfile, 'r')
        for i in f.readlines():
                # Search for know Task names
            for task in sim_cfg.task_list:
                if(True):
                    # Strip off any parenthesis from tasks that have arguments
                    task = re.sub(r'\(.*', '', task)
                    r = re.compile(r'%s' % task)
                    s = r.search(i)
                    if(s is not None):
                        task_name = s.group()
                        task_list.append(task_name)
                        test = self.addTask(task_name, test_score)
                            # score is the current child in the Score hierarchy
                        score = test
                        break

                # Search for Error expressions
            for regex in self.errorRegex:
                s = regex.search(i)
                if(s is not None):
                    score.incError()

                # Search for Warning expressions
            for regex in self.warningRegex:
                s = regex.search(i)
                if(s is not None):
                    score.incWarning()

                # Search for test begin expression
            if(self.testBeginRegex is not None):
                s = self.testBeginRegex.search(i)
                if(s is not None):
                    if(got_test_begin is True):
                        prev_score.incIncomplete()
                    else:
                        got_test_begin = True

                # Search for test end expression
            if(self.testEndRegex is not None):
                s = self.testEndRegex.search(i)
                if(s is not None):
                    if(got_test_begin is False):
                        score.incIncomplete()
                    else:
                        got_test_begin = False

            prev_score = score

            # If the simulation is canceled then it should be reported
            # as an incomplete. Right?
        if(got_test_begin is True):
            score.incIncomplete()

    def printHTMLReport(self):
        """
        Prints an HTML table representation of the simulation result.
        """
        print "<table>"
        print "<tr>"
        print "<td>Variant</td>"
        print "<td>Test</td>"
        print "<td>Task</td>"
        print "<td>ERRORS</td>"
        print "<td>WARNINGS</td>"
        print "<td>INCOMPLETES</td>"

        print "</tr>"
        print "</table>"

        for v in self.variant_list:
            print self.scores[v].name, self.scores[v].error_count
            for test in self.scores[v].children:
                print "  ", test.name, test.error_count, test.incomplete_count
                for task in test.children:
                    print "    ", task.name, task.error_count, task.incomplete_count

    def getLongestString(self, data=None, last=False, max_level=None):
        if(max_level is not None):
            self.max_level = max_level
        elif(self.level > self.max_level):
            self.max_level = self.level

        if(len(data['name']) > self.longest_string):
            self.longest_string = len(data['name'])

        for i in range(len(data['kids'])):
            last = (i == len(data['kids']) - 1)
            self.level += 1
            self.getLongestString(data['kids'][i], last, max_level=max_level)
            self.level -= 1

    def traverse(self, data):
        # Recurse through the children
        for i in range(len(data['kids'])):
            last = (i == len(data['kids']) - 1)
            self.level += 1
            self.traverse(data['kids'][i], last)
            self.level -= 1


if __name__ == '__main__':
    sb = ScoreBoard('Simulation')
    sb.incError()
    a = sb.add('Deserializer')

#    a = Score('Deserializer')
    r = a.add('regression')
    r.add('task0')
    r.add('task1')
    t = r.add('task2')
    t.incError()
    r.add('task3')
#    test = r.add('start_error')
#    test = r.add('start_error')
#    test = r.add('start_error')
    r.incIncomplete()
#    task = test.add('test_start_error')
#    test = r.add('stop_error')
#    task = test.add('test_stop_error')
#    test = r.add('bobs_error')

    a = sb.add('Serializer')
    r = a.add('regression')
#    errors.increment()
#    errors.increment()
#    warnings = a.add('warnings')
#    warnings.increment()
#    print errors['score']
#    print warnings['score']
    # Determine longest string for pretty printing the results

    longest = 0
#    for variant in sb.variant_list:
#        score = sb.scores[variant]
#        longest_str = score.longestString(score)
#        if(longest_str > longest):
#            longest = longest_str

    print longest
    sb.printTree(max_level=sb.max_level, pad=40)

#    d = c.add('test0')
#    d.add('task0')
#    e = d.add('task1')
#    e.increment()
#    d = c.add('test1')
##    d.increment()
#    e = d.add('task0')
#    e.increment()
#    e = d.add('task1')
#    e.increment()
#    e.increment()
#    d = c.add('test2')
#    d.add('task0')
#    d.add('task1')
#    sa = a.add('simulate')
#    sb = sa.add('test0')
#    sc = sb.add('task0')
#    sc = sb.add('task1')
#    sc.increment()
#    sa.add('test1')
#    t = sa.add('test2')
#    t.increment()
#
#    sa.traverse()
#    sa = a.add('sub')
#    sa = a.add('sub')
#    sb = sa.add('sub_sub')
#    sb = sa.add('sub_sub')
#    sb.add('sub_sub_sub')
#    sb.add('sub_sub_sub')
#    sb = sa.add('sub_sub')
#    a.add('sub')

#    traverse.lasts = []
#    traverse.level = 0
#    traverse(a)
#    a.traverse(max_level=2)
#    a.traverse()

#    targets = ['test0', 'test1', 'test2']
#    for target in targets:
#        print "Compiling %s" % target
#        print "Simulating %s" % target
#        compile_score       = Score(name = target)
#        sim_error_score     = Score(name = target)
#        task_score          = sim_error_score.add('task0')

#    variants = {}
#    variants['v0'] = Score(name='v0')
#
#    # Add a new test to the variant
#    test = variants['v0'].add('test0')
#
#    # Add a new task to the test
#    task = test.add('task0')
#    task.incError()
#    # Add another new task to the test
#    task = test.add('task1')
#    task.incError()
#
#    # Add a new test to the variant
#    test = variants['v0'].add('test1')
#    # Add a new task to the test
#    task = test.add('taskA')
#    task.incError()
#    # Add another new task to the test
#    task = test.add('taskB')
#    task.incError()
#
#    # Add a new test to the variant with no tasks
#    test = variants['v0'].add('test1')
#    test.incError()
#
#    print variants['v0'].name, variants['v0'].error_count
#    for child in variants['v0'].children:
#        print "  ", child.name, child.error_count
#        for c in child.children:
#            print "    ", c.name, c.error_count
