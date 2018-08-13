from flask import Flask
from flask import request, render_template
from mongo_datatables import DataTables
from flask_pymongo import PyMongo
import json
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'connect'
app.config["MONGO_URI"] = "mongodb://localhost:27017/Bigdbee"
mongo = PyMongo(app)

#Adding data to the MongoDB database

def clear_database():

	mongo.db.annotations.remove()
	mongo.db.videos.remove()
	return

@app.route('/add_annotations')
def add_annotations():

	clear_database()
	ann = mongo.db.annotations

	filt = ann.find_one({"Name":"06241712_1_3i27vfl5",
		"ID":"3i27vfl5",
		"video_id":"2q23asdg1",
		"date_created":"082417",
		"date":"170624",
		"hour":"12",
		"user_id":"1",
		"data":{},
		"Notes":{"text":"ok"}})

	if filt:
		return 'annotation already in database'


	ann.insert_one({"Name":"06241712_1_3i27vfl5",
		"ID":"3i27vfl5",
		"video_id":"2q23asdg1",
		"date_created":"170824",
		"date":"170624",
		"hour":"12",
		"user_id":"1",
		"data":{"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}}
,
		"Notes":{"text":"ok"}})
	ann.insert_one({"Name":"062417110000_1_1223443",
		"ID":"1223443",
		"video_id":"8r12djl5",
		"date_created":"170824",
		"date":"170624",
		"hour":"11",
		"user_id":"1",
		"data":{"menu": {
  "id": "file",
  "value": "File",
  "popup": {
    "menuitem": [
      {"value": "New", "onclick": "CreateNewDoc()"},
      {"value": "Open", "onclick": "OpenDoc()"},
      {"value": "Close", "onclick": "CloseDoc()"}
    ]
  }
}}
,
		"Notes":{"text":"ok"}})


	return 'Annotations added'

#better date format.
#hour and month can be extracted if date is defined format.
#is name ok? 
@app.route('/add_videos')
def add_videos():
	clear_database()
	vid = mongo.db.videos
	vid.insert_one({
	"Name":"062417120000",
	"ID":"2q23asdg1" ,
	"Date":"170624",
	"Path":"work/rmegret/data/videos/062417120000",
	"month":"06", 
	"Hour": "12",              
	"status":{
	"tag_raw":"yes",
	"tag_clean":"yes",
	"tag_merge":"yes"}})
	vid.insert_one({
	"Name":"062417110000",
	"ID":"8r12djl5" ,
	"Date":"170624",
	"Path":"work/rmegret/data/videos/062417110000",
	"month":"06", 
	"Hour":"11",              
	"status":{
	"tag_raw":"yes",
	"tag_clean":"yes",
	"tag_merge":"yes"}})

		
	return 'Videos Added'

@app.route('/loadJSON/<myid>')
def load_json(myid):
	loadj = mongo.db.annotations.find_one({"ID": myid })
	retjson = loadj['data']
	return str(retjson)

@app.route('/mongo/<collection>')
def api_db(collection):
    request_args = json.loads(request.values.get("args"))
    results = DataTables(mongo, collection, request_args).get_rows()
    print(results)
    return json.dumps(results)

#html code will call the /mongo/annotation route to get the data 
@app.route('/annotations')
def table_view():
    return render_template('table_view2.html')

@app.route('/videos')
def video_view():
	return render_template('video_view.html')

#@app.route('/annotationfile')
#def displayfile(path):
#	

if __name__ == '__main__':
	app.run(debug = True)