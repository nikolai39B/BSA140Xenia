# Python libraries
import datetime

# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler

# Database Models
from eventInfo import EventInfo

class EventsCondensedHandler(Handler):
	def renderPage(self, events):
		self.render('eventsCondensed.html', events=events)

	def get(self):
		# Get the upcoming events (soonest first) and generate their html
		events = db.GqlQuery("SELECT * FROM EventInfo "
							 "WHERE returnTime > :1 "
							 "ORDER BY returnTime ASC",
							 datetime.datetime.now())
		events = self.getEventsCondensedHtml(events)
	
		self.renderPage(events=events)
		
	"""
	Generates the html for a list of events
	
		eventList: a list of EventInfo objects from which to generate the html
		addUtilityBar: whether or not to add the 'Edit Event | Delete Event' bar underneath the event
		
	returns: string
	"""
	def getEventsCondensedHtml(self, eventList, addUtilityBar=True):
		eventsHtml = ''
		
		for event in eventList:
			# Adjust the departure time hour so that it is on a 12 hour clock
			departureTimeMeridiem = 'am'
			if event.departureTime.hour > 12:
				event.departureTime -= datetime.timedelta(hours=12)
				departureTimeMeridiem = 'pm'
			if event.departureTime.hour == 0:
				event.departureTime += datetime.timedelta(hours=12)
				
			# Adjust the return time hour so that it is on a 12 hour clock
			returnTimeMeridiem = 'am'
			if event.returnTime.hour > 12:
				event.returnTime -= datetime.timedelta(hours=12)
				returnTimeMeridiem = 'pm'
			if event.returnTime.hour == 0:
				event.returnTime += datetime.timedelta(hours=12)
				
			# Get event id
			eventId = event.key().id()
				
			# Append the new event html the end of the string of events
			eventsHtml += self.renderStr('eventCondensed.html', event=event, 
				departureTimeMeridiem=departureTimeMeridiem, eventId=eventId, addUtilityBar=addUtilityBar)
				
		return eventsHtml