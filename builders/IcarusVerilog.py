# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

from VerilogSim import VerilogSim
import distutils.dir_util

class IcarusVerilog(VerilogSim):
    """
    Icarus Verilog class to build a compile command and a
    simulation command.
    Inherits VerilogSim

    Defaults:
    TIMESCALE   : 1ns / 10ps
    OUTFILE     : sim
    DUMPFILE    : dump.vcd
    WARN        : all

    """
    def __init__(self, cfg):
        """
        """
        VerilogSim.__init__(self, cfg)
        self.cfg = cfg

        ## Default flags specific to Icarus Verilog
        ## and any required list comprehension commands
#        self['compcmd'] = ['iverilog']
#        self['simcmd'] = ['vvp'] # -n = non-interactive mode
        self['builddir'] = ['run']
        self['warn'] = ['all']
        self['warn'].cmd = lambda x: self._prepend('-W', x)
        self['outfile'] = [self.cfg.outfile]
        self['outfile'].cmd = lambda x: self._prepend('-o', x)

        ## Run the populate method to do the cfg conversion
        ## Populate will overwrite any flags defined locally if they exist
        ## in the config file
        self.populate()

        # The test_files need to come before the rtl_files on the command
        # line or it exposes a strange thing where Icarus will detect an
        # rtl file that doesn't exist, but not return a non-zero exit code.
        # This causes the sim executable to be generated and run but there
        # is nothing to run, so it looks like it completes successfully.
    def buildCompCmd(self):
        self.comp_cmd = self['compcmd'] +  \
                        self['warn'].conv() +  \
                        self['outfile'].conv() + \
                        self['defines'].conv() + \
                        self['rtl_inc_dirs'].conv() + \
                        self['test_inc_dirs'].conv() + \
                        self['test_files'].conv() + \
                        self['rtl_files'].conv() + \
                        [self.cfg.auto_test]
#                        [self.cfg['auto_test']]
        self.cmds.append(self.comp_cmd)

    def buildSimCmd(self):
        log = '-l' + self.cfg.build_path + '/' + self.cfg['logfile']
        self.sim_cmd =  self['simcmd'] + \
                        ['-n'] + \
                        [log] + \
                        self['outfile'] + \
                        self['plusargs'].conv()
        self.cmds.append(self.sim_cmd)
