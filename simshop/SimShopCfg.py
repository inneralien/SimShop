#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import sys, os
import Exceptions
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser
import logging
import NullHandler

#h = NullHandler.NullHandler()
#logger = logging.getLogger(__name__)
#logger.addHandler(NullHandler.NullHandler())
#logging.getLogger(__name__).addHandler(h)

unix_plats = ['darwin', 'linux', 'linux2']
win_plats  = ['win32']

class SimShopCfg(SafeConfigParser):
    """
    This class is used to maintain the standard configuration environment
    which includes things like email settings.
    The default places to look for a config file are:
        OSX/Linux
        =========
        1) Command line : --config-file=my.ini
        2) User         : os.path.expanduser("~") + ".simshoprc"
        3) System Wide  : /etc/simshop/simshoprc

        Windows
        =======
        1) Command line : --config-file=my.ini
        2) User         : os.environ['USERPROFILE'] + "simshoprc"
        3) System Wide  : os.environ['ALLUSERSPROFILE'] + "simshoprc"

    """
    def __init__(self):
        self._log = logging.getLogger('%s.%s' % (__name__, self.__class__.__name__))
        self._log.addHandler(NullHandler.NullHandler())
        SafeConfigParser.__init__(self)
#        logging.error("HERE IS AN ERROR")
#        self.logger = logging.getLogger(__name__)
#        self.logger.addHandler(NullHandler.NullHandler())
#        logging.getLogger(__name__).addHandler(NullHandler.NullHandler())
        self.rc_files = []
        self.successful_rc_files = []
        if(sys.platform in unix_plats):
            self.rc_files = [
                                '/etc/simshop/simshoprc',
                                os.path.normpath(os.path.expanduser("~")  + "/.simshoprc"),
                             ]
        elif(sys.platform in win_plats):
            self.rc_files = [
                                os.path.normpath(os.environ['ALLUSERSPROFILE'] + "/simshoprc"),
                                os.path.normpath(os.environ['USERPROFILE'] + "/simshoprc"),
                             ]

    def readConfigs(self, cfg_file=None):
        if(cfg_file is not None):
            if(type(cfg_file) == type([])):
                self.rc_files.extend(cfg_file)
            else:
                self.rc_files.append(cfg_file)
        self.successful_rc_files = self.read(self.rc_files)
        if(len(self.successful_rc_files) > 0):
            return self.successful_rc_files
        else:
            raise Exceptions.NoConfigFile("SimShopCfg", "Couldn't find a valid SimShop configuration file", None)

    def __getitem__(self, key):
        try:
            value = self.get('DEFAULT', key)
            return value
        except NoOptionError, (instance):
            print "SimShopCfg ERROR - There is no '%s' item" % key
            return ''

    def __setitem__(self, key, value):
        if(not self.has_option('DEFAULT', key)):
            print "==== Missing option:", key
        self.set('DEFAULT', key, value)


if __name__ == '__main__':
    s = SimShopCfg('conf/rc1.ini')
    print s.sections()
    print s.items('test')
#    print s.get('first', 'smtpserver')
#    print s.get('email', 'smtpserver_port')
