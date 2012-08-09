from flask import Flask, request, session, g, redirect, url_for, render_template, flash, abort
from coordinate import move, calculate
from wanderer import app
from models import History, Location
from db_init import init_db
from gcdcal import geocoder, gcd
from bot import twitter_bot, take_suggestions
from flickr import flickr
import datetime
import random

lat = random.triangular(0,90)
log = random.triangular(0,90)
current = []
destination = []
current.append(lat)
current.append(log)
destination.append(lat)
destination.append(log)


@app.route('/')
def main():
    entry = History.query.descending('mongo_id').first()
    print entry.current_location.geocode
    return render_template('index.html',entry = entry)
    
@app.route('/move')
def do_move():
	#try:
	move()
	return "moving.."
	#except IOError:
	#	print "I/O error"
	#	return "I/O error"
	#except :
	#	print "unknown error"
	#	return "unknown error"

@app.route('/initdb')
def init():
	init_db()
	return "database initialized"

@app.route('/resetdb')
def reset():
	all_db = History.query.all()
	for i in all_db:
		single_entry = History.query.first()
		single_entry.remove()
	all_db = History.query.all()
	print all_db
	return "database reset"

@app.route('/suggest')
def suggest():
	entry = History.query.descending('mongo_id').first()
	suggested_point = app.config['SUGGESTED_POINT']
	geocode = geocoder(suggested_point)
	location = Location()
	location.name = geocode[0]
	location.geocode = (geocode[1],geocode[2])
	entry.suggested_location = location
	entry.save()
	return suggested_point + " suggested!"

@app.route('/twitter')
def tweet():
	twitter_bot()
	return "tweeted!"


	
	
    

if __name__ == '__main__':
    app.run(debug=True)
