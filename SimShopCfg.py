#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import sys, os
import Exceptions
from ConfigParser import NoOptionError
from ConfigParser import SafeConfigParser

class SimShopCfg(SafeConfigParser):
    """
    This class is used to maintain the standard configuration environment
    which includes things like email settings.
    """
    def __init__(self, cfg_file=None):
        SafeConfigParser.__init__(self)
        self.cfg_files = []
        self.cfg_files.append(os.path.join(sys.path[0], 'conf', 'simshop.ini'))
        if(cfg_file is not None):
            self.cfg_files.append(cfg_file)
        success_list = self.read(self.cfg_files)
        if(len(success_list) > 0):
            print "Successfully read the following config files:"
            for i in success_list:
                print "  - %s" % i
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
    s = SimShopCfg('conf/simshop-example.ini')
    print s.get('email', 'smtpserver')
    print s.get('email', 'smtpserver_port')
