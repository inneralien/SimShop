import os
import sys
from CmdArgs import CmdArgs
from SimRun import SimRun

class VerilogSim():
    def __init__(self, cfg):
        self.cfg = cfg
        self.flags = {}
        self.flags['proj_root']     = CmdArgs(value=['./'])
        self.flags['defines']       = CmdArgs(cmd=lambda x: self._prepend('-D', x))
        self.flags['rtl_inc_dirs']  = CmdArgs(cmd=lambda x: self._prependWithPath('-I', x))
        self.flags['test_inc_dirs'] = CmdArgs(cmd=lambda x: self._prependWithPath('-I', x))
        self.flags['rtl_files']     = CmdArgs(cmd=lambda x: self._prependWithPath('', x))
        self.flags['test_files']    = CmdArgs(cmd=lambda x: self._prependWithPath('', x))
        self.flags['plusargs']      = CmdArgs(cmd=lambda x: self._prependWithPath('+', x))

        self.rel_proj_root = None

        self.cmds = []

    def __getitem__(self, item):
        return self.flags[item]

    def __setitem__(self, key, value):
        if(key not in self.flags):
            self.flags[key] = CmdArgs(value = value)
        else:
            del self.flags[key][:]
            self.flags[key].extend(value)

    def _prependWithPath(self, flag, items):
        """
        Method to prepend a flag and the relative project root to
        a list of items.
        """
        return ["%s%s/%s" % (flag,self.rel_proj_root,b) for b in items]

    def _prepend(self, flag, items):
        """
        Method to prepend a flag to a list of items.
        """
        return ["%s%s" % (flag,b) for b in items]

    def populate(self):
        """
        This is where the config file items get converted into
        CmdArgs.
        """
        for name,value in self.cfg.items('DEFAULT'):
            self[name] = value.split()
        self.setRelativeRoot()

    def setRelativeRoot(self):
        proj_root = ' '.join("%s" % x for x in self['proj_root'])
        self.rel_proj_root = os.path.normpath(self.cfg.path + "/" + proj_root)

    def run(self):
        s = SimRun(self.cmds)
        s.run()

    def buildCmd(self):
        print "VerilogSim: Overload this method to create a custom command"

class MissingRequiredFields(Exception):
    def __init__(self, cfg, field):
        Exception.__init__(self)
        print "The config %s is missing the required field %s" % \
            (cfg, field)
