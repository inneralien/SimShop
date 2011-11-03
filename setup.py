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
    'long_description':open('docs/intro.rst').read(),
    'classifiers' : [
          'Development Status :: 4 - Beta',
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
    options['options'] = {'py2app': {
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
    options['options'] = {'py2exe': {
           'compressed':1,
           'bundle_files': 2,
           'dist_dir': "dist_win/SimShop_v%s" % __version__
           }}

# run the setup
setup(**options)

# Make the .dmg file
if len(sys.argv) >= 2 and sys.argv[1] == 'py2app':
    import subprocess
    print "Building DMG..."
    subprocess.call(["hdiutil", "create", "-fs", "HFS+", "-srcfolder", "dist/SimShop.app", "-volname", "SimShop", "dist/SimShop_v%s" % __version__])
