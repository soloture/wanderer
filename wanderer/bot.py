from wanderer import db, app
from models import History, Location
from gcdcal import geocoder, gcd, get_geonames
from urlshortener import shorten, expand
import datetime, os, simplejson, urllib2, urllib, json
import twitter

api = twitter.Api(consumer_key='is3JgCTQZcTxC87PsGrI5Q',
                          consumer_secret='VFnHUmfvndxelIpNIaCkpBQqtqeJfFR8tQMW2e0HVK0',
                          access_token_key='741348853-CVJt6XlNS9m8QJtQuHSGyG5GCSXV8TruHvsB1DyH',
                          access_token_secret='kmw4GcUGVEeQKy242k2LTxk5pp7OCkC4elqqMY8VX0')
                          
LATESTFILE_SUG = 'wanderer_latest.txt'
LATESTFILE_RET = 'wanderer_latest_ret.txt'

#Take a suggestion
def take_suggestions():
	if os.path.exists(LATESTFILE_SUG):
		fp = open(LATESTFILE_SUG)
		lastid = fp.read().strip()
		fp.close()
		
		if lastid == '':
			lastid = 0
	else:
		lastid = 0
		
	result = api.GetMentions(since_id = lastid)
	#No mention, no suggestion
	print lastid
	if len(result) == 0:
		print "No mention received"
		return []
	else :
		fp = open(LATESTFILE_SUG, 'w')
		fp.write(str(max([x.id for x in result])))
		fp.close()
		entry = History.query.descending('mongo_id').first()
		for x in result:
			print x.text
		#Somebody already suggested..
		if entry.next_location.name != entry.suggested_location.name :
			print "There already is a suggestion. Fitz is currently headed to "+entry.next_location.name
			return []
		else :
			candidates = {}
			#Walk through all the mentions we got here..
			
			for x in result :
				mention_entry = x.text.split(' ')
				s_user = x.user.screen_name
				#Locations have to be proposed in a form of "Check out ***"
				if mention_entry[1] == 'Check' and mention_entry[2] == 'out':
					s_key = s_user + ":" + ' '.join(mention_entry[3:])
					s_geo = geocoder(' '.join(mention_entry[3:]))
					distance = gcd(entry.next_location.geocode[0], entry.next_location.geocode[1], s_geo[1], s_geo[2])
					candidates[s_key] = distance
			#Got somethin' but no useful words
			if len(candidates) == 0:
				print "Got some words, but no suggestions.."
				return []
			#Got somewhere to go!
			else :
				next_move = min(candidates, key=candidates.get)
				print candidates[candidates.keys()[0]] > candidates[candidates.keys()[1]]
				print next_move		
				l = Location()
				l.name = next_move.split(':')[1]
				l.geocode = geocoder(next_move.split(':')[1])[1:]
				entry.suggested_location = l
				entry.suggested_by = next_move.split(':')[0]
				entry.save()
				user_sug = []
				user_sug.append(next_move.split(':')[0])
				user_sug.append(next_move.split(':')[1])
				return user_sug

				
				
def retweet_geo():
	if os.path.exists(LATESTFILE_RET):
		fp = open(LATESTFILE_RET)
		lastid = fp.read().strip()
		fp.close()
		
		if lastid == '':
			lastid = 0
	else:
		lastid = 0
	
	entry = History.query.descending('mongo_id').first()
	lag = entry.current_location.geocode[0]
	lng = entry.current_location.geocode[1]
	results = api.GetSearch(geocode = (lag,lng,app.config['RADIOUS']),since_id = lastid)
	
	if len(results) == 0:
		print "No tweets around here"
	else:
		for tweet in results[:2]:
			tweet_text = tweet.text
			if len(tweet.text) > 100:
				tweet_text = tweet.txt[:100] + "..."
			retweet = "RT @" + tweet.user.screen_name + " " + tweet_text
			#api.PostUpdate(retweet)
			print tweet.user.screen_name
			print tweet.text
			print tweet.location
			print tweet.created_at
			print "-------------------------------------------------------------------"
		
		fp = open(LATESTFILE_RET, 'w')
		fp.write(str(max([x.id for x in results])))
	fp.close()
		
def news_search():
	entry = History.query.descending('mongo_id').first()
	types = ['locality', 'administrative_area_level_1']
	c_loc_geo = get_geonames(entry.current_location.geocode[0], entry.current_location.geocode[1], types)
	c_loc_name=[]
	for geoname in c_loc_geo:
		c_loc_name.append(geoname['long_name'])
	c_loc = ','.join(c_loc_name)
	
	print c_loc
	query = urllib.urlencode({'q': c_loc})
	url = ('https://ajax.googleapis.com/ajax/services/search/news?v=1.0&%s' % query)
	print url
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	results = simplejson.load(response)
	hits = results['responseData']['results']
	for h in hits[:app.config['NUMBER_OF_NEWS']]:
		title = h['titleNoFormatting']
		print title
		print shorten(h['unescapedUrl'])
		if len(title) > 100:
			title = title[:100] + "..."
		news_tweet = title + " " + shorten(h['unescapedUrl'])
		print news_tweet
		#api.PostUpdate(news_tweet)
	


def twitter_bot():

	#suggestions = take_suggestions()
	#retweet_geo()
	news_search()
	#if len(suggestions) != 0:
	#	api.PostUpdate("Oh, @" + suggestions[0] + " suggested me to go to " + suggestions[1] + "! I am coming for you.")
		
    
    
    
    
    
    
    

