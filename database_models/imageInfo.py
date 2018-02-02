# GAE libraries
import webapp2
from google.appengine.ext import db

# Database Models
from eventInfo import EventInfo

# Represents an image
class ImageInfo(db.Model):
	title = db.StringProperty()
	description = db.TextProperty()
	date = db.DateTimeProperty()
	spotlight = db.BooleanProperty(required = True)
	blobKey = db.StringProperty(required = True)
	imageUrl = db.StringProperty(required = True)
	contentType = db.StringProperty(required = True)
	filename = db.StringProperty(required = True)
	eventId = db.StringProperty()
	created = db.DateTimeProperty(required = True)
	
"""
Gets the title, description, date, and event id for a given image. If the image does not have these
fields specified, the function returns the empty string in its place.

	image: the ImageInfo object representing the image
	
returns: string, string, string, int
"""
def getImageDetails(image):
	title = ''
	description = ''
	date = ''
	event = None

	#try:
	# Get the image fields and set to empty string if they are not specified
	title = image.title
	if title == None:
		title = ''
	
	description = image.description
	if description == None:
		description = ''
	
	date = image.date
	if date == None:
		date = ''
		
	if image.eventId != "" and image.eventId != None:
		eventId = int(image.eventId)
		event = EventInfo.get_by_id(eventId)
		#return event
		#if event != None:
		#	eventName = event.name
		
	#except:
	#	pass
		
	return title, description, date, event