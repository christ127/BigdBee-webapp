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


date_in = input("Please write the date you are looking for. Should be in YYMMDD format.")
hour_in = input("Please write the hours you in are looking for. Should be in HH format.")

dates = date_in.split(",")
hours = hour_in.split(",")
table = []
for d in dates:
    for h in hours:
        dic_df = {'name':0,'date':0,'hour':0,'avi':0, 'mp4':0, 'scale4':0, 'tagraw':0,'tagmerge':0,'tagclean':0}
        name = d + h + '0000'
        vname= 'C02_' + name
        paths = config['paths'] 

        avifile=paths['avi'].format(name=name)
        mpgfile=paths['mp4'].format(name=name)
        scale4file=mpgfile+'.scale4.mp4'
        tagrawfile=paths['raw'].format(name=name)
        tagmergefile=paths['merge'].format(name=name)
        tagcleanfile=paths['clean'].format(name=name)
        
        dic_df['name']= name
        dic_df['date']= d
        dic_df['hour'] = h 
        dic_df['scale4'] = ok(os.path.isfile(scale4file), 'ok  ','--')
        dic_df['tagraw'] = ok(os.path.isfile(tagrawfile),  'ok  ','--')
        dic_df['tagmerge'] = ok(os.path.isfile(tagmergefile),  'ok ','--')

        avis = glob.glob(avifile)

        if (len(avis)>0):
            if (os.path.isfile(avis[0])):
                dic_df['avi'] = str(file_size(avifile))
        else:
            dic_df['avi'] = '--'
        if (os.path.isfile(mpgfile)):
            dic_df['mp4'] =  "File exists,"+str(file_size(mpgfile))
        else:
            dic_df['mp4'] = '--'
        if (os.path.isfile(tagcleanfile)):
            dic_df['tagclean'] = "File exists," + str(file_size(tagcleanfile))
        else: 
            dic_df['tagclean'] = '--'
        json_dic = json.dumps(dic_df)
        print(json_dic)
        table.append(dic_df)
        

#save the dictionary in a file 
print(table)
table = json.dumps(table)

tfile = open('data.txt','w')
tfile.write(table)
tfile.close()

config_file = 'listres_config.json'
if (os.path.isfile(config_file)):
    with open(config_file,'r') as fp:
        config = json.load(fp)