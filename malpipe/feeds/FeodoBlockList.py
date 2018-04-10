#!/usr/bin/env python
#Description : Feodo Feed Module 
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

class FeodoBlockList(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="FeodoBlockList",
            interval = schedule.every().day.at("02:00"),
            description="Feed from IP addresses from FeodoBlockList",
            authors=["Silas Cutler"],
            version="0.1"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.url = "https://feodotracker.abuse.ch/blocklist/?download=ipblocklist"
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def pull_feeds(self):
        indata = get_url(self.url)
        if ( "# START" in indata and "# END" in indata):
            fList = indata[indata.index("# START"):indata.index("# END")]
            for addr in fList.split('\n'):
                addr = addr.strip()
                if len(addr) > 6:
                    self.results.add_ipaddress( addr )

    def run(self):
        self.pull_feeds()
        self.process()
        self.export()

        
if (CONFIG['feeds']["FeodoBlockList"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(FeodoBlockList())

