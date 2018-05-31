#!/usr/bin/env python3
import os
import math
import sys
import glob

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


date_in = input("Please write the date you are looking for. Should be in YYMMDD format.")
hour_in = input("Please write the hours you in are looking for. Should be in HH format.")

dates = date_in.split(",")
hours = hour_in.split(",")

dic_df = {'name':0,'date':0,'hour':0,'avi':0, 'mp4':0, 'scale4':0, 'tagraw':0,'tagmerge':0,'tagclean':0}
for d in dates:
    for h in hours:
        name = d + h + '0000'
        vname= 'C02_' + name
        avifile='/work/rmegret/jreyes/data/videos/avi/*_02_R_'+name+'.avi'
        mpgfile='/work/rmegret/jreyes/data/videos/mp4/C02_'+name+'.mp4'
        scale4file=mpgfile+'.scale4.mp4'

        tagrawfile='/work/rmegret/jreyes/data/rawtags/C02_'+name+'/tagjson/tags_00009.json'
        tagmergefile='/work/rmegret/jreyes/data/mergedtags/tags-C02_'+name+'-0-72100.json'
        tagcleanfile='/work/rmegret/jreyes/data/cleantags/Tags-C02_'+name+'.json'
        
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
            dic_df['mp4'] =  "File exists," + str(file_size(mpgfile))
        else:
            dic_df['mp4'] = '--'
        if (os.path.isfile(tagcleanfile)):
            dic_df['tagclean'] = "File exists," + str(file_size(tagcleanfile))
        else: 
            dic_df['tagclean'] = '--'


print(dic_df)


