class BuildersBaseError(Exception):
    def __init__(self, method_name, short_message, long_message):
        Exception.__init__(self)
        self.method_name = method_name
        self.error_message = short_message
        self.long_message = long_message

class ProcessFail(BuildersBaseError):
    def __init__(self, method_name, error_message, long_message):
        BuildersBaseError.__init__(self, method_name, error_message, long_message)