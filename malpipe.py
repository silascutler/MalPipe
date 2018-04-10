#!/usr/bin/env python
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

import malpipe

version = 0.1
banner = """
              _   ___ _            
  /\/\   __ _| | / _ (_)_ __   ___ 
 /    \ / _` | |/ /_)/ | '_ \ / _ \\
/ /\/\ \ (_| | / ___/| | |_) |  __/
\/    \/\__,_|_\/    |_| .__/ \___|
                       |_|         
Version: %s 

""" % version


if __name__ == "__main__":
    print banner 
    malpipe.run()

# For Testing, call feeds directly
#    from malpipe.feeds.MalShare import *
#    t = MalShare()
#    t.run()

