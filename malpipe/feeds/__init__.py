#!/usr/bin/env python
#Description     : Initializes feed modules.  Module loading based on design from github.com/bwall/BAMF
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

from os.path import basename, dirname, abspath
from glob import glob
from importlib import import_module


__all__ = [basename(f)[:-3] for f in glob(dirname(abspath(__file__))+"/*.py")]
__all__ = [v for v in __all__ if not v == "__init__"]

for mod in __all__:
	import_module("malpipe.feeds." +  mod)

