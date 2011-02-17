#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys, os
import re
import Exceptions
import help

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
        test = sim_cfg.test_section
        if(variant in self.variant_list):
            pass
#            print "FOUND %s" % variant
        else:
            self.variant_list.append(variant)
            self.scores[variant] = Score(name=variant)

            # Add a test to the variant
        test_score = self.scores[variant].add(test)

        # A log file contains 1 variant, 1 test and 0 or more tasks
        self.searchFile(sim_cfg, test_score)

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
        score = test_score
        try:
            logfile = sim_cfg.build_path + "/" + sim_cfg['logfile']
        except:
            score.incIncomplete()
        got_test_begin = False
        task_list = []

        if(not os.path.exists(logfile)):
#            print "The logfile to be scored does not exist: %s" % logfile
#            score.incIncomplete()
            raise Exceptions.LogFileDoesNotExistError('searchFile',
                'The file to be scored does not exist: %s' % logfile,
                help.missing_logfile_help)
#            return
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
                    if(got_test_begin is True):
                        score.incIncomplete()
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

    def printASCIIReport(self):
        """
        Prints a pretty ASCII table representation of the simulation
        results.
        """
            # Determine the longest string name
        longest = 0
        for v in self.variant_list:
            if(len(self.scores[v].name) > longest):
                longest = len(self.scores[v].name)
            for test in self.scores[v].children:
                if(len(test.name) > longest):
                    longest = len(test.name)
                for task in test.children:
                    if(len(task.name) > longest):
                        longest = len(task.name)
        longest = longest + 2

            # Format and print the output
        print ""
        print "Test Summary".ljust(longest+9) +\
              "Errors".rjust(6) +\
              "Incomplete".rjust(11)
        print "+-----------------------------------------------------------------------------+"
        for v in self.variant_list:
            passed = "FAIL"

            if(self.scores[v].error_count == 0 and self.scores[v].incomplete_count == 0):
                passed = "PASS"
            print "%s%s%s%s" %  ( self.scores[v].name.ljust(longest+4),
                                  passed,
                                  str(self.scores[v].error_count).rjust(5),
#                                  str(self.scores[v].warning_count).rjust(5),
                                  str(self.scores[v].incomplete_count).rjust(5)
                              )
            for test in self.scores[v].children:
                if(test.error_count == 0 and test.incomplete_count == 0):
                    passed = "PASS"
                else:
                    passed = "FAIL"
                print "  %s%s%s%s" % (test.name.ljust(longest+2),
                                      passed,
                                      str(test.error_count).rjust(5),
#                                      str(test.warning_count).rjust(5),
                                      str(test.incomplete_count).rjust(5)
                                     )
                for task in test.children:
                    if(task.error_count == 0 and task.incomplete_count == 0):
                        passed = "PASS"
                    else:
                        passed = "FAIL"
                    print "    %s%s%s%s" % ( task.name.ljust(longest),
                                             passed,
                                             str(task.error_count).rjust(5),
#                                             str(task.warning_count).rjust(5),
                                             str(task.incomplete_count).rjust(5)
                                            )

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

        self.level = 1

    def add(self, name):
#        print "adding %s to %s" % (name, self.name)
        self.append(name)
        child = Score(name=name, parent=self)
        self.children.append(child)
        return child

    def incError(self):
#        print "Incrementing error in %s" % (self.name)
#        len_children = len(self.children)
        if(self.parent is not None):
            self.parent.incError()
        self.error_count += 1

    def incWarning(self):
#        print "Incrementing warning in %s" % (self.name)
        if(self.parent is not None):
            self.parent.incWarning()
        self.warning_count += 1

    def incIncomplete(self):
#        print "Incrementing incomplete error in %s" % (self.name)
        if(self.parent is not None):
            self.parent.incIncomplete()
        self.incomplete_count += 1

    def getChildren(self, data):
        print ' ' * self.level
        for kid in self.children:
            self.level += 1
            self.getChildren(kid)
            self.level -=1

