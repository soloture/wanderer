import random
from wanderer import db
from models import History, Location
from gcdcal import gcd, geocoder
import datetime, os


def move():
    p_entry = History.query.descending('mongo_id').first()
    n_entry = History()
    n_entry = p_entry
    print p_entry.next_location.geocode[0]
    print p_entry.next_location.geocode[1]
    print p_entry.suggested_location.geocode[0]
    print p_entry.suggested_location.geocode[1],
    print p_entry.suggested_location.geocode[0] == p_entry.next_location.geocode[0]
    #if the bot is not moving
    
   
    if p_entry.status is False:
    	print "Fitz Owen is not moving, and.."
    	#if the bot has got a new suggestion, then move move move yo
    	if p_entry.next_location.geocode != p_entry.suggested_location.geocode:
    		print "there is a suggested destination :" + p_entry.suggested_location.name
    		n_entry.status = True
    		n_entry.previous_location = p_entry.next_location
    		n_entry.next_location = p_entry.suggested_location
    		distance = gcd(n_entry.previous_location.geocode[0], n_entry.previous_location.geocode[1], n_entry.next_location.geocode[0], n_entry.next_location.geocode[1])
    		n_entry.distance = distance
    		n_entry.number_of_segments = int(distance / p_entry.speed)
    		if (distance / p_entry.speed) < 1:
    			n_entry.number_of_segments = 1
    		print "Now moving towards" + n_entry.next_location.name +"..."
    	else :
    		print "okay, not moving"
    #if the bot is approaching the destination..
    elif p_entry.status is True:
    	if p_entry.segment is p_entry.number_of_segments:
    		print "got there!"
    		#then stop, and calibrate the location, reset
    		n_entry.status = False
    		n_entry.current_location = p_entry.next_location
    		n_entry.segment = 1
    	#Okay, now let's move..
    	else:
    		print "moving.."
    		lon = (p_entry.next_location.geocode[0] - p_entry.previous_location.geocode[0]) / p_entry.number_of_segments
    		lat = (p_entry.next_location.geocode[1] - p_entry.previous_location.geocode[1]) / p_entry.number_of_segments
    		xy = (p_entry.current_location.geocode[0]+lon,p_entry.current_location.geocode[1]+lat)
    		n_entry.current_location.geocode = xy
    		n_entry.segment = p_entry.segment + 1
    		print n_entry.segment 
    		print n_entry.number_of_segments
    n_entry.current_time = str(datetime.datetime.now())
    n_entry.save()
    			
    
    
    


    


def calculate(current,destination):
    #if the bot arrived to the destination
    if current[0] == destination[0] and current[1] == destination[1]:
        return current
    #still moving
    else:
        return current
        
