====================
Command Line Options
====================
To list all the available command line options either run the sim command
with no options or with the ``--help`` or ``-h`` option.

.. cmdoption:: --version             
    
   Show program's version number and exit.

.. cmdoption:: -h, --help            
   
   Show the help message and exit

.. cmdoption::--init                
   
   generate an example variant directory

.. cmdoption:: -l, --list-tests      
   
   List all available tests.  SimShop will recursively search from the current
   directory for any file that ends with the extension .cfg and when found
   will list all tests described in those files.

.. cmdoption:: -n, --dry-run         
   
   Print out the commands that would be executed, but do not execute them.

.. cmdoption:: -c, --compile-only    

   Compile the simulation but don't run it.

.. cmdoption:: -d, --dumpon          

   Enable dumping of waveform. This is a convenience option for -pDUMPON.

.. cmdoption:: -v, --verbose         
   
   Display verbose error messages.

.. cmdoption:: -D DEFINES, --defines=DEFINES

   Pass in defines to the simulation. Multiple defines can be set by adding
   extra -D options.

   ::

        shop -Dfoo -Dbar="stuff" <testname>

.. cmdoption:: -p PLUSARGS, --plusarg=PLUSARGS

   Pass plusargs to the simulation. These values will be expanded to +PLUSARG
   by the simulation builder. Multiple plusargs can be set by adding extra -p
   options.

   ::

        shop -pDUMPON -pSTUFF <testname>

.. cmdoption:: -o FILE, --output-file=FILE

   Store the scoreboard report to pickled FILE.

.. cmdoption:: --rc=FILE             
   
   Parse the resource file FILE

.. cmdoption:: --email               
  
   Email the results using settings from one of the standard resource files or
   from an rc file given with the --rc option

.. cmdoption:: --to=RECIPIENT        
   
   Send email to the RECIPIENT. Multiple --to can be used to specify more
   recipients.

.. cmdoption:: --subject="SUBJECT"   
   
   Change the subject of the email. "My informative subject - $status"

.. cmdoption:: --debug=DEBUG         
   
   Run in special debug mode. Valid options are:
       * debug
       * info
       * warning
       * error
       * critical

