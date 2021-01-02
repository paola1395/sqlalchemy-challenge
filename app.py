#Import Flask and Dependencies
from flask import Flask, jsonify
import numpy as no
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

####################################
# Create database
####################################

#Create engine and reflect DataBase 
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", echo=False)
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



#/Home page; List all routes that are available.




#/api/v1.0/precipitation; Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.




#/api/v1.0/stations; Return a JSON list of stations from the dataset.



#/api/v1.0/tobs; Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.




#/api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.