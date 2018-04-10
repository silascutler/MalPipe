#!/usr/bin/env python
#Description     : Malware Feed Module for VirusTotal
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2018 04 08
#==============================================================================

import os
import sys
sys.path.extend(["../../"])

from malpipe.config import CONFIG
from malpipe.feeds.common import Modules,MalwareFeed,MalwareFeedDescription
from malpipe.utils import get_url, post_url

import schedule
import time
import re
import json

DISABLE=None

class VirusTotal(MalwareFeed):
    def __init__(self):
        md = MalwareFeedDescription(
            module_name="VirusTotal",
            interval = None,
            description="Feed from VirusTotal of Yara hits",
            authors=["Silas Cutler"],
            version="0.2"
        )
        MalwareFeed.__init__(self, md)
        self.parse_settings()

        self.feed_url = "https://www.virustotal.com/intelligence/hunting/notifications-feed/?key=%s"
        self.download_url = "https://www.virustotal.com/vtapi/v2/file/download?apikey=%s&hash=%s"
        self.clear_notifications = "https://www.virustotal.com/intelligence/hunting/delete-notifications/programmatic/?key=%s"


    def parse_settings(self):
        global CONFIG,DISABLE
        try:
            self.api_key = CONFIG['feeds'][self.get_module_name()]['API_KEY']
            self.download_files = CONFIG['feeds'][self.get_module_name()]['DOWNLOAD']
            self.exporters = CONFIG['feeds'][self.get_module_name()]['EXPORTERS']
            self.processors = CONFIG['feeds'][self.get_module_name()]['PROCESSORS']
        except Exception, e:
            print "[%s] Error Loading: %s" % ( self.get_module_name(), e)
            DISABLE = True

    # Create an object that defines each of the notifications from VT
    def parse_metadata(self, vt_notif):
        md = {}
        md['notificaiton_date'] = self.func_to_epoch(vt_notif["date"])
        md['first_seen_date'] = self.func_to_epoch(vt_notif["first_seen"])
        md['last_seen_date'] = self.func_to_epoch(vt_notif["last_seen"])

        md['hashes'] = {}
        md['hashes']['md5'] = vt_notif["md5"]
        md['hashes']['sha1'] = vt_notif["sha1"]
        md['hashes']['sha256'] = vt_notif["sha256"]

        md['yara'] = []
        md['yara'].append(vt_notif["subject"] )
        md['vtyara'] = { 'ruleset': vt_notif["ruleset_name"], 'rule': vt_notif["subject"] }

        return md

    def func_to_epoch(self, str_timestamp):
        format = '%Y-%m-%d %H:%M:%S'
        try:
            return int(time.mktime(time.strptime(str_timestamp, format)))
        except: 
            return int("0000000");

    def pull_feed(self):
        req_user_agent = {'User-agent': 'MalPipe 0.1'}
        vtIDS = []
        notif_feed = get_url( self.feed_url % (self.api_key), req_user_agent )
        if notif_feed == None:
            return False

        try:
            json_notif_feed = json.loads(notif_feed)
        except Exception, e:
            return False

        for vt_notif in json_notif_feed["notifications"]:
            vtIDS.append( int(vt_notif["id"]) )
        post_url( self.clear_notifications % self.api_key, _data=json.dumps(vtIDS))

        for vt_notif in json_notif_feed["notifications"]:
            try:
                if self.download_files:
                    fsample = get_url( self.download_url % (self.api_key, vt_notif["sha256"]), req_user_agent )
                else:
                    fsample = vt_notif["sha256"]
                self.results.add_file( fsample, self.parse_metadata(vt_notif) )
            except KeyError:
                print "[%s] Problem parsing VT feed" % (self.metadata.module_name)
                return False
        return True

    # For threaded feeds, use while loop to keep running
    def run(self):    
        while True:
            if self.pull_feed():
                self.process()
                self.export()

            time.sleep(30)

if (CONFIG['feeds']["VirusTotal"]['ENABLED'] == True and DISABLE is not False):
    Modules.Feeds.append(VirusTotal())

