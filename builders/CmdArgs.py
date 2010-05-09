class CmdArgs(list):
    def __init__(self, value=[], cmd=None):
        list.__init__(self, value)
        self.cmd = cmd

#    def __setitem__(self, key, value):
#        print "SETITEM", key, value

#    def __getitem__(self, key):
#        print "GETITEM", key

    def conv(self):
        if(self.cmd == None):
            return self
        else:
            return self.cmd(self)
