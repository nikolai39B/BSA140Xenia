# Python libraries
import datetime

# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler

# Database Models
from eventInfo import EventInfo

class EventsHandler(Handler):
	def renderPage(self, spotlightEvents, upcomingEvents, pastEvents, showAllButton=True):
		self.render('events.html', spotlightEvents=spotlightEvents, upcomingEvents=upcomingEvents,
		pastEvents=pastEvents, showAllButton=showAllButton)

	def get(self):
		# Get the spotlight events and generate their html
		spotlightEvents = db.GqlQuery("SELECT * FROM EventInfo "
									  "WHERE spotlight = True "
									  "ORDER BY departureTime DESC")
		spotlightEvents = self.getEventsHtml(spotlightEvents)
		spotlightEvents += '<br><br>'
	
		# Get the upcoming events (soonest first) and generate their html
		upcomingEvents = db.GqlQuery("SELECT * FROM EventInfo "
								     "WHERE returnTime > :1 "
									 "ORDER BY returnTime ASC",
									 datetime.datetime.now())
		upcomingEvents = self.getEventsHtml(upcomingEvents)
		upcomingEvents += '<br><br>'
	
		# Get the 4 most recent (or all of them if the flag is set) past events (most recent first) 
		# and generate their html
		allPastEvents = self.request.get("all")
		showAllButton = allPastEvents != 'y'
		pastEvents = db.GqlQuery("SELECT * FROM EventInfo "
								   "WHERE returnTime <= :1 "
								   "ORDER BY returnTime DESC "
								   "%s" % ("LIMIT 4" if showAllButton else ''),
								   datetime.datetime.now())
		pastEvents = self.getEventsHtml(pastEvents)
	
		self.renderPage(spotlightEvents=spotlightEvents, upcomingEvents=upcomingEvents,
		pastEvents=pastEvents, showAllButton=showAllButton)