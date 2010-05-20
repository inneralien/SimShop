import os, re
from ConfigParser import SafeConfigParser

class TestFind():
    """
    This class is used to find any variant config files and list the 
    tests that they contain.
    It walks the directory tree starting at ./ looking for any file
    with the extension .cfg.
    """
    def __init__(self):
        self.cfg_files = []

    def getCfgs(self, path=None):
        cfg = re.compile(".*\.cfg$")
        if(path is None):
            path = '.'
            self.cfg_files = []
        for directory, subdirs, files in os.walk(path):
            for f in files:
                found = cfg.search(f.strip())
                if(found is not None):
                    if(path is '.'):
                        self.cfg_files.append("%s%s%s" % (directory, os.sep, f))
                    else:
                        self.cfg_file = "%s%s%s" % (directory, os.sep, f)
#                        self.read(self.cfg_file)
        print self.cfg_files

    def listTests(self):
        """
        List all available tests from the current working directory down.
        """
        self.getCfgs()
        if(len(self.cfg_files) > 0):
            for config in self.cfg_files:
                cfg = SafeConfigParser()
                cfg.read(config)
                if(cfg.has_option('DEFAULT', 'PROJ_ROOT')):
                    proj_root = cfg.get('DEFAULT', 'PROJ_ROOT')
                else:
                    proj_root = ''
                path = os.path.normpath(os.path.split(config)[0])
                print "%s/" % (path) #, cfg.cp.get('DEFAULT', 'VARIANT_NAME'))
                for section in cfg.sections():
                    print "    %s" % section
        print ""
        print "To run a simulation:"
        print "simulate <path_to/variant>/<test>"
        print ""


