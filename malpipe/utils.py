#!/usr/bin/env python
#Description     : Shared / utility functions for modules
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

import json
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_url( url, headers = None, ret_json=False ):
    _headers = { 'User-Agent': "MalPipe v0.1" }

    if headers:
        _headers.update( headers )

    try:
        r = requests.get(url, headers=_headers)
    except requests.exceptions.Timeout:
        raise("get_urlError","[X] get_page timed out for %s" % url) 
    except requests.exceptions.TooManyRedirects:
        raise("get_urlError", "[X] get_page redirect loop when pulling %s" % url)
    except requests.exceptions.RequestException as e:
        raise("get_urlError", "[X] get_page failed to pull %s" % url)

    if ret_json:
        try:
            return r.json()
        except Exception, e:
            print "[X] get_url failed to convert result to JSON: %s -> %s" % ( url, r.content )
            return None
    return r.content

def post_url( url, headers = None, _data = {}, ret_json=False ):
    _headers = { 'User-Agent': "MalPipe v0.1" }

    if headers:
        _headers.update( headers )

    try:
        r = requests.post(url, data=_data, headers=_headers)
    except requests.exceptions.Timeout:
        print "[X] post_url timed out for %s" % url
        return None
    except requests.exceptions.TooManyRedirects:
        print "[X] post_url redirect loop when pulling %s" % url
        return None
    except requests.exceptions.RequestException as e:
        print "[X] post_url failed to POST to %s" % url
        return None

    if ret_json:
        try:
            return r.json()
        except Exception, e:
            print "[X] post_url failed to convert result to JSON: %s =>  %s" % (url, r.content)
            return None
    return r.content    
