from setuptools import setup

setup(
    name = "SimShop",
    version = 'v0.13',
    author='Tim Weaver',
    author_email='tim@rtlcores.com',
    packages=['simshop', 'simshop.builders'],
    scripts=['bin/sim.py'],
    url='http://pypi.python.org/pypi/SimShop',
    license='LICENSE.txt',
    description='Easy Verilog simulation',
    long_description=open('README.txt').read(),
)
