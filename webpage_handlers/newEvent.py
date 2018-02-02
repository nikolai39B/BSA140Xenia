# Python libraries
import datetime
import sys
import re
import time

# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler
import dateTimeParser

# Database Models
from eventInfo import EventInfo
import userInfo

class NewEventHandler(Handler):
	def renderPage(self, name="", spotlight="", departureTime="", returnTime="",
			meetLocation="", outingLocation="", description="", eventId="", error="", editing=False):
		self.render('newEvent.html', name=name, spotlight=spotlight, departureTime=departureTime,
			returnTime=returnTime, meetLocation=meetLocation, outingLocation=outingLocation,
			description=description, eventId=eventId, error=error, editing=editing)

	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Add Event')
		if not accessAllowed:
			return
			
		# Get the event id (used when editing existing events)
		eventId = 0
		try:
			eventId = int(self.request.get("id"))
		except:
			pass
		
		# If there is no id provided, display a blank form
		if eventId == 0:
			self.renderPage()
			return
		
		# If an id was provided, find the corresponding event in the datastore
		event = EventInfo.get_by_id(eventId)
		
		# If there is no corresponding event, display a blank form
		if event == None:
			self.renderPage()
			return
			
		# Set the spotlight checkbox 'checked' attribute
		spotlightText = ''
		if event.spotlight:
			spotlightText = 'checked'
		
		# Dispay the form with the event details already filled in (to simplify editing)
		self.renderPage(event.name, spotlightText,
			dateTimeParser.parseDateTimeToString(event.departureTime), 
			dateTimeParser.parseDateTimeToString(event.returnTime), event.meetLocation,
			event.outingLocation, event.description, eventId=eventId, editing=True)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Add Event')
		if not accessAllowed:
			return
			
		# Get Parameters
		name = self.request.get("name")
		spotlight = self.request.get("spotlight")
		departureTimeStr = self.request.get("departureTime")
		departureTime = dateTimeParser.parseStringToDateTime(departureTimeStr)
		returnTimeStr = self.request.get("returnTime")
		returnTime = dateTimeParser.parseStringToDateTime(returnTimeStr)
		meetLocation = self.request.get("meetLocation")
		outingLocation = self.request.get("outingLocation")
		description = self.request.get("description")
		
		editing = False
		eventId = -1
		try:
			# If teh event exists, set the editing flag to True
			eventId = int(self.request.get("eventId"))
			if EventInfo.get_by_id(eventId) != None:
				editing = True
		except:
			pass
		
		error = ''
		maxLength = 200
		
		# Event must have a name < 200 characters long
		if name == '':
			error += 'Enter an event name.<br>'
		elif len(name) > maxLength:
			error += 'Enter an event name less than 200 characters long.<br>'
			
		# Event must have a departure time
		if departureTime == None:
			error += 'Enter a valid departure time.<br>'
			
		# Event must have a return time
		if returnTime == None:
			error += 'Enter a valid return time.<br>'
			
		# Departure time must be before return time
		if departureTime != None and returnTime != None and departureTime >= returnTime:
			error += 'Departure time must be before return time.<br>'
		
		# Event must have a meet location < 200 characters long
		if meetLocation == '':
			error += 'Enter a meet location.<br>'
		elif len(meetLocation) > maxLength:
			error += 'Enter a meet location less than 200 characters long.<br>'
		
		# Event must have an outing location < 200 characters long
		if outingLocation == '':
			error += 'Enter an outing location.<br>'
		elif len(outingLocation) > maxLength:
			error += 'Enter an outing location less than 200 characters long.<br>'
			
		# Event must have a description
		if description == '':
			error += 'Enter a description of the event.<br>'

		# If there are errors, display them
		if error != '':
			self.renderPage(name, spotlight, departureTimeStr, returnTimeStr, meetLocation, outingLocation,
				description, error=error)
			return
		
		# If there are no errors, store the event and redirect to the events page
		else:
			# Get the current user
			currentUser = self.getCurrentUser()
			currentUser = ('%s %s') % (currentUser.firstName, currentUser.lastName)
			
			# If the eventId corresponds to an event already in the database, update it
			ei = EventInfo.get_by_id(eventId)
			if ei != None:
				ei.name = name
				ei.description = description
				ei.meetLocation = meetLocation
				ei.outingLocation = outingLocation
				ei.departureTime = departureTime
				ei.returnTime = returnTime
				ei.spotlight = (spotlight != '')
				ei.creator = currentUser
			
			# Otherwise, create a new entry
			else:
				ei = EventInfo(name=name, description=description, meetLocation=meetLocation,
					outingLocation=outingLocation, departureTime=departureTime, returnTime=returnTime,
					spotlight=(spotlight != ''), creator=currentUser)
			ei.put()
			
			time.sleep(0.2)
			self.redirect('/events')
			return