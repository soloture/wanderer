from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
from wanderer import db

class History(db.Document):
    previous_location = db.DocumentField(Location)
    current_location = db.DocumentField(Location)
    suggested_location = db.DocumentField(Location)
    next_location = db.DocumentField(Location,allow_none = True)
    current_time = db.TimeField()
    speed = db.FloatField()
    status = db.StringField()
    distance = db.FloatField()
    segment_index = db.IntField()
    number_of_segments = db.IntField()
    def __str__(self):
        return '%s %s %s' % (self.destination, self.time, self.speed)


class Location(db.Document):
	name = db.StringField()
	geocode = db.GeoField()
    
    

    
