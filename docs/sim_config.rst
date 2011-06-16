======================
Simulation Config File
======================
Simulation config files are used to define the files needed for a simulation as
well as define the tests that can be run. Each variant will have one and only
one simulation config file.

Required Entries
----------------
.. describe:: PROJ_ROOT

    This item describes where the project root is located relative to the
    directory containing the config file. For instance, if a directory 
    structure was setup to look like the following:

::

    .
    |-- rtl
    |   |-- and_nand.v
    |   `-- or_nor.v
    `-- test
        |-- variant0
        |   |-- tb.v
        |   `-- v.cfg
        `-- variant1
            |-- tb.v
            `-- v.cfg
        

The root of the project is at the top of the tree and the two config files,
*v.cfg*, are two directories down, so relative to those config files PROJ_ROOT
would be two directories up or ../../

::

    PROJ_ROOT = ../../


.. describe:: RTL_FILES

    This item is a list of all the RTL files needed by the variant. All
    files are relative to the PROJ_ROOT.

::

    RTL_FILES = rtl/and_nand.v rtl/or_nor.v

.. describe:: RTL_INC_DIRS
    
   If there are files include in the source via the ```include`` statement
   the compiler needs to know where those files are located and
   ``RTL_INC_DIRS`` defines those directories.

::

    RTL_INC_DIRS = rtl/includes

.. describe:: TEST_FILES

   Any files used by the testbench that aren't RTL are defined here.

::

   TEST_FILES = test/tb.v test/other_test_file.v

.. describe:: TEST_INC_DIRS

   Just like the RTL_INC_DIRS, if there are included files used by the
   testbench the directories they are contained in would be defined here.

::

   TEST_INC_DIRS = test/includes test/models/includes

Optional Entries
----------------
.. describe:: DEFINES

::

    DEFINES = VERBOSE FILTEN

.. describe:: TIMEOUT

::

   TIMEOUT = 50000000

.. describe:: TIMESCALE

::

   TIMESCALE = 1ns/10ps

.. todo:: Define the rest of the optional entries

Here are all of the available options and their default values:

::

    'BUILDDIR':         'simbuild',
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
        # Auto Test Variables
    'AUTO_TEST_FILE':   'auto_test.v',
    'DUMPFILE':         'out.vcd',
    'DUMPVARS':         '(0,tb)',
    'TIMESCALE':        '1ns / 10ps',
    'TIMEOUT':          '40000000',
    'RESET':            '',
    'FINISH':           '$finish',
    'TIMEOUT_ERROR':    '',
        # Simulator Specific Options
    'COMPCMD':          'iverilog',
    'SIMCMD':           'vvp',
    'WARN':             'all',
