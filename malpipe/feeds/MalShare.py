#!/usr/bin/env python
#Description : Malware Feed Module for MalShare
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 08
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

class MalShare(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="MalShare",
            interval = schedule.every().day.at("04:00"),
            description="Feed from MalShare of Daily files",
            authors=["Silas Cutler"],
            version="0.2"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.url_daily_list = "https://malshare.com/daily/malshare.current.sha256.txt"
        self.url_download = "https://malshare.com/api.php?api_key=%s&action=getfile&hash=%s"
        self.url_sources = "https://malshare.com/api.php?api_key=%s&action=getsources"

        # Settings
    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.api_key = CONFIG['feeds'][self.get_module_name()]['API_KEY']
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True


    def get_hash_list(self):
        return get_url( self.url_daily_list )

    def get_file_feed(self):
        hash_list = self.get_hash_list()
        if hash_list:
            for thash in hash_list.split('\n'):
                uFile = self.url_download % ( self.api_key, thash )
                fData = get_url( uFile )
                self.results.add_file( fData )

    def get_url_feed(self):
        url_list = []
        turl = self.url_sources % ( self.api_key )

        fData = get_url( turl, ret_json=True )
        for url in fData:
            self.results.add_url(url)

    def pull_feeds(self):
        self.get_url_feed()
        self.get_file_feed()

    def run(self):
        self.pull_feeds()
        self.process()
        self.export()

        
if (CONFIG['feeds']["MalShare"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(MalShare())

