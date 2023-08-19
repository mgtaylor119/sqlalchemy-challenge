# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').all()

    session.close()

    data_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        data_list.append(precipitation_dict)


    return jsonify(data_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station).all()
    session.close()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(measurement) \
    .filter(measurement.date >= '2016-08-23') \
    .filter(measurement.station == 'USC00519281') \
    .all()
    session.close()

    tobs_list = []
    for row in results:
        tobs_list.append({
        'date': row.date,
        'tobs': row.tobs
    })

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end):
    session = Session(engine)

    temperature_stats = session.query(measurement.date, measurement.tobs) \
                           .filter(measurement.date >= start) \
                           .filter(measurement.date <= end) \
                           .all()
    session.close()

    temp_list = []
    for date_obj in temperature_stats:
        date = date_obj.date
        
        date_stats = session.query(func.min(measurement.tobs),
                                    func.avg(measurement.tobs),
                                    func.max(measurement.tobs)) \
                             .filter(measurement.date == date) \
                             .first()

        tmin, tavg, tmax = date_stats

        temp_list.append({
            'date': date,
            'tmin': tmin,
            'tavg': tavg,
            'tmax': tmax
        })

    return jsonify(temp_list)

app.run(debug=True)

    # sel = [temperature_stats, 
    #    func.min(measurement.tobs), 
    #    func.max(measurement.tobs), 
    #    func.avg(measurement.tobs)]
    
    # temp_list = list(np.ravel(sel))