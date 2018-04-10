#!/usr/bin/env python
#Description : Tor Feed Module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2017 12 27
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

class TorNodes(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="TorNodes",
            interval = schedule.every().day.at("07:00"),
            description="Feed from Tor nodes and details",
            authors=["Silas Cutler"],
            version="0.2"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.url = "https://torstatus.blutmagie.de/query_export.php/Tor_query_EXPORT.csv"
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True


    # Example
    #    IPredator,LR,61296,47,197.231.221.211,exit1.ipredator.se,443,9030,0,1,1,0,0,1,1,1,1,Tor 0.3.2.10 on FreeBSD,0,0,2014-04-19,CYBERDYNE- LR,37560,255000,None
    def pull_feeds(self):
        indata = get_url(self.url)
        for rnode in indata.split('\n')[1:]: # Loop through each, strip off CSV header
            node = rnode.split(',')
            if len(node) < 22:
                continue
            addr = node[4]
            md = {
                'name': node[0],
                'country': node[1],
                'uptime' : node[3],
                'hostname': node[5],
                'exit' : bool(int(node[9])),
                'version' : node[17],
                'asn': { 
                    'asnname' : node[21],
                    'asn' : node[22],
                }
            }
            self.results.add_ipaddress( addr, md )

    def run(self):
        self.pull_feeds()
        self.process()
        self.export()

        
if (CONFIG['feeds']["TorNodes"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(TorNodes())

