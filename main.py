from flask import Flask, send_file, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from NOAA import *
from NOAAdataView import *
# import json
# from unittest import result
#jsonify, send_file, Response
# import io
# import pandas as pd

app = Flask(__name__, static_folder="")
api = Api(app)
CORS(app)

class status(Resource):    
     def get(self):
         try:
            return {'data': 'Api running OK'}
         except(error): 
            return {'data': error}

class get_station_year_plot (Resource):
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

class get_station_month_plot(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('station', type=str)
        parser.add_argument('month', type=str)
        args = parser.parse_args()
        station, month = args['station'], args['month']

        noaa = NOAAData()
        dfSta = pd.read_csv('data/noaaApt.csv')
        year = '2021'  
        station1 = 'USW00003016'
        noaaDaily = getDailyData(noaa, month, year, station, dfSta)
        fig = showDaily(noaaDaily, station, year, month)

        #result = noaaMonthly.to_json(orient="split")
        #return month
        #return send_file('plotMonWind.png', mimetype='image/png')
        return app.send_static_file("index.html")

class get_parse(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('station', type=str)
        parser.add_argument('month', type=str)
        args = parser.parse_args()
        station = args['station']
        month = args['month']
        return [month, station]

class get_index(Resource):
    def get(self):
        return app.send_static_file("index.html")


api.add_resource(status,'/')
api.add_resource(get_station_year_plot, '/year/<station>')
api.add_resource(get_station_month_plot, '/month')
api.add_resource(get_parse, '/parse')
api.add_resource(get_index, '/index')

if __name__ == '__main__':
    app.run()