import sys
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from simshop import __version__

options = {
    'name' : "SimShop",
    'version' : __version__,
    'author':'Tim Weaver',
    'author_email':'tim@rtlcores.com',
    'packages':find_packages(),
    'scripts':['bin/shop'],
    'url':'http://pypi.python.org/pypi/SimShop',
    'license':'LICENSE.txt',
    'description':'Easy Verilog simulation',
    'long_description':open('README.txt').read(),
    'classifiers' : [
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Education',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
          'Topic :: Utilities',
          ],
}

# Mac specific for py2app
if len(sys.argv) >= 2 and sys.argv[1] == 'py2app':
    # Mac specific options
    # Copy bin/shop to bin/shop.py or py2app won't build
    fo = open('bin/shop.py', 'w')
    fi = open('bin/shop', 'r')
    fo.write(fi.read())
    fi.close()
    fo.close()

    options['app'] = ['bin/shop.py']
    options['options'] = {
        'py2app': {
            'argv_emulation': True,
            'no_chdir': True,
        }
    }

# Windows specific for py2exe
if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    try:
        import py2exe
    except ImportError:
        print 'Could not import py2exe.  Windows bundle could not be built.'
        sys.exit(0)
    options['console'] = ['bin/shop']

# run the setup
setup(**options)
