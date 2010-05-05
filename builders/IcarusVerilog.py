from VerilogSim import VerilogSim

class IcarusVerilog(VerilogSim):
    """
    Defaults:
        TIMESCALE   : 1ns / 10ps
        OUTFILE     : sim
        DUMPFILE    : dump.vcd
        WARN        : all
    """
    def __init__(self, cfg):
        VerilogSim.__init__(self, cfg)
        self.compCmd = ['iverilog']
        self.simCmd = ['./sim']
        self.plusargs = None
        self.flags['warn'] = lambda x: self.prepend('-W', x)
        self.comp_flags = [
            ('warn',            lambda x: self.prepend('-W', x)),
            ('outfile',         lambda x: self.prepend('-o', x)),
            ('defines',         lambda x: self.prepend('-D', x)),
            ('rtl_inc_dirs',    lambda x: self.prependWithPath('-I', x)),
            ('test_inc_dirs',   lambda x: self.prependWithPath('-I', x)),
            ('rtl_files',       lambda x: self.prependWithPath('', x)),
            ('test_files',      lambda x: self.prependWithPath('', x)),
            ('dump',            None),
        ]
        self.sim_flags = [
            ('plusargs',        lambda x: self.prepend('+', x)),
        ]
        
        self.buildCompCmd()
        self.buildSimCmd()
        self.cmds = [self.compCmd, self.simCmd]

    def buildCompCmd(self):
        print "IcarusVerilog Compile"
        for i,f in self.comp_flags:
            if(i in self.data and not None):
                if(f is not None):
                    flag = f(self[i])
                    self.compCmd += flag

    def buildSimCmd(self):
        print "IcarusVerilog Simulation"
        for i,f in self.sim_flags:
            if(i in self.data and not None):
                if(f is not None):
                    flag = f(self[i])
                    self.simCmd += flag

#        self.simCmd = [self.outfile, self.plusargs]

        ## Remove all None items from the list
#        for i in range(self.compCmd.count(None)): 
#            self.compCmd.remove(None)
#        for i in range(self.simCmd.count(None)): 
#            self.simCmd.remove(None)
                    
#                    '-W%s' % self.warn,
#                    '-o%s' % self.outfile,
#                   ] #\
                    #+ self.prepend('-D', self.defines) \
                    #+ self.prepend('-I' + rel_proj_root + "/", inc_dirs) \
                    #+ self.prepend(rel_proj_root + "/", src_files)

