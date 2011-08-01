.. _tarball: http://dl.dropbox.com/u/36920546/simshop_example.tar.gz
.. _zipball: http://dl.dropbox.com/u/36920546/simshop_example.zip

==========
QuickStart
==========
Here is a short example of running a simulation on a design that's already
set up for SimShop. Using a very simple design that can be downloaded as
either a zipball_ or a tarball_, 
I'll run a simulation with SimShop.

Untar/unzip the file which will create the example directory structure that
contains the Verilog RTL, the testbench and a couple simshop config files.

::
    
    $ tar zxvf simshop_example.tar.gz
    $ cd simshop_example/
    $ ls -l
    total 0
    drwxr-xr-x  4 tweaver  staff  136 Jun  8 05:28 rtl/
    drwxr-xr-x  4 tweaver  staff  136 Mar 16 05:37 test/
    $ tree .
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

    4 directories, 6 files

Listing Available Tests
-----------------------
The tests to be run are specified in config files which are contained in a
directory that constitutes a test *variant*. Each variant directory contains a
testbench and a simulation config file. In the example case above the testbench
Verilog file is named *tb.v* and the simulation config file is *v.cfg*. To list
the available tests in the core use the ``-l`` or ``--list-tests`` option. By
default SimShop will search for files that have a .cfg extension and attempt to
parse them for any available tests.

::

    $ shop -l
    Found the following config files
    --------------------------------
    ./test/variant0/v.cfg
    ./test/variant1/v.cfg

    test/variant0/
        basic

    test/variant1/
        basic

    To run a simulation:
    shop <path_to/variant>/<test>

    Example:
        shop test/variant1/basic
    
    $


In this case the simulation script found two config files 
``./test/variant0/v.cfg`` and ``./test/variant1/v.cfg``
and lists the tests contained in each. The config files only define a single
test named *basic*. The last thing that is printed out is an example of how
one can run a test.


Running a Simulation
--------------------
To run the test listed in the example above one would type the following

::

    shop test/variant1/basic


Assuming Icarus Verilog is already installed, the output of the command would
produce

::

    $ shop test/variant1/basic

    Verifying target...
      PATH    : test/variant1
      VARIANT : variant1
      TEST    : basic


    Generating auto test file based on test 'basic'

    Making new build directory: test/variant1/simbuild/basic

    iverilog -Wall -otest/variant1/simbuild/basic/sim -I./test/variant1/ ./test/variant1/tb.v ./rtl/and_nand.v ./rtl/or_nor.v test/variant1/simbuild/basic/auto_test.v
    vvp -n -ltest/variant1/simbuild/basic/sim.log test/variant1/simbuild/basic/sim

    <0> Dump file set to test/variant1/simbuild/basic/out.vcd.
    <0> Dumping has been turned OFF. Nothing will be dumped.

    <0> Starting Auto Tests
    --------||---------|----------|--------|--------
    in1 in0 || and_out | nand_out | or_out | nor_out
    --------||---------|----------|--------|--------
     0   0  ||    0    |     1    |   0    |    1
     0   1  ||    0    |     1    |   1    |    0
     1   0  ||    0    |     1    |   1    |    0
     1   1  ||    1    |     0    |   1    |    0


    Simulation Score              
    `-- variant1                  
        `-- basic                   [PASS]  (00h 00m 00s)

    Passed      1/1 (100.0%)
    Failed      0/1 (0.0%)
    Invalid     0
    Incomplete  0
    Not Run     0
    Errors      0
    Warnings    0
    Run Time    00h 00m 00s
    $ 

    
The output of the simulation is directed to a sub-directory of the variant that
is being simulated.  The default build directory is ``simbuild``, so in this
case the output would be written to 
::

    test/variant1/simbuild/basic/

All output files associated with the simulation are kept in this directory.  To
dump a VCD waveform file just pass the ``-pDUMPON`` argument on the command
line which passes the plusarg DUMPON to the simulation:

::

    $ bin/sim -pDUMPON test/variant1/basic
