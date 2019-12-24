# 1. import Flask & sql library
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func, desc, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
# 3. Define what to do when a user hits the index route.
@app.route("/")
def home():
    return(
          "Availabe Routes are<br>"
          "/api/v1.0/precipitation<br>"
          "/api/v1.0/stations<br>"
          "/api/v1.0/tobs<br>"
          "/api/v1.0/2016-11-10<br>"
          "/api/v1.0/2016-11-10/2016-11-18<br>"
          )
#4. Return the JSON representation of  dictionary.

@app.route("/api/v1.0/precipitation")
def percptation():
  session = Session(engine)
  start_date ='2016-11-10'
  end_date = '2016-11-18'
  query_date = dt.date(2016,11,10) - dt.timedelta(days=365)
  last12months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).\
                  filter(Measurement.date <= start_date).all()
  session.close()
  l =[]
  for row in last12months:
    l.append(row._asdict())
  return jsonify(l)


#5. Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def station():
  session = Session(engine)
  station_list = session.query(Station.station, Station.name).all()
  session.close()
  st =[]
  for row in station_list:
    st.append(row._asdict())
  return jsonify(st)


#6. Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobObservation():
  session = Session(engine)
  start_date ='2016-11-10'
  end_date = '2016-11-18'
  query_date = dt.date(2016,11,10) - dt.timedelta(days=365)
  tob_observation = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).\
                    filter(Measurement.date <= start_date).all()
  
  observ = []
  for row in tob_observation:
    observ.append(row._asdict())
  session.close()
  return jsonify(observ)

#7. Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.


@app.route("/api/v1.0/<start>")
def temp_type(start):
  session = Session(engine)
  temp_recorded = session.query(Measurement.date, func.min(Measurement.tobs).label("TMIN"), func.max(Measurement.tobs).label("TMAX"), func.avg(Measurement.tobs).label("TAVG")).\
                  filter(Measurement.date >= start).group_by(Measurement.date).all()
  session.close()
  recorded = []
  for row in temp_recorded:
    recorded.append(row._asdict())
  
  return jsonify(recorded)

@app.route("/api/v1.0/<start>/<end>")
def temp_inc(start, end):
  session = Session(engine)
  tempStartend =  session.query(Measurement.date, func.min(Measurement.tobs).label("TMIN"), func.max(Measurement.tobs).label("TMAX"), func.avg(Measurement.tobs).label("TAVG")).\
                  filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
  tempRecorded = []
  for row in tempStartend:
    tempRecorded.append(row._asdict())
  session.close()
  return jsonify(tempRecorded)
if __name__ == "__main__":
  app.run(debug=True)
