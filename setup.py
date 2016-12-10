import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pypower",
    version = "0.0.1",
    author = "Paul Johnson",
    author_email = "paul@johnson.kiwi.nz",
    description = ("Simple module to parse power management information from osx pmset command"),
    license = "BSD",
    keywords = "osx power management pmset",
    url = "http://github.com/pj/pypower",
    packages=['pypower', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
