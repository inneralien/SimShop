class CmdArgs(list):
    def __init__(self, value=[], cmd=None):
        list.__init__(self, value)
        self.cmd = cmd

    def conv(self):
        if(self.cmd == None):
            return self
        else:
            return self.cmd(self)
