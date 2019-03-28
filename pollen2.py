#import plotly.graph_objs as go
#from plotly.utils import PlotlyJSONEncoder
from flask import Flask, request, jsonify
import json
import requests
import time
#from pprint import pprint
from json2html import *
from cassandra.cluster import Cluster
#import requests_cache

#requests_cache.install_cache('air_api_cache',backend='sqlite',expire_after=36000)
app = Flask(__name__,instance_relative_config=True)
# app.config.from_object('config')
app.config.from_pyfile('config.py')

cluster = Cluster(['cassandra'])
session = cluster.connect()

#insert_data = session.prepare("INSERT INTO pollendata.pollenvalue(Time,Grass,Tree,Weed) VALUES(?,?,?,?)")   #Grass,Tree,Weed is true or false
#air_url_template = "https://api.breezometer.com/air-quality/v2/historical/hourly?lat={lat}&lon={lng}&key={API_KEY}&start_datetime={start}&end_datetime={end}"
pollen_url_template = "https://api.breezometer.com/pollen/v2/current-conditions?lat={lat}&lon={lng}&key={API_KEY}"

#MY_API_KEY = '97cf2825e3ac448784bbff6434f2cadf'

@app.route('/',methods=['GET'])
def pollen():
    try:
        print("Hit")
        my_latitude = request.args.get('lat','51.52369')
        my_longitude = request.args.get('lng','-0.036587')
        print("longi")
        print(my_longitude)
        print("lati")
        print(my_latitude)
        #my_start = request.args.get('start','2019-03-14T07:00:00Z')
        #my_end = request.args.get('end','2019-03-15T07:00:00Z')
        pollen_url = pollen_url_template.format(lat=my_latitude, lng=my_longitude, API_KEY=app.config['MY_API_KEY'])
        print(pollen_url)
        resp = requests.get(pollen_url)
        data = {}
        error = {'errmsg':'none'}
        if resp.ok:
            json_data= resp.json()
            # grass = json_data['data']['types']['grass']['in_season']
            # weed = json_data['data']['types']['weed']['in_season']
            # tree = json_data['data']['types']['tree']['in_season']
            # data['grass'] = grass
            print(json_data)
        else:
            error['errmsg'] = resp.reason
        result = jsonify([json_data,error])
    except Exception as e:
        result = jsonify(error)
#    session.execute(insert_data,[time.time(),grass, tree, weed])

#return json2html.convert(resp.json())
    return result


@app.route('/rest',methods=['GET','POST'])
def dbQuerying():
    rows = list(session.execute( "Select * From pollendata.pollenvalue"))
    return jsonify(list(rows)) # result = ""
    #for e in rows:
        #result = result + str(e.grass)
    #return(result)



if __name__ =="__main__":
    app.run(host='0.0.0.0',port=8080)

