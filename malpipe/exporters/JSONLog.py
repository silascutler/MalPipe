#!/usr/bin/env python
#Description : Exporter for saving data to JSON files
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 10
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
import json
from datetime import date

DISABLE=None

class JSONLog(Exporter):
    def __init__(self):
        md = ExportDescription(
            module_name="JSONLog",
            description="Save received files to disk",
            authors=["Silas Cutler"],
            version="0.2",
        )
        Exporter.__init__(self, md)
        self.types = ['files', 'domains', 'ipaddresses', 'urls']
        self.parse_settings()

        #Settings
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.localpath = CONFIG['exporters'][self.get_module_name()]['LOG_PATH']
            self.pretty_print = CONFIG['exporters'][self.get_module_name()]['PRETTY']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    # If path does not exist, create it
    def make_path(self,nPath):
        if not os.path.exists(nPath):
            os.makedirs(nPath)
        
    def save(self, caller_name, eType, indata):
        # Setup output path
        oPath = "%s/%s/%s/" % (self.localpath, caller_name, date.today().strftime("%Y_%m_%d"))
        lPath = "%s%s.json" % (oPath, eType)
        try:
            self.make_path(oPath)
        except Exception, e:
            print "[%s] Failed to make output directory: %s" % (self.get_module_name(), e)
            return False

        # If Existing file, read data in and append
        try:
            if os.path.exists(lPath):
                eFile = open( lPath, 'r')
                oData = json.loads( eFile.read())
                eFile.close()
            else:
                oData = {}                

        except Exception, e:
            print "[%s] Problem setting up log file: %s" % (self.get_module_name(), e)
            return False

        # Read indicators in to oData
        for indicator in indata:
            ioc_key = indicator.value
            oData[ioc_key] = {}

            for m in indicator.metadata.keys():
                oData[ioc_key][m] = indicator.metadata[m]            
        try:
            if self.pretty_print == True:
                oJson = json.dumps(oData, indent=4, sort_keys=True)
            else:
                oJson = json.dumps(oData)

            oFile = open( lPath, 'w')
            oFile.write(oJson)
            oFile.close()
            return True

        except Exception, e:
            print "[%s] Error saving log : %s" % (self.get_module_name(), e)

        return False

    def run(self, callerRef, eType, indata):
        try:
            self.save( callerRef.get_module_name(), eType, indata)
        except Exception, e:
            print "[%s] Error Processing (%s) : %s" % (self.get_module_name(), callerRef.get_module_name(), e)
   
if (CONFIG['exporters']["JSONLog"]['ENABLED'] == True and DISABLE is not False):
    Modules.Exporters.append(JSONLog())

