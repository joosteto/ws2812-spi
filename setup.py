#!/usr/bin/env python

from distutils.core import setup

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware',
               'Topic :: System :: Hardware :: Hardware Drivers']

setup(	name		= "ws2812",
	version		= "0.0",
	description	= "Python bindings for WS2812 communication over SPI.MOSI",
	long_description= open('README.md').read() + "\n" + open('CHANGELOG.md').read(),
	author		= "Joost Witteveen",
	author_email	= "joosteto@gmail.com",
	maintainer	= "Joost Witteveen",
	maintainer_email= "joosteto@gmail.com",
	license		= "GPLv2",
	classifiers	= classifiers,
	url		= "http://github.com/joosteto/raspberry_ws2812",
        py_modules      = ['ws2812'],
)
