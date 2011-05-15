#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

from optparse import OptionParser
import sys
import subprocess
import logging

__author__        = "Tim Weaver"
__copyright__     = "Copyright: (C) 2011 RTLCores LLC."
__creation_date__ = "Sun Jan  2 08:17:16 PST 2011"
__version__       = 'v0.1.0'

class BaseError(Exception):
    def __init__(self, method_name, short_message, long_message):
        Exception.__init__(self)
        self.method_name = method_name
        self.error_message = short_message
        self.long_message = long_message

class GitInfoError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

if __name__ == '__main__':
#==============================================================================
# Define logging levels for the command line
#==============================================================================
    LEVELS = {  'debug'    : logging.DEBUG,
                'info'     : logging.INFO,
                'warning'  : logging.WARNING,
                'error'    : logging.ERROR,
                'critical' : logging.CRITICAL,
            }

#==============================================================================
# Option Parser
#==============================================================================
    parser = OptionParser(usage="%prog <options> [tag]", version="%s\n%s" % (__version__, __copyright__))
    parser.add_option("-n", "--just-print",
                        default=False,
                        action='store_true',
                        dest="just_print",
                        help="just print the command that would be run.")
    parser.add_option("-d", "--debug",
                        dest="debug",
                        default='error',
                        help="Run in special debug mode. Valid options are debug, info, warning, error, critical")
    parser.add_option("-l", "--long_messages",
                        default=False,
                        action='store_true',
                        dest="long_messages",
                        help="Print out extra help messages on warnings and errors")

    (options, args) = parser.parse_args()

    if(len(args) == 1):
        tag = args[0]
    else:
        parser.print_help()
        sys.exit(1)

#==============================================================================
# Turn on logging
#==============================================================================
#    logging.basicConfig()
    # create logger
    logger = logging.getLogger("Archive")
    logger.setLevel(LEVELS[options.debug])

    # create console handler
    ch = logging.StreamHandler()

    # create formatter
    formatter = logging.Formatter("%(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
#==============================================================================
# Do stuff here
#==============================================================================
#    archive_cmd = "git archive --format=tar --prefix=sim_%s/ %s > sim_%s.tar" % (tag, tag, tag)
    archive_cmd = "git archive --format=tar --prefix=sim_%s/ %s -o sim_%s.tar" % (tag, tag, tag)
    if(options.just_print is True):
        print archive_cmd
    else:
        logger.debug(archive_cmd)
        (resp, cmd_error) = subprocess.Popen(archive_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if(cmd_error):
            logger.error(cmd_error)
        else:
            print "Successfully wrote sim_%s.tar" % (tag)

