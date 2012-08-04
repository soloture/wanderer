from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
from wanderer import db

class History(db.Document):
    previous_location = db.GeoField()
    current_location = db.GeoField()
    next_location = db.GeoField(allow_none=True)
    current_time = db.TimeField()
    speed = db.FloatField()
    def __str__(self):
        return '%s %s %s' % (self.destination, self.time, self.speed)
    
    

    