#!/usr/bin/env python

from distutils.core import setup
import py2exe

setup(name='ediptool',
      version='1.0',
      description='Elite Dangerous IP Tool',
      author='Rob Fisher',
      author_email='robfisher@gmail.com',
      url='https://github.com/RobFisher/ediptool',
	  console=['ediptool.py'],
     )
