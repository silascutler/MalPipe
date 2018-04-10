#!/usr/bin/env python
#Description : Bambenek Consulting Feed Module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 07
#==============================================================================

#Required Imports
import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.feeds.common import Modules,MalwareFeed,MalwareFeedDescription
from malpipe.utils import get_url, post_url

import schedule

# Local Imports
import time
import re
import os
import json

DISABLE=None

class BambenekFeeds(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="BambenekFeeds",
            interval = schedule.every().day.at("01:00"),
            description="Amazing set of feeds from Bambenek Consulting",
            authors=["Silas Cutler"],
            version="0.1"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.c2_masterlist_url = "http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt"
        self.c2_domainlist_url = "http://osint.bambenekconsulting.com/feeds/c2-dommasterlist.txt"
        self.dga_list_url = "http://osint.bambenekconsulting.com/feeds/dga-feed.txt"

    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def pull_c2_ips(self):
        indata = get_url(self.dga_list_url)
        for r_addr in indata.split('\n'):
            if r_addr.startswith("#") or "," not in r_addr:
                continue
            addr = r_addr.split(',')
            md = {'note': addr[1]}
            self.results.add_ipaddress( addr[0], md )

    def pull_c2_domains(self):
        indata = get_url(self.dga_list_url)
        for r_addr in indata.split('\n'):
            if r_addr.startswith("#") or "," not in r_addr:
                continue
            addr = r_addr.split(',')
            md = {'note': addr[1]}
            self.results.add_domain( addr[0], md )                   

    def pull_c2_dga(self):
        indata = get_url(self.dga_list_url)
        for r_addr in indata.split('\n'):
            if r_addr.startswith("#") or "," not in r_addr:
                continue
            addr = r_addr.split(',')
            md = {'note': addr[1]}
            self.results.add_domain( addr[0], md )

    def pull_feeds(self):
        self.pull_c2_dga()
        self.pull_c2_domains()
        self.pull_c2_ips()

    def run(self):
        self.pull_feeds()
        self.process()
        self.export()

        
if (CONFIG['feeds']["BambenekFeeds"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(BambenekFeeds())

