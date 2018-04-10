#!/usr/bin/env python
#Description : Exporter for saving files to specific paths
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 07
#==============================================================================

#Required Imports
import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.exporters.common import Modules,Exporter,ExportDescription 
from malpipe.utils import get_url, post_url

#Module Imports
import os

DISABLE=None

class LocalFileStorage(Exporter):
    def __init__(self):
        md = ExportDescription(
            module_name="LocalFileStorage",
            description="Save received files to disk",
            authors=["Silas Cutler"],
            version="0.2",
        )
        Exporter.__init__(self, md)
        self.types = ['files']
        self.parse_settings()

        #Settings
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.localPath = CONFIG['exporters'][self.get_module_name()]['FILE_PATH']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def make_path(self,nPath):
        if not os.path.exists(nPath):
            os.makedirs(nPath)
        
    def save(self, _File):
        tHash = _File.value
        oPath = "%s/%s/%s/%s/" % (self.localPath, tHash[0:3], tHash[3:6], tHash[6:9])
        self.make_path(oPath)

        try:
            os.rename(_File.tmp_path, oPath + tHash)
        except Exception, e:
            print "[%s] Error saving file (%s) : %s" % (self.get_module_name(), tHash, e)

    def run(self, callerRef, eType, infiles):
        if eType == "files":
            for file in infiles:
                self.save(file)


                    
if (CONFIG['exporters']["LocalFileStorage"]['ENABLED'] == True and DISABLE is not False):
    Modules.Exporters.append(LocalFileStorage())

