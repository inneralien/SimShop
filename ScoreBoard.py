#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import re

"""
Takes a list of variants and tests and generates a scoreboard based off
of regular expression matches.

Possible ASCII outputs:
+------------------------------------------------------------+
| TEST SUMMARY:                                              |
+----------------------------+-----------+----------+--------+
| Test                       | PASS/FAIL | WARNINGS | ERRORS |
+----------------------------+-----------+----------+--------+
| Deserializer/              |   PASS    |   0      |   0    |
|     stop_errors            |   PASS    |   0      |   0    |
|     start_errors           |   PASS    |   0      |   0    |
|     parity_errors          |   FAIL    |   2      |   7    |
|     start_errors           |   PASS    |   0      |   0    |
|------------------------------------------------------------|
|                            |    4/1    |   2      |   7    |
|------------------------------------------------------------|
| Serializer/                |           |          |        |
|     serial_8N1             |   PASS    |   0      |   0    |
|     serial_8N2             |   PASS    |   0      |   0    |
|     serial_8P1             |   PASS    |   0      |   0    |
|     serial_8P2             |   PASS    |   0      |   0    |
|------------------------------------------------------------|
|                            |    4/0    |   0      |   0    |
+============================+===========+==========+========+
| All Tests                  | PASS/FAIL | WARNINGS | ERRORS |
|                            |    8/1    |   2      |   7    |
|------------------------------------------------------------|

+-----------------------------------------+
| TEST SUMMARY:                           |
+--------------------+-----------+--------+
| Test               | PASS/FAIL | ERRORS |
+--------------------+-----------+--------+
| test_stop_errors   |   PASS    |   0    |
| test_start_errors  |   PASS    |   0    |
| test_parity_errors |   FAIL    |   7    |
| test_start_errors  |   PASS    |   0    |
+--------------------+-----------+--------+

TEST SUMMARY:                     PASS/FAIL   ERRORS
------------------------------------------------------
deserializer                         FAIL        7
  regression                         FAIL        7
    test_task.test_stop_errors       PASS        0
    test_task.test_start_errors      PASS        0
    test_task.test_parity_errors     FAIL        7
    test_task.test_start_errors      PASS        0

serializer                           FAIL        2
  regression                         FAIL        2
    test_task.serial_8N1             PASS        0
    test_task.serial_8N2             FAIL        1
    test_task.serial_8P1             FAIL        1
    test_task.serial_8P2             PASS        0
------------------------------------------------------
"""

class ScoreBoard():
    """
    cfg: SimCfg object
    """
    def __init__(self):
        self.scores = {}
        self.variant_list = []
        self.errorRegex = []
        self.warningRegex = []
        self.testBeginRegex = None  # There can be only 1
        self.testEndRegex = None    # There can be only 1
        self.errors = []
        self.warnings = []
        self.error_re = re.compile(r'ERROR')

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
        test = sim_cfg.test
        logfile = sim_cfg.build_path + "/" + sim_cfg['logfile']
        print "==============================================================================="
        print " Scoring Simulation %s/%s" % (variant, test)
        print " %s" % logfile
        print "==============================================================================="
        if(variant in self.variant_list):
            print "FOUND %s" % variant
        else:
            print "Adding new variant: %s" % variant
            self.variant_list.append(variant)
            self.scores[variant] = Score(name=variant)

            # Add a test to the variant
        test_score = self.scores[variant].add(test)

        # A log file contains 1 variant, 1 test and 0 or more tasks
        task_scores = self.searchFile(sim_cfg, test_score)
#        print task_scores

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
        score = test_score
        logfile = sim_cfg.build_path + "/" + sim_cfg['logfile']
        got_test_begin = False
        task_list = []

        print "Scanning for errors and warnings"
        f = open(logfile, 'r')
        for i in f.readlines():
                # Search for know Task names
            for task in sim_cfg.task_list:
                if(task not in task_list):
                    r = re.compile(r'%s' % task)
                    s = r.search(i)
                    if(s is not None):
                        task_name = s.group()
                        task_list.append(task_name)
                        test = test_score.add(task_name)
                            # score is the current child in the Score hierarchy
                        score = test

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
                    print "Found TEST_BEGIN"
                    if(got_test_begin is True):
                        score.incIncomplete()
                    else:
                        got_test_begin = True

                # Search for test end expression
            if(self.testEndRegex is not None):
                s = self.testEndRegex.search(i)
                if(s is not None):
                    print "Found TEST_END"
                    if(got_test_begin is False):
                        score.incIncomplete()
                    else:
                        got_test_begin = False

            # If the simulation is canceled then it should be reported
            # as an incomplete. Right?
        if(got_test_begin is True):
            score.incIncomplete()

    def printReport(self):
        """
        Print an ascii report to stdout.
        """
        print "++ Printing Report ++"
        for v in self.variant_list:
            print self.scores[v].name, self.scores[v].error_count
            for test in self.scores[v].children:
                print "  ", test.name, test.error_count, test.incomplete_count
                for task in test.children:
                    print "    ", task.name, task.error_count, task.incomplete_count


class Score(list):
    """
    A Score contains a 'test' and some children 'tasks'
    """
    def __init__(self, value=[], name=None, parent=None):
        list.__init__(self, value)
        self.name = name
        self.parent = parent
        self.error_count = 0
        self.warning_count = 0
        self.incomplete_count = 0
        self.children = []
        self.current_child = None

    def add(self, name):
        print "adding %s to %s" % (name, self.name)
        self.append(name)
        child = Score(name=name, parent=self)
        self.children.append(child)
        return child

    def incError(self):
        print "Incrementing error in %s" % (self.name)
        len_children = len(self.children)
        if(self.parent is not None):
            self.parent.incError()
        self.error_count += 1

    def incWarning(self):
        print "Incrementing warning in %s" % (self.name)
        if(self.parent is not None):
            self.parent.incWarning()
        self.warning_count += 1

    def incIncomplete(self):
        print "Incrementing incomplete error in %s" % (self.name)
        if(self.parent is not None):
            self.parent.incIncomplete()
        self.incomplete_count += 1


if __name__ == '__main__':
    variants = {}
    variants['v0'] = Score(name='v0')

    # Add a new test to the variant
    test = variants['v0'].add('test0')

    # Add a new task to the test
    task = test.add('task0')
    task.incError()
    # Add another new task to the test
    task = test.add('task1')
    task.incError()

    # Add a new test to the variant
    test = variants['v0'].add('test1')
    # Add a new task to the test
    task = test.add('taskA')
    task.incError()
    # Add another new task to the test
    task = test.add('taskB')
    task.incError()

    # Add a new test to the variant with no tasks
    test = variants['v0'].add('test1')
    test.incError()

    print variants['v0'].name, variants['v0'].error_count
    for child in variants['v0'].children:
        print "  ", child.name, child.error_count
        for c in child.children:
            print "    ", c.name, c.error_count
