#!/usr/bin/env python
# encoding: utf-8
import json
from unittest import result
from flask import Flask, jsonify, send_file, Response
from NOAA import *
from NOAAdataView import *
import io
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/<station>', methods=['GET'])
def get_station(station: str):
    noaa = NOAAData()
    dfSta = pd.read_csv('data/noaaApt.csv')
    # Fetch monthly summary data and show plots
    month = 'JAN'
    year = '2021'    
    noaaMonthly = getMonthlyNormalsData(noaa, month, year, station, dfSta)
    fig = showMonthlyNormals(noaaMonthly, month, year, station, dfSta)
    result = noaaMonthly.to_json(orient="split")
    return send_file('plot.png', mimetype='image/png')



app.run()