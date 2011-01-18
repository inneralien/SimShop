#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import re

"""
Takes a list of variants and tests and generates a scoreboard based off
of regular expression matches.

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

Variant
    Test
        Tasks

Deserializer                 PASS/FAIL  Warnings      Errors
    regression                  PASS       3             0

Serializer                   PASS/FAIL  Warnings      Errors
    serial_8N1                  1/0         3           0

    serial_8N2                  1/0         3           0
        serial_8N2              PASS        0           0

    serial_8P1                  3/0         3           0
    serial_8P2                  3/0         3           0


"""

class ScoreBoard():
    """
    cfg: SimCfg object
    """
    def __init__(self, sim_cfg):
        self.sim_cfg = sim_cfg
        self.errorRegex = []
        self.warningRegex = []
        self.errors = []
        self.warnings = []
        self.error_re = re.compile(r'ERROR')

    def addWarningRegex(self, regex):
        self.warningRegex.append(regex)

    def addErrorRegex(self, regex):
        self.errorRegex.append(regex)

    def newTest(self, testname):
        pass

    def newVariant(self, variant):
        pass

    def searchFile(self, filename):
        print "FILENAME:", filename
        f = open(filename, 'r')
        for i in f.readlines():
            for regex in self.errorRegex:
                s = regex.search(i)
                if(s is not None):
                    self.errors.append(s)
            for regex in self.warningRegex:
                s = regex.search(i)
                if(s is not None):
                    self.warnings.append(s)

        print "%d Errors:" % len(self.errors)
        for i in self.errors:
            print "  ", i.group()
        print ""
        print "%d Warning:" % len(self.warnings)
        for i in self.warnings:
            print "  ", i.group()


if __name__ == '__main__':
    filename = sys.argv[1]
    logs = []
    s = ScoreBoard(logs)
    s.addErrorRegex(re.compile(r'ERROR(.*)'))
    s.addErrorRegex(re.compile(r'Error(.*)'))
    s.addErrorRegex(re.compile(r'Error(.*)'))
    s.searchFile(filename)
