#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import re
import os, os.path
import string
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser
from test_template import test_template
import Exceptions
import distutils

class SimCfg(SafeConfigParser):
    """
    This class is used to maintain the simulation environment
    including paths and config files.
    """
    def __init__(self):
        self.defaults = {
                'TIMESCALE':        '1ns / 10ps',
                'TIMEOUT':          '40000000',
                'BUILDDIR':         'simbuild',
                'AUTO_TEST_FILE':   'auto_test.v',
                'DUMPFILE':         'out.vcd',
                'DUMPVARS':         '(0,tb)',
                'SIMFILE':          'sim',
                'LOGFILE':          'sim.log',
                'BUILDFILE':        'build.log',
                'PROJ_ROOT':        './',
                'DEFINES':          '',
                'PLUSARGS':         '',
                'RTL_FILES':        '',
                'RTL_INC_DIRS':     '',
                'TEST_FILES':       '',
                'TEST_INC_DIRS':    '',
                'TASKS':            '',
                    # Simulator Specific Options
                'COMPCMD':          'iverilog',
                'SIMCMD':           'vvp',
                'WARN':             'all',
        }
        SafeConfigParser.__init__(self, self.defaults)

        self.invalid = False    # Invalid variant/test
        self.incomplete = False # Incomplete Test
        self.not_run = False    # Command failure
        self.incomplete_error_message = None

#        self.post_read_defaults = []
#        self.invalid_default_items = []

        self.cfg_files = []
        self.target = None
        self.path = None
        self.test_section = None
        self.rel_proj_root = None
        self.tasks = []

    def __getitem__(self, key):
        try:
            value = self.get(self.test_section, key)
            return value
        except NoOptionError, (instance):
            print "LOG - missing config option: '%s'" % key
#            return list()
            return ''

    def __setitem__(self, key, value):
#        print dir(self)
        if(not self.has_option(self.test_section, key)):
            print "==== Missing option:", key
#        print "%s -> %s" % (key.upper(), value)
#        return self.set(self.test_section, key, value)
        self.set(self.test_section, key, value)

    def readCfg(self, path=None):
        """
        Given a path to a directory, search for a .cfg file and
        read it in.  If more than one is found raise an exception.

        Some checking goes on here to make sure that only valid options
        are declared in a config file.
        Any options in the B{[DEFAULT]} section that are not initially
        declared in the I{self.defaults} dictionary are invalid and removed
        from the section. This is true of options in sections other than
        B{[DEFAULT]} as well.

        @type  path: string
        @param path: A directory path
        """
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
            self.invalid = True
            raise Exceptions.MultipleConfigFiles('readCfg', self.cfg_files, None)
        else:
            self.read(self.cfg_files[0])

            # DEFAULT Section Checks
        for item in self.items('DEFAULT'):
#            self.post_read_defaults.append(item[0])
            if(item[0].upper() not in self.defaults):
                print 'Unrecognized option "%s" in [DEFAULT] section of %s' % \
                    (item[0].upper(), os.path.normpath(self.cfg_files[0]))
                self.remove_option('DEFAULT', item[0])
#                self.invalid_default_items.append(item[0])

            # Test Section Checks
        for test in self.sections():
            for option in self.options(test):
                if(option.upper() not in self.defaults):
#                    if(option not in self.invalid_default_items):
                    print 'Unrecognized option "%s" in [%s] section of %s' % \
                        (option.upper(), test, os.path.normpath(self.cfg_files[0]))
                    self.remove_option(test, option)

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
        (self.path, self.test_section) = os.path.split(target)
        if(self.path == ""):
            self.path = "./"
        (n, self.variant) = os.path.split(self.path)
        if(self.variant == ""):
            (n, self.variant) = os.path.split(os.getcwd())
        print ""
        print "Verifying target..."
        print "  PATH".ljust(9), ":", self.path
        print "  VARIANT".ljust(9), ":", self.variant
        print "  TEST".ljust(9), ":", self.test_section
        print ""
        if(os.path.exists(self.path)):
            self.readCfg(self.path)
            if(self.has_section(self.test_section)):
                self.tasks = self.get(self.test_section, 'TASKS').split()
                self.task_list = list(self.tasks)
                self.tasks = [x+';' for x in self.tasks]
                self.tasks = "\n".join(str(x) for x in self.tasks)
            else:
                self.invalid = True
                raise Exceptions.InvalidTest('verifyTarget', self.test_section, None)
        else:
            self.invalid = True
            raise Exceptions.InvalidPath('verifyTarget', self.variant, None)

    def genAutoTest(self, dry_run=False, use_variant_dir=False):
        """
        Generate an auto_test.v file from a template file and a
        replacements dictionary.
        """
        print ""
        print "Generating auto test file based on test '%s'" % self.test_section
        print ""
        full_path = self.path + '/' + self['PROJ_ROOT']
        self.rel_proj_root = os.path.normpath(full_path)

        if(use_variant_dir == False):
            build_path =    self.rel_proj_root + \
                                '/' + \
                                self['BUILDDIR'] + \
                                '/' + \
                                self.variant + \
                                '/' + \
                                self.test_section
        else:
            build_path =   self.path + \
                                '/' + \
                                self['BUILDDIR'] + \
                                '/' + \
                                self.test_section

        ## Dumpvars
        dumpvars = ""
        # search for strings like this (0, tb)
        dumpvars_re = re.compile('\(\d+\s*,\s*\w+\)')
        s = dumpvars_re.findall(self['DUMPVARS'])
        for i in s:
            dumpvars += "$dumpvars%s;" % i
        # TODO Should probably put some error checking here

        self.build_path = os.path.normpath(build_path)
        self.auto_test = self.build_path + '/' + self['AUTO_TEST_FILE']
        self.dumpfile = self.build_path + '/' + self['DUMPFILE']
        self.outfile = self.build_path + '/' + self['SIMFILE']
#        self['auto_test'] = self.build_path + '/' + self['auto_test_file']
#        self['dumpfile'] = self.build_path + '/' + self['dumpfile']

            # Remove existing and/or create new build directory
        if(dry_run is True):
            pass
#            print "Build Path:", self.build_path
        else:
            if(os.path.exists(self.build_path)):
                print "Removing old build directory: %s" % self.build_path
                print ""
                distutils.dir_util.remove_tree(self.build_path)
            print "Making new build directory: %s" % self.build_path
            print ""
            distutils.dir_util.mkpath(self.build_path)
            s = string.Template(test_template)
            f = open(self.auto_test, 'w')
            f.write(s.safe_substitute( {'timescale': self['timescale'],
                                        'timeout': self['timeout'],
                                        'tasks': self.tasks,
                                        'dumpfile': self.dumpfile,
                                        'dumpvars': dumpvars
                                        })
            )
            f.close()


if __name__ == '__main__':
    s = SimCfg()
#    print s.defaults()
#    print dir(s)
    s.readCfg('./test/')
#    s.test = 'DEFAULT'
#    s.verifyTarget('scratch/BOB')
    print 'test', s.test_section
    print s['timescale']
    print s['builddir']
    print dir(s)
#    print dir(s)
#    print s.defaults()
#    print s.get('DEFAULT', 'dumpfile')
#    self.tasks = self.get(self.test, 'TASKS').split()
