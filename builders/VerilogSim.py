import os
import sys

class VerilogSim():
    def __init__(self, cfg):
        self.cfg = cfg
        self.data = {}
        self.flags = {
            # Compiler Flags
            'defines':         lambda x: self.prepend('-D', x),
            'rtl_inc_dirs':    lambda x: self.prependWithPath('-I', x),
            'test_inc_dirs':   lambda x: self.prependWithPath('-I', x),
            'rtl_files':       lambda x: self.prependWithPath('', x),
            'test_files':      lambda x: self.prependWithPath('', x),
            # Simulation Flags
            'plusargs':        lambda x: self.prepend('+', x),
            }
        self.cmds = []
        self.comp_flags = [
            (),
        ]
        self.rel_proj_root = None
        self.required_fields = ['proj_root']
        self.populate()

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def populate(self):
        """
        This is where the config file items get converted into
        class variables.
        """
        # Check for required fields first
        for field in self.required_fields:
            if(not self.cfg.has_option('DEFAULT', field)):
                raise MissingRequiredFields(self.cfg.cfg_file, field)
            for item in self.cfg.items('DEFAULT'):
                self.data[item[0]] = item[1].split()
#        self.checkRequiredFields()
            self.setRelativeRoot()

    def checkRequiredFields(self):
        for field in self.required_fields:
            if(field not in self.data):
                print "%s doesn't exist in %s" % (field.upper(), cfg.cfg_file)
                sys.exit(1)

    def setRelativeRoot(self):
        if('proj_root' not in self.data):
            print "%s doesn't exist in %s" % (field.upper(), cfg.cfg_file)
            sys.exit(1)
        else:
            proj_root = self.cfg.get('DEFAULT', 'PROJ_ROOT')
            self.rel_proj_root = os.path.normpath(self.cfg.path + "/" + proj_root)

    def prependWithPath(self, flag, items):
        return ["%s%s/%s" % (flag,self.rel_proj_root,b) for b in items]

    def prepend(self, flag, items):
        return ["%s%s" % (flag,b) for b in items]

    def buildCmd(self):
        print "VerilogSim: Overload this method to create a custom command"

class MissingRequiredFields(Exception):
    def __init__(self, cfg, field):
        Exception.__init__(self)
        print "The config %s is missing the required field %s" % \
            (cfg, field)
