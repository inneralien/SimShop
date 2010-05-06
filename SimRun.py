#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess

class SimRun():
    def __init__(self, cmds=None):
        self.cmds = []
        self.show_cmds = True

    def showCmds(self, enable):
        self.show_cmds = bool(enable)

    def run(self):
        for cmd in self.cmds:
            if(self.show_cmds):
                print ">",
                print " ".join(cmd)
            try:
                run_process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                run_process.communicate()
                if(run_process.returncode):
                    raise ProcessFail
            except OSError, (instance):
                print instance
                break
            except KeyboardInterrupt:
                print "KeyboardInterrupt Caught... terminating simulation"
                run_process.terminate()

class ProcessFail(Exception):
    def __init__(self):
        print "In ProcessFail Exception"

if __name__ == '__main__':
    s = SimRun()
    s.cmds = (['pwd'], ['./t.py'], ['ls', '-ltrp'], ['pwd'], ['nocmd'])
    s.run()
