#!/usr/bin/env python
#Description : Malc0de Feed Module 
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

class Malc0deIPList(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="Malc0deIPList",
            interval = schedule.every().day.at("03:00"),
            description="Feed from IP addresses from Malc0de",
            authors=["Silas Cutler"],
            version="0.1"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.url = "http://malc0de.com/bl/IP_Blacklist.txt"
        
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def pull_feed(self):
        indata = get_url(self.url)
        for r_addr in indata.split('\n'):
            if r_addr.startswith("//") or len(r_addr) < 6:
                continue

            addr = r_addr.strip()            
            self.results.add_ipaddress( addr)

    def run(self):
        self.pull_feed()
        self.process()
        self.export()

        
if (CONFIG['feeds']["Malc0deIPList"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(Malc0deIPList())

