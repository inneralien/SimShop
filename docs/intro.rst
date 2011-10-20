.. _RTLCores: http://rtlcores.com
.. _documentation: http://simshop.readthedocs.org

=====
Intro
=====
SimShop is a tool that makes running command line based Verilog simulations 
simple. 

SimShop is part of the simulation environment used to run baseline simulations
of cores purchased from RTLCores_. The simulation environment is included with
any purchased source level RTL core. It is being released under the BSD license
for use by anyone who would like an easy way to set up and run Verilog
simulations.

At RTLCores_, we wanted a way to run simulations on Mac OSX, Linux and Windows
through a consistent interface. Normally we would just use Make, but using Make
on Windows requires the installation of Cigwin which, while it's a wonderful
tool, is a pain for some people to deal with. Python, on the other hand, is
very easy to install and use on all platforms. There are other reasons to favor
Python over Make for creating a Verilog simulation environment, but that's a
much longer conversation.

SimShop is a work in progress, as all software is, with new features being
added all the time. We at RTLCores_ use it every day with excellent results and
hope that you will too.

Why command line
================
You may be wondering why we would choose to run simulations via the command
line. The answer is that more often than not GUIs are a hindrance.  Running
simulations from the command line keeps your environment agnostic, allows the
use of simulation grids and makes it much easier to automate various processes.

Documentation
=============
For information on how to install and use SimShop check out the pretty
documentation_. 
