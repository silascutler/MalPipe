#!/usr/bin/env python
#Description : NoThink Feed Module 
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

class NoThinkIPFeeds(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="NoThinkIPFeeds",
            interval = schedule.every().day.at("05:00"),
            description="IP Honeypot feeds from NoThinkIPFeeds",
            authors=["Silas Cutler"],
            version="0.1"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.smtp_url = "http://www.nothink.org/blacklist/blacklist_snmp_day.txt"
        self.ssh_url  = "http://www.nothink.org/blacklist/blacklist_ssh_day.txt"
        self.telnet_url = "http://www.nothink.org/blacklist/blacklist_telnet_day.txt"

    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def pull_smtp_feed(self):
        indata = get_url(self.smtp_url)
        if "Provided by nothink.org" not in indata:
            return False
        for r_addr in indata.split('\n'):
            if r_addr.startswith("#") or len(r_addr) < 6:
                continue
            md = {'note': "SMTP Scanner"}
            r_addr = r_addr.strip()
            self.results.add_ipaddress( r_addr, md )
    def pull_ssh_feed(self):
        indata = get_url(self.ssh_url)
        if "Provided by nothink.org" not in indata:
            return False
        for r_addr in indata.split('\n'):
            if r_addr.startswith("#") or len(r_addr) < 6:
                continue
            md = {'note': "SSH Scanner"}
            r_addr = r_addr.strip()            
            self.results.add_ipaddress( r_addr, md )
    def pull_telnet_feed(self):
        indata = get_url(self.telnet_url)
        if "Provided by nothink.org" not in indata:
            return False
        for r_addr in indata.split('\n'):
            if r_addr.startswith("#") or len(r_addr) < 6:
                continue
            md = {'note': "Telnet Scanner"}
            r_addr = r_addr.strip()            
            self.results.add_ipaddress( r_addr, md )

    def pull_feeds(self):
        self.pull_smtp_feed()
        self.pull_ssh_feed()
        self.pull_telnet_feed()

    def run(self):
        self.pull_feeds()
        self.process()
        self.export()

        
if (CONFIG['feeds']["NoThinkIPFeeds"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(NoThinkIPFeeds())

