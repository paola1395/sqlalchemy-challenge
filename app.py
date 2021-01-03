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
        
    <ul>Precipitation Analysis:</ul>
        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
        
    <ul>Station Analysis:</ul>
        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>

    <ul>Temperature Analysis:</ul>
        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>

    <ul>Start Date Analysis:</ul>
        <li><a href="/api/v1.0/2017-07-03">/api/v1.0/2017-07-03</a></li>

    <ul>Start and End Date Analysis:</ul>
        <li><a href="/api/v1.0/2017-07-03/2017-07-09">/api/v1.0/2017-07-03/2017-07-09</a></li>
    </html>
    '''

#/api/v1.0/precipitation; Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary
@app.route(/api/v1.0/precipitation)
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



#/api/v1.0/tobs; Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.




#/api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


if __name__ == "__main__":
    app.run(debug=True)