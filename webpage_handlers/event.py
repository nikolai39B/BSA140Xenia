# Python libraries
import datetime

# GAE libraries
import urllib

# Utility Classes
from handlerBase import Handler

# Database Models
from eventInfo import EventInfo

class EventHandler(Handler):
	def renderPage(self, eventBlock='', error='', eventId=''):
		self.render('eventPage.html', eventBlock=eventBlock, error=error, eventId=eventId)

	def get(self, resource):
		# Get the event
		eventId = ''
		try:
			eventId = int(str(urllib.unquote(resource)))
		except:
			error = 'Error: no event found with the given id.'
			self.renderPage(error='Error: no event found with the given id.')
			return
			
		event = EventInfo.get_by_id(eventId)
		
		# If the event could not be found, print the error message
		if event == None:
			error = 'Error: no event found with the given id.'
			self.renderPage(error='Error: no event found with the given id.')
			return
		
		# Generate the html for the event
		eventHtml = self.getEventsHtml([ event ], True, -1, 2)
	
		self.renderPage(eventBlock=eventHtml, eventId=eventId)