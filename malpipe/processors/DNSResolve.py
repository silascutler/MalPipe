#!/usr/bin/env python
#Description : DNS resolver processor module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 09
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.processors.common import Modules,Processor,ProcessorDescription 

import time
import dns.resolver

DISABLE=None

class DNSResolver(Processor):
    def __init__(self):
        md = ProcessorDescription(
            module_name="DNSResolver",
            description="Resolve inbound domains",
            authors=["Silas Cutler"],
            version="0.1"
        )
        Processor.__init__(self, md)
        self.types = ['domains']
        self.parse_settings()
        self.dns = dns.resolver.Resolver()
        self.dns.nameservers = self.nameservers
        self.dns.timeout = 2
        self.dns.lifetime = 2

    # Module Settings
    def parse_settings(self):        
        global CONFIG,DISABLE
        try:
            self.nameservers = CONFIG['processors'][self.get_module_name()]['nameservers']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def resolve(self, t_domain):
        try:
            ans = self.dns.query(t_domain.value, 'a')
            return [a.to_text() for a in ans]
        except Exception, e:
            pass

        return None

    def run(self, callerRef, pType, indomains):
        if pType == "domains":
            rResults = []
            for domain_addr in indomains:
                if 'resolve' not in domain_addr.metadata.keys():
                    tResolve = self.resolve( domain_addr )
                    if tResolve:
                        domain_addr.metadata['resolve'] = tResolve
                rResults.append(domain_addr)
        return rResults

if (CONFIG['processors']["DNSResolver"]['ENABLED'] == True and DISABLE is not False):
    Modules.Processors.append(DNSResolver())

