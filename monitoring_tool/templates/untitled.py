#!/usr/bin/env python3
import os
import math
import sys
import glob
import json

def ok(flag, yes='ok', no='NO'):
    return yes if flag else no

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['_B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1000.0:
            return "%3.1f%s" % (num, x)
        num /= 1000.0

config = {
    'paths':{
        'avi':'/work/rmegret/jreyes/data/videos/avi/*_02_R_{name}.avi',
        'mp4':'/work/rmegret/jreyes/data/videos/mp4/C02_{name}.mp4',
        'raw':'/work/rmegret/jreyes/data/rawtags/C02_{name}/tagjson/tags_00009.json',
        'merge':'/work/rmegret/rmegret/tags/{name}/tags-C02_{name}-0-72100.json',
        'clean':'/work/rmegret/rmegret/tags/Tags/Tags-C02_{name}.json'
    }
}

table = []

#avifile For

for filename in os.listdir('/work/rmegret/jreyes/data/videos/avi/'):
    name = filename
    paths = config['paths']
    avifile = paths['avi'].format(name=name)

#mpgfile For

#scale4file For

#rawtags For 

#mergetag For 

#tagclean For 