#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import time
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
import Exceptions

import email_template
import css_template

class EmailScoreBoard(object):
    """
    Class used to generate and send an email containing simulation results.
    It uses the [email] section of a standard SimShop configuration object
    to fill in the following required values:
        * to
        * from
        * smtp_server
        * smtp_server_port
        * password
    """
    def __init__(self, cfg, score_board):
        self.cfg = cfg
        self.score_board = score_board
        if(self.cfg.has_section('email')):
            self.smtp_server        = self.cfg.get('email', 'smtp_server')
            self.smtp_server_port   = self.cfg.get('email', 'smtp_server_port')
            self.password           = self.cfg.get('email', 'password')
            self.to_addr            = self.cfg.get('email', 'to').split()
            self.from_addr          = self.cfg.get('email', 'from')
        else:
            raise Exceptions.MissingEmailConfigSection('__init__', "The config file has no 'email' section", None)

        self.status = {
                    False: "FAILED",
                    True: "PASSED",
        }

        self.msg = MIMEMultipart('alternative')
        if(self.cfg.has_option('email', 'subject')):
            s = string.Template(self.cfg.get('email', 'subject'))
            subject = s.safe_substitute({'status': self.status[self.score_board['pass']]})
            self.msg['Subject'] = "%s" % subject
        else:
            self.msg['Subject'] = "Simulation - %s" % self.status[self.score_board['pass']]
        self.msg['From'] = self.from_addr
        self.msg['To'] = COMMASPACE.join(self.to_addr)

    def connectToServer(self):
        self.server=smtplib.SMTP(self.smtp_server, self.smtp_server_port)
        # If your mail server requires a username/login, you'll need the
        # following
        if((self.from_addr is not None) and (self.password is not None)):
            self.server.starttls()
            self.server.login(self.from_addr, self.password)

    def disconnectFromServer(self):
        self.server.quit()

    def send(self):
        print ""
        print "Sending scoreboard via email..."
        print "  To   :", self.msg['To']
        print "  From :", self.msg['From']
        self.msg.attach(MIMEText(self.makeBodyText(print_html=False, print_colors=False), 'plain'))
        self.msg.attach(MIMEText(self.makeBodyText(print_html=True), 'html'))
        self.connectToServer()
        self.server.sendmail(self.from_addr, self.to_addr, self.msg.as_string())
        self.disconnectFromServer()

    def makeBodyText(self, print_html=True, print_colors=False):
        longest = self.score_board.longestString(self.score_board)
        tree = self.score_board.asciiTree(self.score_board, pad=longest+4, max_level=3, print_color=print_colors, print_html=print_html)
        tally = self.score_board.asciiTally(self.score_board)
        s = string.Template(email_template.fancy_template)
        if(print_html):
            return s.safe_substitute({
                                        'tree': tree,
                                        'tally': tally,
                                        'css_style': css_template.css_template,
                                        'date': time.strftime("%d-%h-%Y"),
            })
        else:
            return tree + tally

if __name__ == '__main__':
    import SimShopCfg
    import ScoreBoard
    sb = ScoreBoard.ScoreBoard()
    sb.loadPickleFile('score.pkl')
    s = SimShopCfg.SimShopCfg()
    s.readConfigs()
    em = EmailScoreBoard(s, sb)
#    em.send()
