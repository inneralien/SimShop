#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess

class SimRun():
    def __init__(self, cmds=[]):
        self.cmds = cmds
        self.show_cmds = True

    def showCmds(self, enable):
        self.show_cmds = bool(enable)

    def run(self):
        print len(self.cmds)
        for cmd in self.cmds:
            if(self.show_cmds):
#                print ">",
                print " ".join(cmd)
            try:
                run_process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
#                run_process = subprocess.Popen(cmd, stdout=f)
#                run_process = subprocess.Popen(cmd, stdout=f)
                (stdout, stderr) = run_process.communicate()
                print "STDOUT", stdout
                if(run_process.returncode):
                    print "RAISE", stdout, stderr
                    raise ProcessFail
            except OSError, (instance):
                print instance
                break
            except KeyboardInterrupt:
                print "KeyboardInterrupt Caught... terminating simulation"
#                (stdout, stderr) = run_process.communicate()
#                print "STUFF", stdout, stderr
#                run_process.terminate() # Only works with Py2.6+
            finally:
                f = open('out.log', 'w')
                print stdout, stderr
                f.close()

class ProcessFail(Exception):
    def __init__(self):
        print "In ProcessFail Exception"

if __name__ == '__main__':
    s = SimRun(['pwd'])
    s.run()
    cmds = []
    cmds.append([['pwd'], ['ls', '-ltrp'], ['pwd'], ['nocmd']])
    for cmd in cmds:
        s.cmds = cmd
        s.run()
