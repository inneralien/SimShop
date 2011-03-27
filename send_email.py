#!/usr/bin/env python

import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_template import email_template_html

import string
import ScoreBoard
import pickle
import css_template

FROMADDR = 'git@rtlcores.com'
SMTPSERVER = 'smtp.gmail.com'

# me == my email address
# you == recipient's email address
me = "tim@rtlcores.com"
you = "inneralien@gmail.com"

# Read in the ScoreBoard object
sb = ScoreBoard.ScoreBoard()
pkl_file = open('score.pkl', 'rb')
data = pickle.load(pkl_file)
pkl_file.close()

status = {
            False: "- FAILED",
            True: "- PASSED",
        }

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Regression %s" % status[data['pass']]
msg['From'] = me
msg['To'] = you

print "msg['Subject']", msg['Subject']
#sys.exit(0)

longest = sb.longestString(data)
#tree_text = sb.asciiTree(data, pad=longest+4, max_level=3, print_color=False, print_html=False)
tree_html = sb.asciiTree(data, pad=longest+4, max_level=3, print_color=True, print_html=True)
tally = sb.asciiTally(data)
#f = open('style.css')
#css_style = f.read()
#f.close()
css_style = css_template.css_template
# Create the body of the message (a plain-text and an HTML version).
#text = tree_text
#text = "THIS IS SOME PLAIN TEXT"
html_template = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
    <pre>
$tree
$tally
    </pre>
    </p>
  </body>
</html>
"""
#s = string.Template(html_template)
s = string.Template(email_template_html)
#subject = "Regressions %s" % status
#time.strftime("%d-%h-%Y")
html = s.safe_substitute({
                            'tree': tree_html,
                            'tally': tally,
                            'css_style': css_style,
                            'date': time.strftime("%d-%h-%Y"),
})

print html
#print "%r\n%r" % (tree_text, tree_html)
#exit(0)
# Record the MIME types of both parts - text/plain and text/html.
#part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
#msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
server = smtplib.SMTP(SMTPSERVER, 587)
# If your mail server requires a username/login, you'll need the following
server.starttls()
server.login('git@rtlcores.com', 'daic9ed9cas9yick9dav')
#server.sendmail(FROMADDR, toaddrs, msg)
#server.quit()

# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
server.sendmail(me, you, msg.as_string())
server.quit()
