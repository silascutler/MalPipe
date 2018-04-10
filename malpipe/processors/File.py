#!/usr/bin/env python
#Description : File Type Module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 08
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.processors.common import Modules,Processor,ProcessorDescription 

import time
from subprocess import Popen, PIPE

DISABLE=None


class FileType(Processor):
    def __init__(self):
        md = ProcessorDescription(
            module_name="FileType",
            description="Get type of File",
            authors=["Silas Cutler"],
            version="0.2"
        )
        Processor.__init__(self, md)
        self.types = ['files']
        self.parse_settings()

    # Module Settings
    def parse_settings(self):        
        global CONFIG,DISABLE
        try:
            self.cmd_file_path = CONFIG['processors'][self.get_module_name()]['FILE_PATH']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def fCheck(self, fp):
        try:
            p = Popen([self.cmd_file_path, fp.tmp_path], 
                stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b"input data that is passed to subprocess' stdin")
            if " " in output:
                return output[output.index(' ') + 1: ].strip()
        except Exception, e:
            print "[%s] File CMD exception: %s" % (self.metadata.module_name, e)

        return None

    def run(self, pType, infiles):
        if pType == "files":
            rResults = []
            for file in infiles:
                if 'file_type' not in file.metadata.keys():
                    fType = self.fCheck( file )
                    if fType:
                        file.metadata['file_type'] = fType
                rResults.append( file )
            return rResults

if (CONFIG['processors']["FileType"]['ENABLED'] == True and DISABLE is not False):
    Modules.Processors.append(FileType())

