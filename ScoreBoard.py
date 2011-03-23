#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import sys, os
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

    def writePickleFile(self, data=None, max_level=None):
        """
        Writes a pickled version of the ScoreBoard datastructure so that
        it can be read later. This is where a database would probably make
        a more formidable choice.
        """
        import pickle
        if(data is None):
            data = self.data
        output = open('out.pkl', 'wb')
        pickle.dump(data, output, -1)
        output.close()

    def asciiTree(self, data=None, last=False, max_level=None, pad=0, print_color=True):
        if(data is None):
            data = self.data

        pad_length = len(data['name'])

        if(self.level not in self.lasts):
            self.lasts.append(self.level)

        # Lay out the tree pipes if necessary
        for i in range(1, self.level):
            if(i in self.lasts):
                self.tree_str += "|   "# % (lasts[i], i))
            else:
                self.tree_str += "    "# % (lasts[i], i))
            pad_length += 4

        # If the item is the tail of the branch it gets a ` instead of a |
        if(self.level != 0):
            if(last):
                self.tree_str += '`'
            else:
                self.tree_str += '|'
            pad_length += 1

        # All levels but the top get --
        if(self.level != 0):
            self.tree_str += '-- %s ' % (data['name'])
            pad_length += 4
        else:
            self.tree_str += '%s ' % (data['name'])
            pad_length += 1

        pad_length = pad - pad_length + 10
        if(data['status'] == 'PASS'):
            padding = ' ' + ' ' * pad_length
        else:
            padding = '<' + '-' * pad_length

        if(len(data['kids']) == 0):
            if(print_color is True):
                pass_msg = '%s [%s]' % (padding, colorize(data['status']))
            else:
                pass_msg = '%s [%s]' % (padding, data['status'])
        else:
            pass_msg = ''

        self.tree_str += "%s\n" % pass_msg

        # Remove branches that have ended
        if(self.level in self.lasts):
            if(last):
                self.lasts.remove(self.level)

        # Recurse through the children
        if((max_level is None) or (self.level < max_level)):
            for i in range(len(data['kids'])):
                last = (i == len(data['kids']) - 1)
                self.level += 1
                self.asciiTree(data['kids'][i], last, max_level=max_level, pad=pad, print_color=print_color)
                self.level -= 1

        return self.tree_str

    def asciiTally(self, data=None):
        """
        Prints out a table of the following information about a simulation:
            * Passed     - total and percentage
            * Failed     - total and percentage
            * Invalid    - total
            * Incomplete - total
            * Not Run    - total
            * Errors     - total
            * Warnings   - total

        """
        if(data is None):
            data = self.data
        str = ""

        variant_count = 0
        test_count = 0
        task_count = 0

        total_scores = 0.
        total_failures = 0.
        total_passed = 0.

        variants_failed = 0.
        tests_failed = 0.
        tasks_failed = 0.
        # Variants
        for v in data['kids']:
            total_scores += 1
            variant_count += 1
            if(not v['pass']):
                total_failures += 1
                variants_failed += 1
            else:
                total_passed += 1
            # Tests
            for t in v['kids']:
                total_scores += 1
                test_count += 1
                if(not t['pass']):
                    total_failures += 1
                    tests_failed += 1
                else:
                    total_passed += 1
                # Tasks
                for task in t['kids']:
                    total_scores += 1
                    task_count += 1
                    if(not task['pass']):
                        total_failures += 1
                        tasks_failed += 1
                    else:
                        total_passed += 1

        str+= "Passed      %d/%d (%.1f%%)\n" % (total_passed, total_scores, (total_passed/total_scores)*100.)
        str+= "Failed      %d/%d (%.1f%%)\n" % (total_failures, total_scores, (total_failures/total_scores)*100.)
        str+= "Invalid     %d\n" % (self['invalid_count'])
        str+= "Incomplete  %d\n" % (self['incomplete_count'])
        str+= "Not Run     %d\n" % (self['not_run_count'])
        str+= "Errors      %d\n" % (self['error_count'])
        str+= "Warnings    %d\n" % (self['warning_count'])

        return str

    def longestString(self, data=None, max_level=None):
        """
        Recurses throught the children of 'data' and determines the longest
        string in the bunch. This is use for formatting the tree view status
        messages.
        """
        if(data is None):
            data = self.data
        string_length = len(data['name'])
        # Recurse through the children
        if((max_level is None) or (self.level < max_level)):
            for i in range(len(data['kids'])):
                self.level += 1
                ret = self.longestString(data['kids'][i], max_level=max_level)
                if(ret > string_length):
                    string_length = ret
                self.level -= 1
        return string_length


#TODO - Need to add colored output for Windows as well
if(sys.platform == 'win32'):
    colors = {  'FAIL'   : "",
                'PASS'   : "",
                'INCOMPLETE': "",
                'INVALID': "",
                'end'    : "",
            }
else:
    colors = {  'FAIL'   : "\033[91m",
                'PASS'   : "\033[92m",
                'INCOMPLETE': "\033[95m",
                'INVALID': "\033[95m",
                'NOT RUN': "\033[95m",
                'end'    : "\033[0m",
            }

def colorize(text, type=None):
    str = ""
    if(type is None):
        str += colors[text] + text + colors['end']
    else:
        str += colors[type] + text + colors['end']
    return str

if __name__ == '__main__':
    import sys, pickle
    sb = ScoreBoard()

    pkl_file = open('out.pkl', 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()

    longest = sb.longestString(data)
    tree = sb.asciiTree(data, pad=longest+4)
    tally = sb.asciiTally(data)
    sys.stdout.write(tree)
    sys.stdout.write("\n")
    sys.stdout.write(tally)