class newScore():
    """
    A dictionary version of Score to aid in recursive traversal
    """
    def __init__(self, name, parent=None):
        self.level = 0
        self.lasts = []
        self.data = {   'name'   :  name,
                        'parent' : parent,
                        'kids'   : [],
                    }

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def add(self, name):
        score = newScore(name, self)
        self.data['kids'].append(score)
        return score

    def traverse(self, data=None, last=False):
        if(data is None):
            data = self.data

        if(self.level not in self.lasts):
            self.lasts.append(self.level)

        # Lay out the tree pipes if necessary
        for i in range(1, self.level):
            if(i in self.lasts):
                sys.stdout.write("|   ")# % (lasts[i], i))
            else:
                sys.stdout.write("    ")# % (lasts[i], i))

        # If the item is the tail of the branch it gets a ` instead of a |
        if(self.level != 0):
            if(last):
                sys.stdout.write('`')
            else:
                sys.stdout.write('|')

        # All levels but the top get --
        if(self.level != 0):
            sys.stdout.write('-- %s\n' % data['name'])
        else:
            sys.stdout.write('%s\n' % data['name'])

        # Remove branches that have ended
        if(self.level in self.lasts):
            if(last):
                self.lasts.remove(self.level)

        # Recurse through the children
        for i in range(len(data['kids'])):
            last = (i == len(data['kids']) - 1)
            self.level += 1
            self.traverse(data['kids'][i], last)
            self.level -= 1


#lasts = []
#def traverse(data, last=False):
#    if(traverse.level not in lasts):
#        lasts.append(traverse.level)
#
#    # Lay out the tree pipes if necessary
#    for i in range(1, traverse.level):
#        if(i in lasts):
#            sys.stdout.write("|   ")# % (lasts[i], i))
#        else:
#            sys.stdout.write("    ")# % (lasts[i], i))
#
#    # If the item is the tail of the branch it gets a ` instead of a |
#    if(traverse.level != 0):
#        if(last):
#            sys.stdout.write('`')
#        else:
#            sys.stdout.write('|')
#
#    # All levels but the top get --
#    if(traverse.level != 0):
#        sys.stdout.write('-- %s\n' % data['name'])
#    else:
#        sys.stdout.write('%s\n' % data['name'])
#
#    # Remove branches that have ended
#    if(traverse.level in lasts):
#        if(last):
#            lasts.remove(traverse.level)
#
#    # Recurse through the children
#    for i in range(len(data['kids'])):
#        last = (i == len(data['kids']) - 1)
#        traverse.level += 1
#        traverse(data['kids'][i], last)
#        traverse.level -= 1


#def traverse_so_close(data, last=False):
#    pk = 0
#    k  = 0
#    st = ''
#    if(last):
#        traverse.lasts.pop()
#    if(data['parent'] is not None):
#        pk = len(data['parent']['kids'])
#        k  = len(data['kids'])
#        st = "(%d: %d -> %d %s %r)" % (traverse.level, pk, k, last, traverse.lasts)
#    if(traverse.level == 0):
#        print data['name'], st
#    else:
#        if(last):
#            s = '' * (traverse.level-1)
#            sys.stdout.write('%s' % s)
#            print '' * (traverse.level-1) + '-- ' + data['name'], st
#        else:
#            s1 = '' * (traverse.level-1)
#            print '' * (traverse.level-1) + '-- ' + data['name'], st
#    for i in range(len(data['kids'])):
#        last = (i == len(data['kids']) - 1)
#        if(not last):
#            if(traverse.level not in traverse.lasts):
#                traverse.lasts.append(traverse.level)
#        for j in traverse.lasts:
#            s = '    ' * j
##            s = '    ' * j
#            if(last):
#                sys.stdout.write("%s`" % s)
#            else:
#                sys.stdout.write("%s|" % s)
#        traverse.level += 1
#        traverse(data['kids'][i], last)
#        traverse.level -= 1

if __name__ == '__main__':

    a = newScore('Top')
    c = a.add('compile')
    d = c.add('test0')
    d.add('task0')
    d.add('task1')
    d = c.add('test1')
    d.add('task0')
    d.add('task1')
    d = c.add('test2')
    d.add('task0')
    d.add('task1')
    sa = a.add('simulate')
    sb = sa.add('test0')
    sc = sb.add('task0')
    sc = sb.add('task1')
    sa.add('test1')
    sa.add('test2')

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
    a.traverse()

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
