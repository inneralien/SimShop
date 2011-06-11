=====
Intro
=====
|SIM| is a tool that makes running command line based Verilog simulations 
simple. 

|SIM| is part of the simulation environment used to run baseline simulations of
cores purchased from RTLCores.  The simulation environment is included with any
purchased source level RTL core. It is being released under the BSD license for
use by anyone who would like an easy way to set up and run Verilog simulations.

At RTLCores, we wanted a way to run simulations on Mac OSX, Linux and Windows
through a consistent interface. Normally we would just use Make, but using Make
on Windows requires the installation of Cigwin which, while it's a wonderful
tool, is a pain for some people to deal with. Python, on the other hand, is
very easy to install and use on all platforms. There are other reasons to favor
Python to make for creating a Verilog simulation environment, but that's
a much longer conversation.

|SIM| is a work in progress, as all software is, with new features being added
all the time. We at RTLCores use it every day with excellent results and hope
that you will too.

Why command line
================
You may be wondering why we would choose to do simulations via the command
line. The answer is that more often than not GUIs are a hindrance. Once you
start using a vendor's GUI it's really difficult to switch to another vendors
tool if the need arises, and it will. Running simulations from the command line
keeps your environment agnostic, allows the use of simulation grid and makes it
much easier to automate various processes.
