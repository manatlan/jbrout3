#!/usr/bin/python3
import os
import sys

from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as inf:
        return inf.read()

setup(
    name='jbrout3',
    version="0.0.1",
    description='Photo collection manager of new generation',
    author=u'manatlan',
    author_email='manatlan@gmail.com',
    url='https://github.com/manatlan/jbrout3',
    long_description=read("README.md"),
    entry_points={
        'console_scripts': [
            'jbrout=jbrout:index',
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License " +
                    "Version 2 only (GPL-V2)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
    ],
    install_requires=['py3exiv2', 'lxml', 'wuy', 'vbuild',"easygui","Pillow"],
)
