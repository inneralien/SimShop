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
        for cmd in self.cmds:
            if(self.show_cmds):
                print " ".join(cmd)
            try:
                run_process = subprocess.Popen(cmd,
                )
                (stdout, stderr) = run_process.communicate()
                if(run_process.returncode):
                    raise ProcessFail
            except OSError, (instance):
                break
            finally:
                if(stdout is not None):
                    print "PRINTING STDOUT"
                    print stdout
                if(stderr is not None):
                    print stderr

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
