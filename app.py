#Import Flask and Dependencies
from flask import Flask, jsonify, request
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy.pool import StaticPool

####################################
# Create database
####################################

#Create engine and reflect DataBase 
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)
Base= automap_base()
Base.prepare(engine, reflect=True)

#Save references for each table
Measurement= Base.classes.measurement
Station= Base.classes.station

#Create session
session= Session(engine)

####################################
# Flask Setup
####################################
app= Flask(__name__)

####################################
# Flask Routes
####################################

#Route: "/"; Home page; List all routes that are available
@app.route("/")
def Homepage():
        return '''<html>
    <h1>Surfs up! Welcome to the Hawaii Climate App</h1>
    <h2>Available Routes:<h2>
        
    <ul>Precipitation Data:</ul>
        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
        
    <ul>All Stations:</ul>
        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>

    <ul>Temperatures Observed at the Most Active Station: <br>(within the last year)</ul>
        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>

    <ul>Start Date Analysis:</ul>
        <li><a href="/api/v1.0/2017-07-03">/api/v1.0/2017-07-03</a></li>

    <ul>Start and End Date Analysis:</ul>
        <li><a href="/api/v1.0/2017-07-03/2017-07-09">/api/v1.0/2017-07-03/2017-07-09</a></li>
    </html>
    '''

#/api/v1.0/precipitation; Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago= dt.date(2017,8,23) - dt.timedelta(days=365)
    
    #design query to retrieve last 12 mo. of precipitation data
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date.asc()).all()
    
    #Convert list into dictionary
    precip_data_list=dict(precip_data)
    #Return JSON
    return jsonify(precip_data_list)

#/api/v1.0/stations; Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    all_stations=session.query(Station.station, Station.name).all()

    #Convert into list
    list_stations= list(all_stations)

    #Return JSON
    return jsonify(list_stations)

#/api/v1.0/tobs; Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    year_ago= dt.date(2017,8,23) - dt.timedelta(days=365)
    obs_data= session.query(Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.station =="USC00519281").\
        order_by(Measurement.date).all()

    #Convert into list
    obs_data_list= list(obs_data)
    #Return JSON
    return jsonify(obs_data_list)
    
#/api/v1.0/<start>; calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
@app.route("/api/v1.0/<start>")
def start_date(start):
    start_day= session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    
    #Convert into list
    start_day_list= list(start_day)
    #Return JSON
    return jsonify(start_day_list)

#/api/v1.0/<start>/<end>; calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_end_day= session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    
    #Convert into list
    start_end_list=list(start_end_day)
    #Return JSON
    return jsonify(start_end_list)

if __name__ == "__main__":
    app.run(debug=True)