from flask import Flask, render_template
import json
import os
import math
import datetime


app = Flask(__name__)

@app.route('/listres/data')
def getData():
	file = open("/data.txt", "r") 
	table = file.read()

  data = {'recordsTotal': len(table),
  'recordsFiltered': len(table),
  'draw':1,
  'data': table}

  
	return json.dumps(table)

@app.route('/listresview')
def listres():

    table = getData()
    return render_template('datatable.html', table = table) 	




if __name__ == '__main__':
  config_file = 'listres_config.json'
  if (os.path.isfile(config_file)):
    with open(config_file,'r') as fp:
      config = json.load(fp)
  print('CONFIG:')
  print(config)
  app.run(debug=True,port = 8100)