Resource Configuration Files
============================
The simshoprc is a standard ConfigParser formatted file where SimShop
customizations are defined. SimShop looks for configuration files in predefined
places on the file system. 

* OSX/Linux
    1) Command line : --config-file=my.ini
    2) User         : ~/.simshoprc"
    3) System Wide  : /etc/simshop/simshoprc

* Windows
    1) Command line : --config-file=my.ini
    2) User         : %USERPROFILE%\\simshoprc
    3) System Wide  : %ALLUSERSPROFILE%\\simshoprc

SimShop will read any and all of these files, if they exist, starting with the
system wide file, followed by the user file and finally any file passed on
the command line. The most recently read file will overwrite any options that
were defined in previous configuration files. This is useful when, for
instance, a group wants to use a common email distribution list for receiving
simulation results but for a test simulation an individual user may want the
results to be emailed only to them. That user can override the email settings
by either creating a simshoprc in their home directory or passing a temporary
one on the command line. The users custom configuration file only needs to
contain the items that he would like to override, not every item in the system
wide configuration file.

.. todo::Add [init] section
.. 
    [init]
    ------
    .. describe:: testbench_template

       A shell verilog file that contains a starting point testbench. This can
       be used to simplify the generation of new variants and their associated
       testbenches.

    .. describe:: simcfg_template

       Here one can define a standard simcfg file that will be used for each
       variant. A standard simcfg might have a list of RTL or test files already
       populated to make it easier to begin a simulation.

[email]
-------
Settings which allow the simulation scoreboard report to be emailed to any
number of recipients.

.. describe:: to
   
    Any number of email address to which a simulation report should be sent
    separated by a space and/or newline.

    ::

        to = bill@ourserver.com ted@ourserver.com station@ourserver.com

    or

    ::

        to = bill@ourserver.com 
             ted@ourserver.com 
             station@ourserver.com

.. describe:: from

   A single email address from which the email will be sent.

   ::

        from = git@our_gmail_server.com


.. describe:: subject

   A custom subject message. Some automatic string substitution is available
   which SimShop will replace when the email is actually sent. For instance, the
   status of the simulation can be replaced as part of the subject line.

   ::

        subject = My simulation - $status

   The $status message will be replaced with either PASS or FAIL depending on
   the result of the simulation.

   Available string substitutions are:

    .. describe:: $status

       - PASS
       - FAIL
    

.. describe:: password

   The password for the email account from which the email will be sent.

.. describe:: smtp_server

   The SMTP server from which the email will be sent.

   ::

        smtp_server = smtp.gmail.com

.. describe:: smtp_server_port

   The SMTP server port from which the email will be sent.

   ::

        smtp_server_port = 587

.. describe::html_template

   A Python file that describes the HTML template for the body of the email
   that will be sent.

.. describe::css_template

   A Python file that describes the CSS template for the style of the HTML
   encoded email that will be sent.


.. todo::Initial Variant Creation section

