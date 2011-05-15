# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

class CmdArgs(list):
    def __init__(self, value=[], cmd=None):
        list.__init__(self, value)
        self.cmd = cmd

    def conv(self):
        if(self.cmd == None):
            return self
        else:
            return self.cmd(self)
