# -*- coding: UTF-8 -*-

"""
This file is part of RT1.
(c) 2016- Raphael Quast
For COPYING and LICENSE details, please refer to the LICENSE file
"""

from setuptools import setup
from setuptools import find_packages

install_requires = ["numpy", "sympy", "symengine", "matplotlib"]

def get_packages():
    find_packages(exclude=['contrib', 'docs', 'tests*']),
    return find_packages()


setup(name='rt1',

      version='v0.0.2',

      description='rt1 - bistatic single scattering radiative transfer model',

      packages=get_packages(),
      package_dir={'rt1': 'rt1'},

      author="Raphael Quast",
      author_email='raphael.quast@geo.tuwien.ac.at',
      maintainer='Raphael Quast',
      maintainer_email='raphael.quast@geo.tuwien.ac.at',

      #~ license='APACHE 2',

      url='https://github.com/TUW-GEO/rt1',

      long_description='xxxx',
      install_requires=install_requires,

      keywords=["physics", "radiative transfer"],

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Atmospheric Science',

          # Pick your license as you wish (should match "license" above)
          #~ 'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 3.7'
      ],

      )


