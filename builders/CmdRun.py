#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import subprocess
import Exceptions

class CmdRun():
    def __init__(self, cmds=[]):
        self.cmds = cmds
        self.show_cmds = True
#        self.stdio = []

    def showCmds(self, enable):
        self.show_cmds = bool(enable)

    def run(self):
        for cmd in self.cmds:
            if(self.show_cmds):
                print " ".join(cmd)
            try:
                run_process = subprocess.Popen(cmd, stderr=subprocess.PIPE
                )
                (stdout, stderr) = run_process.communicate()
#                self.stdio.append({'cmd':cmd, 'stdout':stdout, 'stderr':stderr})
                if(run_process.returncode):
#                    print dir(run_process.stderr)
#                    stderr = "%s" % run_process.stderr
                    print stderr
#                    for line in run_process.stderr:
#                        print ".", line
#                    return self.stdio
#                    raise Exceptions.ProcessFail('run', 'The previous command failed', stderr)
                    raise Exceptions.ProcessFail(cmd, stderr, None)
                else:
                    pass
#                    print run_process.returncode
            except OSError, (instance):
#                print dir(instance)
#                print instance.child_traceback
#                print "strerror", instance.strerror
#                print "args", instance.args
#                print "errno", instance.errno
#                print "filename", instance.filename
#                print "IN EXCEPT"
                raise Exceptions.ProcessFail(instance.strerror)
#                break
#            finally:
##                print "IN FINALLY"
#                if(stdout is not None):
#                    print "PRINTING STDOUT"
#                    print stdout
#                if(stderr is not None):
#                    print stderr
#        return self.stdio

#class ProcessFail(Exception):
#    def __init__(self, message):
#        self.message = message
#        print "In ProcessFail Exception"

if __name__ == '__main__':
    s = CmdRun(['pwd'])
    s.run()
    cmds = []
    cmds.append([['pwd'], ['ls', '-ltrp'], ['pwd'], ['nocmd']])
    for cmd in cmds:
        s.cmds = cmd
        s.run()
