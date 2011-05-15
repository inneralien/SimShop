Intro
=====
SimShop is a tool that makes running command line based Verilog simulations 
simple. 

SimShop is part of the simulation environment used to run baseline simulations
of cores purchased from RTLCores.  The simulation environment is included with
any purchase of a source level RTL core.

**TODO** <Link to detailed documentation>

At RTLCores, we wanted a way to run simulations on Mac OSX, Linux and Windows
through a consistent interface. Normally we would just use Make, but using Make
on Windows requires the installation of Cigwin which, while it's a wonderful
tool, is a pain for some people to deal with. Python, on the other hand, is
very easy to install and use on all platforms.

Why command line
================
You may be wondering why we would choose to do simulations via the command
line. The answer is that more often than not GUIs are a hindrance. Once you
start using a vendor's GUI it's really difficult to switch to another vendors
tool if the need arises, and it will. Running simulations from the command line
keeps your environment agnostic and also allows the use of simulation grid.

**TODO** *Show an image of a typical simulation grid*

Supported Verilog Simulators
============================
Current
    - `Icarus Verilog <http://www.icarus.com/eda/verilog/>`_

Future
    - `Modelsim <http://model.com/>`_
    - `Synopsys VCS <http://www.synopsys.com/tools/verification/functionalverification/pages/vcs.aspx>`_
    - `Cadence NC <http://www.cadence.com/us/pages/default.aspx>`_

System Requirements
===================
- Python 2.4+
- Supported Platforms
    - Mac OSX 10.5+
    - Linux
    - Windows XP, Vista, 7
- Verilog Simulator
