from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine('sqlite:///hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurements
Station = Base.classes.stations

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def welcome():
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
        )

@app.route('/api/v1.0/precipitation')
def precipitation():
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-22').order_by(Measurement.date).all()

    precip_results = []
    
    for _measurement in precip:
        precip_dict = {}
        precip_dict['date'] = Measurement.date
        precip_dict['prcp'] = Measurement.tobs
        precip_results.append(precip_dict)

    return jsonify(precip_results)

@app.route('/api/v1.0/stations')
def stations():
    station_name = session.query(Station.name).all()
    station_list = list(station_name)

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    temp_obs = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-22').order_by(Measurement.date).all()
    temp_list = list(temp_obs)
    
    return jsonify(temp_list)

@app.route('/api/v1.0/<start>')
def start_date(start):
    start_response = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    return jsonify(start_response)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    start_end = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug = True)


