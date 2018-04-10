#!/usr/bin/env python
#Description : Test Export Module
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 08
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.exporters.common import Modules,Exporter,ExportDescription 
from malpipe.utils import get_url, post_url

import json
import copy

DISABLE=None

class GenericWebStorage(Exporter):
    def __init__(self):
        md = ExportDescription(
            module_name="GenericWebStorage",
            description="Log data to IOC storage system via HTTP",
            authors=["Silas Cutler"],
            version="0.1",
        )
        Exporter.__init__(self, md)
        self.types = ['files', 'domains', 'ipaddresses']
        self.parse_settings()

    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.url_path = CONFIG['exporters'][self.get_module_name()]['URL_PATH']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True


    def file_submit(self, indata):
        for f in indata:
            tdetails = copy.deepcopy(f.metadata)
            desc = '%s' % f.source
            if "yara" in tdetails.keys():
                desc += " - %s" % json.dumps( tdetails['yara'])
            details = { 
                "md5": tdetails['hashes']['md5'], 
                "sha1": tdetails['hashes']['sha1'], 
                "sha256": tdetails['hashes']['sha256'],
                "source": f.source
            }
            del( tdetails['hashes'] )
            details = dict( details.items() + tdetails.items() )
            res = self.post_ioc( details['sha256'], 'file', desc, details  )

    def generic_submit(self, eType, indata):
        for f in indata:
            desc = 'Source: %s' % f.source
            details = copy.deepcopy(f.metadata)
            details['source'] = f.source

            res = self.post_ioc( f.value, eType, desc, details  )

    def post_ioc(self, name, rtype, note="", details={}):
        print "[%s] Saving %s" % (self.get_module_name(), name)

        payload = {
            'indicator': name,
            'type': rtype,
            'note': note,
            'details': json.dumps( details )
        }    
        try:
            r = post_url(self.url_path + "/add", _data=payload, ret_json=True)
            return r
        except Exception, e:
            print "[+] GenericWebStorage Add problem: %s" % e
            return None    


    def run(self, callerRef, eType, results):
        if eType == 'files':
            self.file_submit( results )

        if eType == 'domains':
            self.generic_submit( 'domain', results )


        if eType == 'ipaddresses':
            self.generic_submit( 'ipaddress', results )


if (CONFIG['exporters']["GenericWebStorage"]['ENABLED'] == True and DISABLE is not False):
    Modules.Exporters.append(GenericWebStorage())

