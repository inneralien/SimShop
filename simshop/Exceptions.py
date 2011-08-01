# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

class BaseError(Exception):
    def __init__(self, method_name, short_message, long_message):
        Exception.__init__(self)
        self.method_name = method_name
        self.error_message = short_message
        self.long_message = long_message

    def __str__(self):
        return self.error_message

class LogFileDoesNotExistError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

#==============================================================================
# TestFind Exceptions
#==============================================================================
class TestFindError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class NoConfigFileFound(TestFindError):
    def __init__(self, method_name, error_message, long_message):
        TestFindError.__init__(self, method_name, error_message, long_message)

class NoTestStructure(TestFindError):
    def __init__(self, method_name, error_message, long_message):
        TestFindError.__init__(self, method_name, error_message, long_message)

#==============================================================================
# SimCfg Exceptions
#==============================================================================
class SimCfgError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class MultipleConfigFiles(SimCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class NoTestSpecified(SimCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class InvalidTest(SimCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class InvalidPath(SimCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

class NoSimConfigFound(SimCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

#==============================================================================
# SimShopCfg Exceptions
#==============================================================================
class SimShopCfgError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)
class InvalidConfigFile(SimShopCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)
class NoConfigFile(SimShopCfgError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)

#==============================================================================
# EmailScoreBoard Exceptions
#==============================================================================
class EmailError(BaseError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)
class MissingSMTPServerError(EmailError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)
class MissingEmailConfigSection(EmailError):
    def __init__(self, method_name, error_message, long_message):
        BaseError.__init__(self, method_name, error_message, long_message)
