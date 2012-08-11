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

Declaring Tests
---------------
Tests are simple collections of Verilog tasks. Any task that you have defined
in your testbench can be run from a test. Declaring a test with a single tasks
would look like the following.

::

    [basic_test]
    TASKS = tb.basic

Tests can have more than one task too.

::

    [regression]
    TASKS = tb.basic
            tb.set_rate(1)
            tb.send_data
            tb.set_rate(3)
            tb.send_data

Tests can also call other tests.

::

    [basic1]
    TASKS = tb.basic1

    [basic2]
    TASKS = tb.basic2

    [basic3]
    TASKS = tb.basic3

    [regression]
    TASKS = [basic1] [basic2] [basic3]

Only 1 level of recursion is currently allowed.

Example
-------
Here's a full configuration file named v.cfg that defines the required entries
as well as some optional entries and defines some tests.

::

    [DEFAULT]
    PROJ_ROOT = ../../

    RTL_FILES = rtl/and_nand.v 
                rtl/or_nor.v

    DUMPVARS = (0,tb)

    TEST_FILES =    test/variant0/tb.v 

    TEST_INC_DIRS = test/variant0/

    [basic1]
    TASKS = tb.basic1

    [basic2]
    TASKS = tb.basic2

    [basic3]
    TASKS = tb.basic3

    [regression]
    TASKS = [basic1] [basic2] [basic3] 

Listing available tests with SimShop:

::

    $ shop -l
    Found the following config files
    --------------------------------
    ./v.cfg

    ./
        basic1
        basic2
        basic3
        regression

    To run a simulation:
    shop <path_to/variant>/<test>

    Example:
        shop regression

Running the regression test.

::

    $ shop regression

    Verifying target...
      PATH    : ./
      VARIANT : variant0
      TEST    : regression


    Generating auto test file based on test 'regression'

    Removing old build directory: simbuild/regression

    Making new build directory: simbuild/regression

    iverilog -Wall -osimbuild/regression/sim -I../../test/variant0/ ../../test/variant0/tb.v ../../rtl/and_nand.v ../../rtl/or_nor.v simbuild/regression/auto_test.v
    vvp -n -lsimbuild/regression/sim.log simbuild/regression/sim

    <0> Dump file set to simbuild/regression/out.vcd.
    <0> Dumping has been turned OFF. Nothing will be dumped.

    <0> Starting Auto Tests
    Task: basic1
    Task: basic2
    Task: basic3


    Simulation Score              
    `-- variant0                  
        `-- regression              [PASS]  (00h 00m 00s)

    Passed      1/1 (100.0%)
    Failed      0/1 (0.0%)
    Invalid     0
    Incomplete  0
    Not Run     0
    Errors      0
    Warnings    0
    Run Time    00h 00m 00s
