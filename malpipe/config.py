#!/usr/bin/env python
#Description : Configuration loader
#Author      : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date        : 2018 04 07
#==============================================================================

import json

CONFIG = {}

def load_config():
	global CONFIG
	inconfig = open('config.json', 'r').read()
	CONFIG = json.loads(inconfig)

load_config()
