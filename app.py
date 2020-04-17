from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, desc

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to the home page! Your options for navigation are as follows: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    result = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    prcp_list = []

    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations(): 
    session = Session(engine)
    st_result = session.query(Station.station,Station.name).all()
    session.close()

    stations_list = []

    for st in st_result:
        st_dict = {}
        st_dict["station"] = st
        stations_list.append(st)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    temp_result = session.query(Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.station == 'USC00519281').all()
    session.close()

    temp_list = []

    for temp in temp_result:
        temp_dict = {}
        temp_dict["Temperature"] = temp
        temp_list.append(temp)




if __name__ == "__main__":
    app.run(debug=True)