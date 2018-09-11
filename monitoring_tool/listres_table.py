#!/usr/bin/env python3
from flask import Flask, render_template
import json
import os
import math
import sys
import glob
import datetime


app = Flask(__name__)


config = {
    'paths':{
        'avi':'/work/rmegret/jreyes/data/videos/avi/*_02_R_{name}.avi',
        'mp4':'/work/rmegret/jreyes/data/videos/mp4/C02_{name}.mp4',
        'raw':'/work/rmegret/jreyes/data/rawtags/C02_{name}/tagjson/tags_00009.json',
        'merge':'/work/rmegret/rmegret/tags/{name}/tags-C02_{name}-0-72100.json',
        'clean':'/work/rmegret/rmegret/tags/Tags/Tags-C02_{name}.json'
    }
}


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

@app.route('/listres/<date>/<hour>')
def listres(date,hour):
    #ate_in = str(input("Please write the date you are looking for. Should be in YYMMDD format."))
    #our_in = str(input("Please write the hours you in are looking for. Should be in HH format."))

    dates = str(date).split(',')
    hours = str(hour).split(',')
    print(dates)
    table = []
    #{'name':0,'date':0,'hour':0,'avi':0, 'mp4':0, 'scale4':0, 'tagraw':0,'tagmerge':0,'tagclean':0}
    for d in dates:
        for h in hours:
            item = {'name':'','date':'','hour':'','avi':'', 'mp4':'', 'scale4':'', 'tagraw':'','tagmerge':'','tagclean':''}
            
            name = str(d[:2])+d[2:4]+d[4:6] + h + '0000'
            vname= 'C02_' + name

            paths = config['paths'] 

            avifile=paths['avi'].format(name=name)
            mpgfile=paths['mp4'].format(name=name)
            scale4file=mpgfile+'.scale4.mp4'
            tagrawfile=paths['raw'].format(name=name)
            tagmergefile=paths['merge'].format(name=name)
            tagcleanfile=paths['clean'].format(name=name)
            
            
            item['name']= name
            item['date']= d
            item['hour'] = h
            item['scale4'] = ok(os.path.isfile(scale4file), 'ok  ','--')
            item['tagraw'] = ok(os.path.isfile(tagrawfile),  'ok  ','--')
            item['tagmerge'] = ok(os.path.isfile(tagmergefile),  'ok ','--')

            avis = glob.glob(avifile)

            if (len(avis)>0):
                if (os.path.isfile(avis[0])):
                    item['avi'] = str(file_size(avifile))
            else:
                item['avi'] = '--'
            if (os.path.isfile(mpgfile)):
                item['mp4'] =  "File exists," + str(file_size(mpgfile))
            else:
                item['mp4'] = '--'
            if (os.path.isfile(tagcleanfile)):
                item['tagclean'] = "File exists," + str(file_size(tagcleanfile))
            else:
                item['tagclean'] = '--'
            table.append(item)
                
    print(table)
    return render_template("table.html", table = table)

if __name__ == '__main__':
  config_file = 'listres_config.json'
  if (os.path.isfile(config_file)):
    with open(config_file,'r') as fp:
      config = json.load(fp)
  print('CONFIG:')
  print(config)
  app.run(debug=True)
