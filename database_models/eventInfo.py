# GAE libraries
import webapp2
from google.appengine.ext import db

# Represents an event
class EventInfo(db.Model):
	name = db.StringProperty(required = True)
	description = db.TextProperty(required = True)
	meetLocation = db.StringProperty(required = True)
	outingLocation = db.StringProperty(required = True)
	departureTime = db.DateTimeProperty(required = True)
	returnTime = db.DateTimeProperty(required = True)
	spotlight = db.BooleanProperty(required = True)
	creator = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	

# Still need to get everything to reference this version
"""
Gets the html for the options for a 'select' input tag. The options are generated from the
EventInfo objects stored in the database, and the option id is the EventInfo id.

	defaultEventId: the id of the event that should begin selected
	
returns: string
"""
def getEventOptionsList(defaultEventId=''):
	# Define option tags
	optionTag = '<option value="%s" %s>%s</option>'
	optionTagHtml = ''
	
	# Get all the events
	events = db.GqlQuery("SELECT * FROM EventInfo "
						 "ORDER BY departureTime DESC ")
						 
	for event in events:
		# Get the id and name for each event
		eventId = event.key().id()
		name = event.name
		
		# If the event id is the defaultEventId, make it the default selected option
		selected = ''
		if str(eventId) == str(defaultEventId):
			selected = 'selected="selected"'
		
		# Append the new option the end of the string of options
		optionTagHtml += optionTag % (eventId, selected, name)
		
	# Add a final 'None' option
	optionTagHtml += optionTag % ('', '', 'None')
	
	return optionTagHtml