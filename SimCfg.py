#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re, sys
import os, os.path
import string
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser
from test_template import test_template
import distutils

class SimCfg(SafeConfigParser):
    """
    This class is used to maintain the simulation environment
    including paths and config files.
    """
    def __init__(self):
        SafeConfigParser.__init__(self)
        self.cfg_files = []
        self.target = None
        self.path = None
        self.test = None
        self.rel_proj_root = None
        self.tasks = []
        self['timescale'] = '1ns / 10ps'
        self['timeout'] = '40000000'
        self['builddir'] = 'build'
        self['auto_test_file'] = 'auto_test.v'
#        self['plusargs'] = ''
#        self['defines'] = ''

    def __getitem__(self, item):
        try:
            value = self.get('DEFAULT', item)
            return value
        except NoOptionError, (instance):
            print "LOG - missing config option: '%s'" % item
#            return list()
            return ''

    def __setitem__(self, key, value):
        print "KEY, VALUE", key, type(value)
        return self.set('DEFAULT', key, value)

    def readCfg(self, path=None):
        """
        Given a path to a directory, search for a .cfg file and
        read it in.  If more than one is found raise an exception.
        """
#        print path
        cfg = re.compile(".*\.cfg$")
        if(path is None):
            path = '.'
            self.cfg_files = []
        for directory, subdirs, files in os.walk(path):
            for f in files:
                found = cfg.search(f.strip())
                if(found is not None):
                    self.cfg_files.append("%s%s%s" % (directory, os.sep, f))
        if(len(self.cfg_files) > 1):
            raise MultipleConfigFiles(self.cfg_files)
        else:
            self.read(self.cfg_files[0])

    def verifyTarget(self, target):
        """
        Verify that the name of the target test passed on the command line
        really does exist in the config files.
        """
        print "Verifying Target: %s" % target
        self.target = target
        if(not os.path.exists(self.target)):
            pass
        else:
            raise NoTestSpecified(self.target)
        
        try:
            (self.path, self.test) = os.path.split(target)
            (n, self.variant) = os.path.split(self.path)
#            print self.path, self.test, self.variant
        except:
            self.path = target
            self.test = ''

        if(os.path.exists(self.path)):
            self.readCfg(self.path)
            if(self.has_section(self.test)):
                print "Generating test file based on test '%s'" % self.test
                self.tasks = self.get(self.test, 'TASKS').split()
                self.tasks = [x+';' for x in self.tasks]
                self.tasks = "\n".join(str(x) for x in self.tasks)
            else:
                raise InvalidTest(self.test)

    def genAutoTest(self):
        """
        Generate an auto_test.v file from a template file and a
        replacements dictionary.
        """
#        print "BULIDDIR", self['BUILDDIR']
#        print "PROJ_ROOT", self['PROJ_ROOT']
#        print "path", self.path
        full_path = self.path + '/' + self['PROJ_ROOT']
#        print "full_path", full_path
        self.rel_proj_root = os.path.normpath(full_path)
#        print self.rel_proj_root

# build dir is relative to PROJ_ROOT
        self.auto_test_path =    self.rel_proj_root + \
                            '/' + \
                            self['BUILDDIR'] + \
                            '/' + \
                            self.variant
#                            '/'
#                            self['auto_test_file']


                           
#        print "self.auto_test_path", self.auto_test_path
        distutils.dir_util.mkpath(self.auto_test_path)
        self['auto_test'] = self.auto_test_path + '/' + self['auto_test_file']
        s = string.Template(test_template)
#        f = open(self.auto_test_path + '/' + 'auto_test.v', 'w')
#        f = open(self.auto_test_path + '/' + self['auto_test_file'], 'w')
        f = open(self['auto_test'], 'w')
#        print type(self.tasks)
#        print self.tasks
        f.write(s.safe_substitute( {'timescale': self['timescale'],
                                    'timeout': self['timeout'],
                                    'tasks': self.tasks})
        )
        f.close()

class SimCfgError(Exception):
    """Base class for exceptions"""
    pass

class MultipleConfigFiles(SimCfgError):
    def __init__(self, cfgs):
        self.data = cfgs

class NoTestSpecified(SimCfgError):
    def __init__(self, target):
        self.data = target
#        print "No tests were specified in the target: %s" % \
#            (target)

class InvalidTest(SimCfgError):
    def __init__(self, test):
        self.data = test
#        print "An invalid test was specified: %s" % \
#            (test)
