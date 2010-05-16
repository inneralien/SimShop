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
        self.compCmd = ['iverilog']
        self.plusargs = None

        ## Default flags specific to Icarus Verilog
        ## and any required list comprehension commands
        self['compCmd'] = ['iverilog']
        self['builddir'] = ['run']
        self['warn'] = ['all']
        self['warn'].cmd = lambda x: self._prepend('-W', x)
        self['outfile'] = ['sim']
        self['outfile'].cmd = lambda x: self._prepend('-o', x)

        ## Run the populate method to do the cfg conversion
        self.populate()

        self.buildCompCmd()
        self.buildSimCmd()
        # Create the builddir if it doesn't exist
        distutils.dir_util.mkpath(self['builddir'][0])

        # Collect the commands into a list of sequential commands
        self.cmds = [self.comp_cmd, self.sim_cmd]

    def buildCompCmd(self):
        self['outfile'] = [self['builddir'][0] + '/' + self['outfile'][0]]
        self.comp_cmd = self['compCmd'] +  \
                        self['warn'].conv() +  \
                        self['outfile'].conv() + \
                        self['defines'].conv() + \
                        self['rtl_inc_dirs'].conv() + \
                        self['test_inc_dirs'].conv() + \
                        self['rtl_files'].conv() + \
                        self['test_files'].conv()# + \

    def buildSimCmd(self):
        self.sim_cmd = self['outfile']
