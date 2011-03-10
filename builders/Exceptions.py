# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

class BuildersBaseError(Exception):
    def __init__(self, method_name, short_message, long_message):
        Exception.__init__(self)
        self.method_name = method_name
        self.error_message = short_message
        self.long_message = long_message

class ProcessFail(BuildersBaseError):
    def __init__(self, method_name, error_message, long_message, log_file=None):
        BuildersBaseError.__init__(self, method_name, error_message, long_message)
        self.log_file = log_file
