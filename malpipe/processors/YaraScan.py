#!/usr/bin/env python
#Description : Yara Scanner Module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 08
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.processors.common import Modules,Processor,ProcessorDescription 

import time
import yara

DISABLE=None

class YaraScan(Processor):
    def __init__(self):
        md = ProcessorDescription(
            module_name="YaraScan",
            description="Scan file objects using Yara Ruleset",
            authors=["Silas Cutler"],
            version="0.1"
        )
        Processor.__init__(self, md)
        self.types = ['files']
        self.parse_settings()

        # Module Settings
        self.scan = yara.compile(filepath=self.yara_rule_path)

    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.yara_rule_path = CONFIG['processors'][self.get_module_name()]['RULES_PATH']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True  

    def yscan(self, fp):
        rMatches = []
        try:
            for r in self.scan.match(data=open(fp, 'rb').read(), timeout = 30):
                rMatches.append(r.rule)
        except Exception, e:
            print "[%s] Exception Yara Scanning file: %s" % (self.metadata.module_name, e)

        return rMatches


    def run(self, callerRef, pType, infiles):
        if pType == "files":
            rResults = []
            for file in infiles:
                if 'yara' not in file.metadata.keys():
                    file.metadata['yara'] = self.yscan( file.tmp_path )
                rResults.append( file )
            return rResults

if (CONFIG['processors']["YaraScan"]['ENABLED'] == True and DISABLE is not False):
    Modules.Processors.append(YaraScan())

