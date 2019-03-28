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
#cassandra
cluster = Cluster(['cassandra'])
session = cluster.connect()

#Pollen data url
pollen_url_template = "https://api.breezometer.com/pollen/v2/current-conditions?lat={lat}&lon={lng}&key={API_KEY}"


@app.route('/',methods=['GET']) #REST api Get method
def pollen():
    try:
        print("Hit")
        my_latitude = request.args.get('lat','51.52369') #latitude
        my_longitude = request.args.get('lng','-0.036587') #Longitude
        print("longi")
        print(my_longitude)
        print("lati")
        print(my_latitude)

        pollen_url = pollen_url_template.format(lat=my_latitude, lng=my_longitude, API_KEY=app.config['MY_API_KEY'])
        print(pollen_url)
        resp = requests.get(pollen_url)
        data = {}
        error = {'errmsg':'none'}
        if resp.ok:
            json_data= resp.json()

            print(json_data)
        else:
            error['errmsg'] = resp.reason #prints error message
        result = jsonify([json_data,error])
    except Exception as e:
        result = jsonify(error)

    return result


@app.route('/rest',methods=['GET','POST'])
def dbQuerying():
    rows = list(session.execute( "Select * From pollendata.pollenvalue"))
    return jsonify(list(rows)) # result = ""




if __name__ =="__main__":
    app.run(host='0.0.0.0',port=8080)
