# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

missing_logfile_help = """
    When a simulation runs it will generate a log file that contains all
    of the output that it prints. The ScoreBoard module attempts to read this
    file and generate a tally of the tests performance.
    If that log file cannot be found it probably means the design failed to
    compile for some reason and therefore the simulation never ran.
"""
