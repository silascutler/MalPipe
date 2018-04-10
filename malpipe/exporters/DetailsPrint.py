#!/usr/bin/env python
#Description : Test Export Module
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2017 12 27
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.exporters.common import Modules,Exporter,ExportDescription 

DISABLE=None


class DetailsPrinter(Exporter):
    def __init__(self):
        md = ExportDescription(
            module_name="DetailsPrinter",
            description="Print Details",
            authors=["Silas Cutler"],
            version="0.1",
        )
        Exporter.__init__(self, md)
        self.types = ['files', 'domains', 'ipaddresses', 'urls']
        self.parse_settings()

        
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.stats_only = CONFIG['exporters'][self.get_module_name()]['STATS_ONLY']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def generic_print(self, indata):
        for f in indata:
            print " + %s" % f.value
            for m in f.metadata.keys():
                print " + + %s - %s" % ( m, f.metadata[m] )

    def run(self, callerRef, eType, results):
        if self.stats_only:
            print "[%s] %s - %s" % ( callerRef.get_module_name(), eType, len(results) )
        else:        
            if eType == 'files':
                self.generic_print( results )
            if eType == 'domains':
                self.generic_print( results )
            if eType == 'ipaddresses':
                self.generic_print( results )
            if eType == 'urls':
                self.generic_print( results )                                
if (CONFIG['exporters']["DetailsPrinter"]['ENABLED'] == True and DISABLE is not False):
    Modules.Exporters.append(DetailsPrinter())

