.. _Icarus: http://iverilog.wikia.com/wiki/Installation_Guide
.. _Windows: http://bleyer.org/icarus/

Installing
==========
There are multiple ways to install SimShop depending on how one intends to use
it.  It can be download either as a source distribution, which can be installed
as a Python package and used to write ones own simulation scripts, or it can be
downloaded as a pre-compiled distribution for Windows or Mac OSX. For Linux the
only option is to install from a source distribution.

SimShop currently only supports the Icarus Verilog simulator, so be sure
to download and install it before attempting to simulate a design with 
SimShop.

General install guide for Icarus: http://iverilog.wikia.com/wiki/Installation_Guide

Icarus binaries for Windows: http://bleyer.org/icarus/

Binary Distribution
-------------------
Binary versions of SimShop are generated with each release for Windows and Mac
OSX. These provide a way of installing SimShop as standalone command line
applications without having to understand Python packages. These also bundle a
Python interpreter so there is no need to install a separate Python runtime to
use them. 

.. note:: These are **not** GUI applications. They are meant to be run from the command line. 


Mac OSX
^^^^^^^

Download the latest OSX DMG file from 
`here <https://github.com/RTLCores/SimShop/downloads>`_.

After the file is downloaded double click on it to mount the disk image to the
filesystem.  Drag the .app file into your ``/Applications`` folder to install
it.

To run the OSX version from the command line after it's been installed to the
``/Applications`` directory issue the following command from
the terminal:

::

    /Applications/SimShop.app/Contents/MacOS/SimShop

Add the following entry to ~/.bash_profile to be able to run the application
from the command line via the alias **shop**.

::

    function shop { /Applications/SimShop.app/Contents/MacOS/SimShop $*; }

Windows
^^^^^^^

Download the latest ZIP file from 
`here <https://github.com/RTLCores/SimShop/downloads>`_.
After the file is downloaded extract it by right clicking on the file and
selecting "Extract All".

Once it's installed you'll want to add the location of the executable to the
PATH environment variable so that it can be run from the command line.

::

    shop.exe


Source Distribution
-------------------
The source distribution is a pure Python package structured such that it can be
hosted on the Python Package Index (PyPi) website and installed via PIP,
setup.py install or easy_install.


PIP from PyPi (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    pip install SimShop

PIP from a source tarball
^^^^^^^^^^^^^^^^^^^^^^^^^
::

    pip install SimShop-<version>.tar.gz

easy_install from PyPi
++++++++++++++++++++++
::

    easy_install SimShop
