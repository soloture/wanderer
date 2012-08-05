import random
from wanderer import db
from wanderer import History, Location
from wanderer import gcd


def move():
    p_entry = History.query.descending('mongo_id').first()
    n_entry = History()
    n_entry = p_entry
    #if the bot is not moving
    if p_entry.status is "stop":
    	print "Fitz Owen is not moving, and.."
    	#if the bot has got a new suggestion, then move move move yo
    	if p_entry.next_location.geocode is not p_entry.suggested_location.geocode:
    		print "there is a suggested destination :" + p_entry.suggested_location.name
    		n_entry.status = "move"
    		n_entry.previous_location = p_entry.next_location
    		n_entry.next_location = p_entry.suggested_location
    		distance = gcd(n_entry.previous_location.geocode[0], n_entry.previous_location.geocode[1], n_entry.next_location.geocode[0], n_entry.next_location.geocode[1])
    		n_entry.distance = distance
    		n_entry.number_of_segments = int(distance / p_entry.speed)
    		print "Now moving towards" + n_entry.next_location.name +"..."
    #if the bot is approaching the destination..
    elif P_entry.status is "move":
    	if p_entry.segment is p_entry.number_of_segments:
    		#then stop, and calibrate the location, reset
    		n_entry.status = "stop"
    		n_entry.current_location = p_entry.next_location
    		n_entry.segment = 1
    	#Okay, now let's move..
    	else:
    		n_entry.current_location.geocode[0] = ((p_entry.next_location.geocode[0] - p_entry.previous_location.geocode[0]) * p_entry.segment) / p_entry.number_of_segments
    		n_entry.current_location.geocode[1] = ((p_entry.next_location.geocode[1] - p_entry.previous_location.geocode[1]) * p_entry.segment) / p_entry.number_of_segments
    		n_entry.segment = p_entry.segment + 1
    
    n_entry.save()
    			
    
    
    
    		

    


def calculate(current,destination):
    #if the bot arrived to the destination
    if current[0] == destination[0] and current[1] == destination[1]:
        return current
    #still moving
    else:
        return current
        
