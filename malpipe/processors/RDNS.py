#!/usr/bin/env python
#Description : RDNS processor module 
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
socket.setdefaulttimeout(10)

DISABLE=None

class RDNS(Processor):
    def __init__(self):
        md = ProcessorDescription(
            module_name="RDNS",
            description="Get RDNS details for IP address",
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
            rdns = socket.gethostbyaddr(t_ip.value)
            if rdns:
                if len(rdns) > 0:
                    return rdns[0]
        except socket.herror:
            return None

        except Exception, e:
            print "[%s] RDNS Lookup exception: %s" % (self.metadata.module_name, e)

        return None


    def run(self, callerRef, pType, inaddrs):
        if pType == "ipaddresses":
            rResults = []
            for ip_addr in inaddrs:
                if 'rdns' not in ip_addr.metadata.keys():
                    tASN = self.asn_lookup( ip_addr )
                    if tASN:
                        ip_addr.metadata['rdns'] = tASN
                rResults.append(ip_addr)
        return rResults


if (CONFIG['processors']["RDNS"]['ENABLED'] == True and DISABLE is not False):
    Modules.Processors.append(RDNS())

