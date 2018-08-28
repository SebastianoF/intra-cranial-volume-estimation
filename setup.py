#!/usr/bin/env python

from icv.__init__ import __version__
from setuptools import setup, find_packages


setup(name='intra-cranial-volume-estimation',
      version=__version__,
      description='Intra cranial volume estimation for MRI image. See http://www.nmr.mgh.harvard.edu/~iglesias/pdf/FIFI_2017_pre.pdf ',
      author='sebastiano ferraris',
      author_email='sebastiano.ferraris@gmail.com',
      license='MIT',
      url='https://github.com/SebastianoF/intra-cranial-volume-estimation',
      packages=find_packages(),
     )
