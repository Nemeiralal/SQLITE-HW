import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """API Routes."""
    return"""<html>
	<center>
    <h2>List of Honolulu, Hawaii APIs </h2>
    <ul>
    <br>
    <li>
	List(in JSON) of stations: 
    <br>
    <a href="/API/v1/Different_Stations">/API/v1/Different Stations</a>
	</li>
    <br>
    <li>
    List of Precipitations during Previous year:
    <br>
    <a href="/API/v1/Precipitation">/API/v1/Precipitation</a>
    </li>
    <br>
    <li>
    List(in JSON) of Temperature Observations (tobs) for the last year:
    <br>
    <a href="/API/v1/temp_obsn">/API/v1/Temp Observaation</a>
    </li>
    <br>
    <li>
    List(in JSON) of tmin, tmax, tavg for the dates greater than or equal to the date provided:
    <br>Simply replace &ltstart&gt with any valid date in Year-Month-Day format.
    <br>
    <a href="/API/v1/2017-01-01">/API/v1/2017-01-01</a>
    </li>
    <br>
    <li>
    List(in JSON) of tmin, tmax, tavg for the dates in domain of TO date and FROM date both inclusive:
    <br>
    Replace &ltstart&gt and &ltend&gt with any date in Year-Month-Day format. 
    <br>
    <br>
    <a href="/API/v1/2017-01-01/2017-01-07">/API/v1/2017-01-01/2017-01-07</a>
    </li>
    <br>
    </ul>
	</center>
    </html>
    """


@app.route("/API/v1/Precipitation")
def Precipitation():
    
    date_Max = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
    date_Max = date_Max[0]
    last_Year_Date = dt.datetime.strptime(date_Max, "%Y-%m-%d") - dt.timedelta(days=366)
    Precipitation_Result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_Year_Date).all()
    Precipitation_dict = dict(Precipitation_Result)
    return jsonify(Precipitation_dict)

@app.route("/API/v1/<start>/<end>")
def start_end(start=None, end=None):
    data_between_two_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    data_between_two_dates_list=list(data_between_two_dates)
    return jsonify(data_between_two_dates_list)

@app.route("/API/v1/Different_Stations")
def Different_Stations(): 
    stations =  session.query(Measurement.station).group_by(Measurement.station).all()
    stations_List = list(np.ravel(stations))
    return jsonify(stations_List)

@app.route("/API/v1/<start>")
def start(start=None):
    start_From = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_From_list=list(start_From)
    return jsonify(start_From_list)

@app.route("/API/v1/temp_obsn")
def tobs(): 
    date_Max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_Max = date_Max[0]
    last_Year_Date = dt.datetime.strptime(date_Max, "%Y-%m-%d") - dt.timedelta(days=366)
    temp_Obsn_Res = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_Year_Date).all()
    temp_Obsn_list = list(temp_Obsn_Res)
    return jsonify(temp_Obsn_list)   


if __name__ == '__main__':
    app.run(debug=True)