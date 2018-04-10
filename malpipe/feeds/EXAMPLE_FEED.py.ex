#!/usr/bin/env python
#Description : Example Feed Module 
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 08
#==============================================================================

#Required Imports
import os
import sys
sys.path.extend(["../../"])

from malpipe.config import config                                           # Used to pass configuration details
from malpipe.feeds.common import Modules,MalwareFeed,MalwareFeedDescription 
from malpipe.utils import get_url, post_url                                 # Common functions that multiple modules
                                                                            #   may use 
import schedule

# Local Imports
import os
import json

DISABLE=None

class MyCoolMalwareFeed(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="MyCoolMalwareFeed",						# Name for the module
            interval = schedule.every().day.at("02:12"),		# Scheduled time to run. Set to None in order
                                                                #    have module run continously
            description="Feed Example",  # Description.
            authors=["Silas Cutler"],                           # Author for tracking
            version="0.1"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        # Custom module settings.  URL paths, static things.
        self.url = "http://MyCoolMalwareFeed.local/FeedPath"

    def parse_settings(self):
        global CONFIG,DISABLE
        try:
        	# these two modules are required. 
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
        	# Fail if the settings fail to parse
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    def pull_feed(self):
        indata = get_url(self.url)
        for r_addr in indata.split('\n'):
            if r_addr.startswith("//") or len(r_addr) < 6:
                continue

            addr = r_addr.strip()
            url = r_addr[1]
            domain = r_addr[2]
            file = r_addr[3]

            # Add captured indicators
            self.results.add_ipaddress( addr) # Add IP address
            self.results.add_domain( domain ) # Add Domain/DNS Address
            self.results.add_url( url ) # Add URL
            self.results.add_file( r_file ) # Pass str() containing sample


    # This function may move up to the base class.  In general, Pull -> Process -> Export
    def run(self):
        self.pull_feed()
        self.process()
        self.export()


# Controls adding feed to list of registered.  If feed is marked disabled, will prevent from use
if (CONFIG['feeds']["MyCoolMalwareFeed"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(MyCoolMalwareFeed())

