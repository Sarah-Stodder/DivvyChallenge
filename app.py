from flask import Flask,  request, make_response, g,  render_template,  jsonify
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
import os
import csv
import json
import datetime
import requests




class Config():
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

app = Flask(__name__)
app.config.from_object(Config)
db= SQLAlchemy(app)
migrate=Migrate(app,db)




class Trips(db.Model):
    trip_id = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    bikeid = db.Column(db.Integer)
    from_station_id = db.Column(db.Integer)
    from_station_name = db.Column(db.String)
    to_station_id = db.Column(db.Integer)
    to_station_name = db.Column(db.String)
    usertype	= db.Column(db.String)
    gender = db.Column(db.String)
    birthdate = db.Column(db.Date)
    trip_duration = db.Column(db.Integer)
    
    def from_dict(self, data):
        self.trip_id = data['trip_id'],
        self.starttime = data['starttime'],
        self.stoptime = data['stoptime'],
        self.bikeid = data['bikeid'],
        self.from_station_id = data['from_station_id'],
        self.from_station_name = data['from_station_name'],
        self.to_station_id = data['to_station_id'],
        self.to_station_name = data['to_station_name'],
        self.usertype = data['usertype'],
        self.gender = data['gender'],
        self.birthdate = data['bi render_templaterthdate'],
        self.trip_duration = data['trip_duration']
    
    def to_dict(self):
        return {"trip_id ": self.trip_id
        , "starttime":self.starttime," stoptime":self.stoptime,
        "bikeid":self. bikeid,"from_station_id":self.from_station_id, 
        "from_station_name":self.from_station_name,"to_station_id":self.to_station_id, 
        "to_station_name":self.to_station_name,"usertype":self.usertype,"genders":self.gender,
        "birthdate":self.birthdate, "trip_duration":self.trip_duration}

@app.route("/home")
def home():
    return render_template("home.html")

@app.get('/trips')                                     
def get_trips():
    trips = Trips.query.all()
    return make_response(json.dumps([trip.to_dict() for trip in trips]))

@app.get('/trips/<start>/<stop>')
def get_average_trip_time(start, stop):
   avtrips = Trips.query.filter(Trips.starttime==start, Trips.stoptime==stop).all()
   if not avtrips :
    return make_response(f"Invalid selected trip")
   else:
    newlist = []
    newlist.append(avtrips[0].trip_duration)
    return make_response(f' Average trip time: {newlist[0]} minutes')
 

@app.get('/trips/<id>/<start>/<stop>')
def get_bike_trips(id,start,stop):
    biketrip=Trips.query.filter( Trips.bikeid==id, Trips.starttime==start, Trips.stoptime==stop).all()
    if not biketrip :
        return make_response(f"Invalid selected trip")
    else:
        avbiketrip = 0
        for trip in biketrip:
            avbiketrip +=1
        return make_response(f"Average Bike trips: {avbiketrip}")





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)