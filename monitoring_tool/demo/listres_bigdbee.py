from flask import Flask, render_template
import json
import os
import math
import datetime
from import app




@app.route('/listres/data')
def getData():
    with open('data.txt') as json_file:  
      table = json.load(json_file)

    
    data = {'recordsTotal': len(table),
    'recordsFiltered': len(table),
    'draw':1,
    'data': table}

  
    return json.dumps(data)

@app.route('/listresview')
def listres():

    #table = getData()
    return render_template('datatable_big.html')     




if __name__ == '__main__':
  config_file = 'listres_config.json'
  if (os.path.isfile(config_file)):
    with open(config_file,'r') as fp:
      config = json.load(fp)
  app.run(debug=True,port = 8100)