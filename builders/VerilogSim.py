# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import os
import time
from CmdArgs import CmdArgs
from CmdRun import CmdRun
import Exceptions
from HMS import HMS

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
        self.flags['plusargs']      = CmdArgs(cmd=lambda x: self._prepend('+', x))

        self.rel_proj_root = None
        self.run_time = HMS(0)

        self.cmds = []

    def __getitem__(self, key):
        if(key in self.flags):
            return self.flags[key]
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if(key not in self.flags):
            self.flags[key] = CmdArgs(value = value)
        else:
                # Clear the entire list before adding values to it
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
        for name,value in self.cfg.items(self.cfg.test_section):
            self[name] = value.split()
        self.setRelativeRoot()

    def setRelativeRoot(self):
        proj_root = ' '.join("%s" % x for x in self['proj_root'])
        self.rel_proj_root = os.path.normpath(self.cfg.path + "/" + proj_root)

    def run(self, index=None):
        if(index is not None):
            s = CmdRun([self.cmds[index]])
        else:
            s = CmdRun(self.cmds)
        try:
            start_time = time.time()
            s.run()
            end_time = time.time()
            self.run_time = HMS(end_time-start_time)
#            self.run_time = self.seconds_to_hms(end_time-start_time)
        except Exceptions.ProcessFail, info:
#            print dir(info)
#            print "Error message", info.error_message
#            print info.method_name[0]
            stdio_logfile = info.method_name[0] + '_cmd.log'
            build_logfile =  self.cfg.build_path + '/' + stdio_logfile
            info.log_file = build_logfile
            f = open(build_logfile, 'w')
            f.write(info.error_message)
            f.close()
            raise

#        for commands in stdio:
#            stdio_logfile = commands['cmd'][0] + '_cmd.log'
#            build_logfile =  self.cfg.build_path + '/' + stdio_logfile
#            f = open(build_logfile, 'w')
#            if(commands['stdout'] is not None):
#                f.write(commands['stdout'])
#            if(commands['stderr'] is not None):
#                f.write(commands['stderr'])
#            f.close()

#                print commands['stderr']
#        print "VerilogSim Stdio:", stdio
#        return stderr
#        (stdout, stderr) = s.run()

    def buildCmd(self):
        print "VerilogSim: Overload this method to create a custom command"

    def seconds_to_hms(self, total_seconds):
        hours = total_seconds/3600.
        minutes = hours*60.
        minutes = minutes%60.
        seconds = total_seconds%60.
        return "%.2dh %.2dm %.2ds" % (hours, minutes, seconds)

#class MissingRequiredFields(Exception):
#    def __init__(self, cfg, field):
#        Exception.__init__(self)
#        print "The config %s is missing the required field %s" % \
#            (cfg, field)
