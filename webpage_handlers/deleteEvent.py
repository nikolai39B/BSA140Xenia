# Python libraries
import time

# Utility Classes
from handlerBase import Handler

# Database Models
from eventInfo import EventInfo
import userInfo

class DeleteEventHandler(Handler):
	def renderPage(self, event = '', error='', eventId=''):
		self.render('deleteEvent.html', event=event, error=error, eventId=eventId)

	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Event')
		if not accessAllowed:
			return
			
		eventId = 0
		error = ''
		eventHtml = ''
		try:
			# Find the event in the datastore
			eventId = int(self.request.get("id"))
			event = EventInfo.get_by_id(eventId)
			
			# If the event was not found, raise and exception (to be caught by the proceeding except).
			if event == None:
				raise Exception()
				
			# If the event was found, generate the event html for the event
			else:
				eventHtml = self.getEventsHtml([ event ], addUtilityBar = False)
		except:
			error = 'Error: no event found with the given id (%s). Cannot delete event.' % eventId
		
		self.renderPage(event=eventHtml, error=error, eventId=eventId)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Event')
		if not accessAllowed:
			return
			
		eventId = int(self.request.get("id"))
		try:
			# Find the event in the datastore
			event = EventInfo.get_by_id(eventId)
			
			# If the event was not found, raise and exception (to be caught by the proceeding except).
			if event == None:
				raise Exception()
				
			# If the event was found, delete it and redirect to the main events page
			else:
				EventInfo.delete(event)
				time.sleep(0.2)
				self.redirect('/events')
				return
		except:
			error = 'Error: no event found with the given id (%s). Cannot delete event.' % eventId
			
		self.renderPage(event='', error=error)