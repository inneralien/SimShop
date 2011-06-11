==========
Installing
==========
There are a couple requirements to run simulations, Python and a Verilog
simulator.  The cores designed by RTLCores should run on any professional level
simulator like Synopsys VCS or Cadence NC-Verilog as well as open source
simulators like Icarus Verilog.

There are multiple ways to install SimShop depending on how one intends to use
it.  It can be download either as a source distribution, which can be installed
as a Python package and used to write ones own simulation scripts, or it can be
downloaded as a pre-compiled distribution for Windows or Mac OSX. For Linux the
only option is downloading a source distribution.

Binary Distribution
-------------------
Binary versions of g are generated, with each release, for Windows and Mac
OSX. These provide a way of installing SimShop as standalone command line
applications without having to understand Python packages. These also bundle
a Python interpreter so there is no need to install a separate Python runtime
to use them.

<link to current OSX .app>

<link to current Windows .zip>

Source Distribution
-------------------
The source distribution is a pure Python package structured such that it can be
hosted on the Python Package Index (PyPi) website and installed via PIP,
setup.py install or easy_install.


PIP from PyPi (Recommended)
+++++++++++++++++++++++++++
::

    pip install SimShop

PIP from a source tarball
+++++++++++++++++++++++++
::

    pip install SimShop-<version>.tar.gz

easy_install from PyPi
++++++++++++++++++++++
::

    easy_install SimShop

Windows GUI Installer
+++++++++++++++++++++



System Requirements
-------------------
- Python 2.4+
- Supported Platforms
    - Mac OSX 10.5+
    - Linux
    - Windows XP
    - Windows Vista
    - Windows 7
- Verilog Simulator
    - Icarus Verilog

