import sys
from setuptools import setup, find_packages

from simshop import __version__

options = {
    'name' : "SimShop",
    'version' : __version__,
    'author':'Tim Weaver',
    'author_email':'tim@rtlcores.com',
    'packages':find_packages(),
    'scripts':['bin/shop.py'],
    'url':'http://pypi.python.org/pypi/SimShop',
    'license':'LICENSE.txt',
    'description':'Easy Verilog simulation',
    'long_description':open('README.txt').read(),
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2app':
    try:
        import py2app
    except ImportError:
        print 'Could not import py2app.  Mac bundle could not be built.'
        sys.exit(0)
    # Mac specific options
    options['app'] = ['bin/shop.py']
    options['options'] = {
        'py2app': {
            'argv_emulation': True
        }
    }

# run the setup
setup(**options)

