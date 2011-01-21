#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess

class SimRun():
    def __init__(self, cmds=[]):
        self.cmds = cmds
        self.show_cmds = True

    def showCmds(self, enable):
        self.show_cmds = bool(enable)

    def run(self, store_stdio=False):
#        print len(self.cmds)
        if(store_stdio is True):
            print "****************************"
            print "TBD: Make this message clear"
            print "****************************"
            print "-- Collecting stdout/stderr for error tabulation --"
            print "-- You will *not* see any output from this simulation --"
            print "-- until it has completed. --"
        for cmd in self.cmds:
            if(self.show_cmds):
#                print ">",
                print " ".join(cmd)
            try:
                if(store_stdio is True):
                    print ""
                    print "Running with tabulation"
                    print ""
                    run_process = subprocess.Popen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    (stdout, stderr) = run_process.communicate()
                else:
                    print ""
                    print "Running without tabulation"
                    print ""
                    run_process = subprocess.Popen(cmd,
#                        stderr=subprocess.PIPE)
                    )
                    (stdout, stderr) = run_process.communicate()
#                run_process = subprocess.Popen(cmd, stdout=f)
#                run_process = subprocess.Popen(cmd, stdout=f)
#                print "STDOUT", stdout
                if(run_process.returncode):
#                    print "RAISE", stdout, stderr
                    raise ProcessFail
            except OSError, (instance):
#                print instance
                break
#            except KeyboardInterrupt:
#                print "KeyboardInterrupt Caught... terminating simulation"
#                (stdout, stderr) = run_process.communicate()
#                print "STUFF", stdout, stderr
#                run_process.terminate() # Only works with Py2.6+
            finally:
#                f = open('out.log', 'w')
                if(stdout is not None):
                    print "PRINTING STDOUT"
                    print stdout
                if(stderr is not None):
                    print stderr
#                f.close()

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
