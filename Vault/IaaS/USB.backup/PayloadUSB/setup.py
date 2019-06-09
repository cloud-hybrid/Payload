from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(
  name = 'PayloadUSB',
  version = '1.0',
  ext_modules = [
    Extension('PayloadUSB', ['PayloadUSB.c'], extra_objects = ["-lusb-1.0"])
  ]
) 