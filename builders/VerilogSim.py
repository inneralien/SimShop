import os
import sys

class Flag():
    def __init__(self, name, value, cmd):
        self.name = name
        self.value = value
        self.cmd = cmd

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def conv(self):
        return self.cmd(self.value)

class VerilogSim():
    def __init__(self, cfg):
        self.cfg = cfg
        self.flag_cmds = {
            # Compiler Flags
            'defines':         lambda x: self._prepend('-D', x),
            'rtl_inc_dirs':    lambda x: self._prependWithPath('-I', x),
            'test_inc_dirs':   lambda x: self._prependWithPath('-I', x),
            'rtl_files':       lambda x: self._prependWithPath('', x),
            'test_files':      lambda x: self._prependWithPath('', x),
            # Simulation Flags
            'plusargs':        lambda x: self._prepend('+', x),
            }
        self.cmds = []
        self.rel_proj_root = None
        self.required_fields = ['proj_root']
        self.flags = {}
        self['proj_root']       = './'
        self['plusargs']        = []
        self['defines']         = []
        self['rtl_files']       = []
        self['rtl_inc_dirs']    = []
        self['test_files']      = []
        self['test_inc_dirs']   = []

#        self.populate()

    def __getitem__(self, item):
        return self.flags[item]

    def __setitem__(self, key, value):
        self.flags[key] = value

    def _prependWithPath(self, flag, items):
        return ["%s%s/%s" % (flag,self.rel_proj_root,b) for b in items]

    def _prepend(self, flag, items):
        return ["%s%s" % (flag,b) for b in items]

    def flag(self):
        print "stuff"

    def populate(self):
        """
        This is where the config file items get converted into
        class variables.
        """
        # Check for required fields first
        for field in self.required_fields:
            if(not self.cfg.has_option('DEFAULT', field)):
                raise MissingRequiredFields(self.cfg.cfg_file, field)
            else:
#                self.flags['proj_root'] = self.cfg.get('DEFAULT', 'proj_root')
                self.setRelativeRoot()
        # Check for fields that need manipulated by flag_cmds
            for item in self.cfg.items('DEFAULT'):
                if(item[0] in self.flag_cmds):
                    temp_list = item[1].split()
                    cmd = self.flag_cmds[item[0]]
                    self.flags[item[0]] = cmd(temp_list)
#                    print "ITEM", self.flags[item[0]]
                else:
        # All other fields just get set to class variables
                    self.flags[item[0]] = item[1].split()
#        self.checkRequiredFields()

    def checkRequiredFields(self):
        for field in self.required_fields:
            if(field not in self.flags):
                print "%s doesn't exist in %s" % (field.upper(), self.cfg.cfg_file)
                sys.exit(1)

    def setRelativeRoot(self):
        if('proj_root' not in self.flags):
            print "%s doesn't exist in %s" % ('proj_root'.upper(), self.cfg.cfg_file)
            sys.exit(1)
        else:
            proj_root = self.cfg.get('DEFAULT', 'PROJ_ROOT')
            self.rel_proj_root = os.path.normpath(self.cfg.path + "/" + proj_root)

    def buildCmd(self):
        print "VerilogSim: Overload this method to create a custom command"

class MissingRequiredFields(Exception):
    def __init__(self, cfg, field):
        Exception.__init__(self)
        print "The config %s is missing the required field %s" % \
            (cfg, field)
