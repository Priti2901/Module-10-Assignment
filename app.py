# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
ase = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    most_recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(last_date[0],'%Y-%M-%D').date()
    one_year_ago = most_recent_date - dt.timedelta(days=365)

precipitation_score = session.query(Measurement.date, Measurement.prcp).\
                      filter(Measurement.date >= one_year_ago).\
                      order_by(Measurement.date).all()
return jsonify(precipitation_score)

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    station_list = session.query(Station.station, Station.name).all()
    session.close()

    station_list_data = [{"station":station, "name":name} for station, name in station_list]
    return jsonify(station_list_data)

@app.route("/api/v1.0/tobs")
station_count = session.query(Measurement.station).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).first()[0]
most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
most_recent_date =  dt.datetime.strptime(last_date[0],'%Y-%M-%D').date()
one_year_ago = most_recent_date - dt.timedelta(days=365)

temperature_obs_data = session.query (Measurement.tobs).\
                       filter(Measurement.station == 'USC00519281').\
                       filter(Measurement.date >= '2016-08-23').all()
temperature_obs_data = [{"date":date, "tobs":tobs} for date, tobs in temperature_obs_data]

return jsonify(temperature_obs_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=none):
    if end:
        tempstats=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <=end).all()

    else:
        tempstats=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

temp_stats_list = [{"TSMIN":tempstats[0], "TSAVG":tempstats[1]},"TSMAX":tempstats[2] for result in tempstats]

return jsonify(temp_stats_list)

if __name__ == '__main__':
    app.run(debug=True)
    

