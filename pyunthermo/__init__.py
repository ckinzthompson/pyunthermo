"""
pyunthermo - A python wrapper aroung the Golang module unthermo for opening Thermo .Raw files
"""

__description__ = "A python wrapper aroung the Golang module unthermo for opening Thermo .Raw files"
__author__ = "Colin Kinz-Thompson"
__license__ = "Apache-2.0"
__url__ = "https://github.com/ckinzthompson/"
__version__ = "0.1.0"

from .wrapper import load_all_spectra,find_nscans,compile_dylib