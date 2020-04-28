import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify


#Get Database
engine = create_engine("sqlite:///resources/hawaii.sqlite",echo=False)
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temps/<start><br/>"
        f"/api/v1.0/temps/<start>/<end><br/>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #query for date and prcp for the past 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= query_date).all()
    prcp_dict = list(np.ravel(results))
    

    return  jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station.distinct()).all()
    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    station_id = 'USC00519281' 
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    # Choose the station with the highest number of temperature observations.
    # Query the last 12 months of temperature observation data for this station
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == station_id).\
    filter(Measurement.date >= query_date).all()
    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/temps/<start>")
def calcute_temp_dates(start):
    # try:

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    temp_list = list(np.ravel(results))

    return jsonify(temp_list)


@app.route("/api/v1.0/temps/<start>/<end>")
def dates(start,end):

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    

    temp_list = list(np.ravel(results))

    return jsonify(temp_list)
        
        

if __name__ == "__main__":
    app.run(debug=True)


