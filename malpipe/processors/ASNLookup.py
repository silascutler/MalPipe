#!/usr/bin/env python
#Description : ASN details processor module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 09
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.processors.common import Modules,Processor,ProcessorDescription 

import time
import socket
import cymruwhois

DISABLE=None

class ASNLookup(Processor):
    def __init__(self):
        md = ProcessorDescription(
            module_name="ASNLookup",
            description="Get ASN details from Cymru whois service",
            authors=["Silas Cutler"],
            version="0.2"
        )
        Processor.__init__(self, md)
        self.types = ['ipaddresses']
        self.parse_settings()

    # Module Settings
    def parse_settings(self):        
        global CONFIG,DISABLE
        try:
            pass
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def asn_lookup(self, t_ip):
        try:
            asnClient = cymruwhois.Client()
            r = asnClient.lookup(t_ip.value)
            return { "number" : r.asn, "name" : r.owner }
        except Exception, e:
            print "[%s] ASN Lookup exception: %s" % (self.metadata.module_name, e)

        return None


    def run(self, callerRef, pType, inaddrs):
        if pType == "ipaddresses":
            rResults = []
            for ip_addr in inaddrs:
                if 'asn' not in ip_addr.metadata.keys():
                    tASN = self.asn_lookup( ip_addr )
                    if tASN:
                        ip_addr.metadata['asn'] = tASN
                rResults.append(ip_addr)
        return rResults


if (CONFIG['processors']["ASNLookup"]['ENABLED'] == True and DISABLE is not False):
    Modules.Processors.append(ASNLookup())

