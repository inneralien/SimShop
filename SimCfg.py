#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re, os
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser

class SimCfg(SafeConfigParser):
    """
    This class is used to maintain the simulation environment
    including paths and config files.
    """
    def __init__(self):
        SafeConfigParser.__init__(self)
        self.cfg_files = []
        self.cfg_file = None
        self.target = None
        self.path = None
        self.test = None

    def __getitem__(self, item):
        try:
            value = self.get('DEFAULT', item)
            return value
        except NoOptionError, (instance):
            print "LOG - missing config option: '%s'" % item
            return list()


    def __setitem__(self, key, value):
        return self.set('DEFAULT', key, value)

    def getCfg(self, path=None):
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
                        self.read(self.cfg_file)

    def listTests(self):
        """
        List all available tests from the current working directory down.
        """
        self.getCfg()
        if(len(self.cfg_files) > 0):
            for config in self.cfg_files:
                self.read(config)
                if(self.has_option('DEFAULT', 'PROJ_ROOT')):
                    proj_root = self.get('DEFAULT', 'PROJ_ROOT')
                else:
                    proj_root = ''
                path = os.path.normpath(os.path.split(config)[0])
                print "%s/" % (path) #, self.cp.get('DEFAULT', 'VARIANT_NAME'))
                for section in self.sections():
                    print "    %s" % section
                print "--------------------------"
        print ""
        print "To run a simulation:"
        print "simulate <path_to/variant>/<test>"

    def verifyTarget(self, target):
        """
        Verify that the name of the target test passed on the command line
        really does exist in the config files.
        """
        print "Verifying Target: %s" % target
        self.target = target
        try:
            (self.path, self.test) = os.path.split(target)
#            (self.path, self.test) = target.split('.')
            print self.path, self.test
        except:
            self.path = target
            self.test = ''

        if(os.path.exists(self.path)):
            self.getCfg(self.path)
            if(self.has_section(self.test)):
                print "Generating test file based on test '%s'" % self.test
            else:
                print "No test given or found, so just compiling the files"
        else:
            print "No valid target found"
            sys.exit(1)

