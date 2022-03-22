import json
from unittest import result
from flask import Flask, jsonify, send_file, Response
from NOAA import *
from NOAAdataView import *
import io
import pandas as pd
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(app)

class status(Resource):    
     def get(self):
         try:
            return {'data': 'Api running'}
         except(error): 
            return {'data': error}

class get_station (Resource):
    def get(self, station: str):
        noaa = NOAAData()
        dfSta = pd.read_csv('data/noaaApt.csv')
        # Fetch monthly summary data and show plots
        month = 'JAN'
        year = '2021'    
        noaaMonthly = getMonthlyNormalsData(noaa, month, year, station, dfSta)
        fig = showMonthlyNormals(noaaMonthly, month, year, station, dfSta)
        result = noaaMonthly.to_json(orient="split")
        return send_file('plot.png', mimetype='image/png')

api.add_resource(status,'/')
api.add_resource(get_station, '/station/<station>')

if __name__ == '__main__':
    app.run()