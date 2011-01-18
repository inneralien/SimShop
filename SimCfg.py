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
        self['builddir'] = 'simbuild'
        self['auto_test_file'] = 'auto_test.v'
        self['dumpfile'] = 'out.vcd'
        self['dumpvars'] = '(0,tb)'
        self['logfile'] = 'sim.log'
#        self['plusargs'] = ''
#        self['defines'] = ''

    def __getitem__(self, item):
        try:
            value = self.get(self.test, item)
            return value
        except NoOptionError, (instance):
            print "LOG - missing config option: '%s'" % item
#            return list()
            return ''

    def __setitem__(self, key, value):
        return self.set(self.test, key, value)

    def readCfg(self, path=None):
        """
        Given a path to a directory, search for a .cfg file and
        read it in.  If more than one is found raise an exception.
        """
#        print path
        self.cfg_files = []
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
        Valid target syntax
        Single targets:
            - path/variant/test_name
                - path = path/variant
                - variant = variant
                - test = test_name
            - variant/test_name
                - path = variant
                - variant = variant
                - test = test_name
            - test_name
                - path = ./
                - variant = cwd
                - test = test_name
            - test_name (FUTURE)
                - path = ./
                - variant = cfg.get('DEFAULT', 'variant') else cwd
                - test = test_name
            - path/variant/test_*   (FUTURE: Regular expression in test name)
                - path = path/variant
                - variant = variant
                - test = test_*
        """
        (self.path, self.test) = os.path.split(target)
        if(self.path == ""):
            self.path = "./"
        (n, self.variant) = os.path.split(self.path)
        if(self.variant == ""):
            (n, self.variant) = os.path.split(os.getcwd())
        print "PATH:", self.path
        print "VARIANT:", self.variant
        print "TEST:", self.test
        print ""
        if(os.path.exists(self.path)):
            self.readCfg(self.path)
            if(self.has_section(self.test)):
                print "Generating test file based on test '%s'" % self.test
                self.tasks = self.get(self.test, 'TASKS').split()
                self.tasks = [x+';' for x in self.tasks]
                self.tasks = "\n".join(str(x) for x in self.tasks)
            else:
                raise InvalidTest(self.test)
        else:
            raise InvalidPath(self.test)

    def verifyTarget_old(self, target):
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
            print "PATH:", self.path
            print "TEST:", self.test
            print "VARIANT:", self.variant
        except:
            self.path = target
            self.test = ''
        finally:
            print "in Finally"

        if(os.path.exists(self.path)):
            self.readCfg(self.path)
            if(self.has_section(self.test)):
                print "Generating test file based on test '%s'" % self.test
                self.tasks = self.get(self.test, 'TASKS').split()
                self.tasks = [x+';' for x in self.tasks]
                self.tasks = "\n".join(str(x) for x in self.tasks)
                print self.tasks
            else:
                raise InvalidTest(self.test)
        else:
            self.path = "./"
            print "INVALID PATH"

    def genAutoTest(self, dry_run=False, use_variant_dir=False):
        """
        Generate an auto_test.v file from a template file and a
        replacements dictionary.
        """
        full_path = self.path + '/' + self['PROJ_ROOT']
        self.rel_proj_root = os.path.normpath(full_path)

        if(use_variant_dir == False):
            build_path =    self.rel_proj_root + \
                                '/' + \
                                self['BUILDDIR'] + \
                                '/' + \
                                self.variant + \
                                '/' + \
                                self.test
        else:
            build_path =   self.path + \
                                '/' + \
                                self['BUILDDIR'] + \
                                '/' + \
                                self.test

        ## Dumpvars
        dumpvars = ""
        # search for strings like this (0, tb)
        dumpvars_re = re.compile('\(\d+\s*,\s*\w+\)')
        s = dumpvars_re.findall(self['DUMPVARS'])
        for i in s:
            dumpvars += "$dumpvars%s;" % i
        # TODO Should probably put some error checking here

        self.build_path = os.path.normpath(build_path)
        self['auto_test'] = self.build_path + '/' + self['auto_test_file']
        self['dumpfile'] = self.build_path + '/' + self['dumpfile']
        if(dry_run is True):
            print "Build Path:", self.build_path
        else:
            distutils.dir_util.mkpath(self.build_path)
            s = string.Template(test_template)
            f = open(self['auto_test'], 'w')
            f.write(s.safe_substitute( {'timescale': self['timescale'],
                                        'timeout': self['timeout'],
                                        'tasks': self.tasks,
                                        'dumpfile': self['dumpfile'],
                                        'dumpvars': dumpvars
                                        })
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

class InvalidTest(SimCfgError):
    def __init__(self, test):
        self.data = test

class InvalidPath(SimCfgError):
    def __init__(self, test):
        self.data = test
