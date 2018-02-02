# Python libraries
import os
import datetime
import urllib
import re
import logging

# GAE libraries
import jinja2
import webapp2
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail

# Utility Classes
import encryption

# Database Models
from userInfo import UserInfo
from imageInfo import ImageInfo
from eventInfo import EventInfo
from fileInfo import FileInfo
from contactInfo import ContactInfo
import contactInfo
import announcementInfo
from announcementInfo import AnnouncementInfo

# Initialize the jinja2 templating
templateDir = os.path.join(os.path.dirname(__file__), '../templates')
jinjaEnv = jinja2.Environment(loader = jinja2.FileSystemLoader(templateDir), autoescape = True)

class Handler(webapp2.RequestHandler):
	"""
	Write the given text to the page
	"""
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
	
	"""
	Substitue the given values into the html template, and return the html as a string. Automatically
	inserts the user's name and admin status.
	
		template: the filename for the html template. must be located in the directory where jinja2
			was initialized
		**params: the variables to pass to the template
		
	returns: string
	"""
	def renderStr(self, template, **params):
		# Get the template loaded
		t = jinjaEnv.get_template(template)
		
		# Get current user
		user = self.getCurrentUser()
		
		# If the cookie is invalid (or does not exist) set the username to Guest
		name = 'Guest'
		adminStatus = 4
		if user != None:
			name = user.firstName
			adminStatus = user.adminStatus
		
		return t.render(user = name, adminStatus = adminStatus, **params)
		
	"""
	Substitue the given values into the html template, and display the html on the screen. Automatically
	inserts the sidebar and topbar (as well as the user's name and admin status through renderStr).
	
		template: the filename for the html template. must be located in the directory where jinja2
			was initialized
		**kw: the variables to pass to the template
		
	returns void
	"""
	def render(self, template, **kw):
		# Get sidebar and topbar
		sidebar = self.renderStr('sidebar.html')
		topbar = self.renderStr('topbar.html')
		
		self.write(self.renderStr(template, sidebar = sidebar, topbar = topbar, **kw))
		
	"""
	Read the current user cookie and ensure it is valid. Return either the UserInfo object or None.
	
	returns: UserInfo (or None)
	"""
	def getCurrentUser(self):
		# Get current user's username from the cookie
		username = encryption.getCurrentUserFromHash(self.request.cookies.get('user'))
		
		# Find the user datastore object with the given username
		if username != None:
			user = db.GqlQuery("SELECT * from UserInfo "
							   "WHERE username = :1 "
							   "LIMIT 1", username)
			return user.get()
		return None
		
	"""
	Returns True if the current user has the appropriate admin status. If the user does not have the
	appropriate admin status, the redirect flags are set to the 'unauthorized' page and the function
	return False.
	
		requiredStatus: the minimum admin status required for the page
		pageName: the name of the calling page
		
	returns: boolean
	"""
	def verifyAdminStatus(self, requiredStatus, pageName):
		# Get the current user and set the default admin status to 4 (not logged in)
		user = self.getCurrentUser()
		adminStatus = 4
		
		# If the user is logged in, set the admin status to their admin status
		if user != None:
			adminStatus = user.adminStatus
		
		# If they do not have a low enough admin status, redirect to the unauthorized page
		if adminStatus > requiredStatus:
			self.redirect('/unauthorized?p=%s' % pageName)
			return False
			
		return True
	
	"""
	Builds the event photos block for the given event.
	
		event: the event from which to get the photos
		maxPhotos: the maximum number of photos. the default is -1, which represents no limit
		photoSize: the size of the photo. the default is 3, which is small. the other valid options are
			2 for medium or 1 for large
	
	returns: string
	"""
	def getEventPhotosBlock(self, event, maxPhotos = -1, photoSize = 3):
		# Old utility code
		"""
		images = db.GqlQuery("SELECT * FROM ImageInfo")
		for image in images:
			image.spotlight = False
			image.put()
		"""
	
		# If there is a max photos limit, specifiy
		limitString = ""
		if maxPhotos > 0:
			limitString = "LIMIT %s" % maxPhotos
	
		# Get all of the images for the given event (limiting if necessary)
		images = db.GqlQuery("SELECT * FROM ImageInfo "
							 "WHERE eventId = :1 "
							 "ORDER BY spotlight DESC, created DESC "
							 "%s" % limitString, str(event.key().id()))
							 
		# Specify the class based on the photoSize
		cssClass = "content-image-small"
		if photoSize == 1:
			cssClass = "content-image"
		elif photoSize == 2:
			cssClass = "content-image-medium"
		else:
			# Default size (will also catch the small size option)
			photoSize = 3
			
		# Set up columns
		columns = []
		for ii in range(photoSize):
			columns.append('')
		
		# Loop through all the images
		ii = 0
		imageTag = '<img class="%s" src="%s">'
		for image in images:
			# Add the tag
			columns[ii % photoSize] += imageTag % (cssClass, image.imageUrl)
			columns[ii % photoSize] += '<br>'
			
			# If photoSize number of iterations since the last break, add a break
			#if (ii + 1) % photoSize == 0:
			#	eventPhotosHtml += '<br>'
				
			ii += 1
			
		eventPhotosHtml = self.renderStr('photosBlock.html', photoSize=photoSize, columns=columns,
			cssClass=cssClass)
				
		return eventPhotosHtml
		
	"""
	Generates the html for a list of events
	
		eventList: a list of EventInfo objects from which to generate the html
		addUtilityBar: whether or not to add the 'Edit Event | Delete Event' bar underneath the event
		maxPhotos: the maximum number of photos. the default is 3. -1 represents no limit
		photoSize: the size of the photo. the default is 3, which is small. the other valid options are
			2 for medium or 1 for large
		
	returns: string
	"""
	def getEventsHtml(self, eventList, addUtilityBar=True, maxPhotos=3, photoSize=3):
		eventsHtml = ''
		
		firstIteration = True
		for event in eventList:
			# Add breaks between events (but not before the first or after the last event)
			if firstIteration:
				firstIteration = False
			else:
				eventsHtml += '<br>'
		
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
			
			# Get event photos
			eventPhotosBlock = self.getEventPhotosBlock(event, maxPhotos, photoSize)
				
			# Append the new event html the end of the string of events
			eventsHtml += self.renderStr('event.html', event=event, 
				departureTimeMeridiem=departureTimeMeridiem, returnTimeMeridiem=returnTimeMeridiem,
				eventId=eventId, eventPhotosBlock=eventPhotosBlock, addUtilityBar=addUtilityBar)
				
		return eventsHtml
		
	"""
	Get the ImageInfo object and associated blobstore key for the given resource.
	
		resource: the resource passed to the calling handler
		
	returns: ImageInfo, string (or None)
	"""
	def getPhotoAndKey(self, resource):
		try:
			# Get the key from the image blob
			resource = str(urllib.unquote(resource))
			blobInfo = blobstore.BlobInfo.get(resource)
			key = str(blobInfo.key())
			
			# Get the image object from the datastore using the key
			photo = db.GqlQuery("SELECT * FROM ImageInfo "
								"WHERE blobKey = :1 "
								"LIMIT 1", key)
			photo = photo.get()
			
			return photo, key
		except:
			return None, ""
		
	"""
	Get the FileInfo object and associated BlobInfo for the given file.
	
		resource: the resource passed to the calling handler
		
	returns: FileInfo, BlobInfo (or FileInfo, None | None, None)
	"""
	def getFileAndBlobInfo(self, resource):
		file = None
		blobInfo = None
		try:
			fileId = str(urllib.unquote(resource))
			file = FileInfo.get_by_id(int(fileId))
			if file == None:
				return None, None
		
			# Get the blobstore object to edit
			blobInfo = blobstore.BlobInfo.get(file.blobKey)
			if blobInfo == None:
				return file, None
				
			return file, blobInfo
		except:
			return None, None
		
	# Still need to get everything to reference the eventInfo version
	"""
	Gets the html for the options for a 'select' input tag. The options are generated from the
	EventInfo objects stored in the database, and the option id is the EventInfo id.
	
		defaultEventId: the id of the event that should begin selected
		
	returns: string
	"""
	def getEventOptionsList(self, defaultEventId=''):
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
		optionTagHtml += optionTag % ('', 'selected="selected"' if defaultEventId == '' else '', 'None')
		
		return optionTagHtml
		
	"""
	Sends out the announcement to all selected contacts.
	
		announcementInfoInstance: the announcement instance to send out
		
	returns void
	"""
	def sendAnnouncement(self, announcementInfoInstance):
		# Get the email fields
		outboundSender = "announceSender@bsa140xenia.appspotmail.com"
		subject = announcementInfoInstance.title
		body = announcementInfoInstance.content
		
		# Add the date time to the bottom
		compDT = announcementInfo.getCompensatedDatetime(announcementInfoInstance.created)
		body += '\n\nSent: %s at %s' % (
			compDT.strftime(announcementInfo.dateFormat),
			compDT.strftime(announcementInfo.timeFormat)
			)
		
		# Add the user to the bottom
		user = UserInfo.get_by_id(int(announcementInfoInstance.creatorId))
		userName = user.firstName + " " + user.lastName
		body += '\nSent By: ' + userName
		
		# Get the user's contact info and add it to the bottom
		contact = db.GqlQuery("SELECT * FROM ContactInfo "
							  "WHERE userInfoId = :1", str(user.key().id()))
		contact = contact.get()
		if contact != None:
			if contact.cellPhoneNumber != None and contact.cellPhoneNumber != '':
				body += '\nCell: ' + contactInfo.makePhoneNumberPretty(contact.cellPhoneNumber)
			if contact.homePhoneNumber != None and contact.homePhoneNumber != '':
				body += '\nHome: ' + contactInfo.makePhoneNumberPretty(contact.homePhoneNumber)
			if contact.email != None and contact.email != '':
				body += '\nEmail: ' + contact.email
			if contact.altEmail != None and contact.altEmail != '':
				body += '\nAlt Email: ' + contact.altEmail
				
		body = str(body)
				
		# Create the text message formatted body (deprecated)
		#textMessageBody = str('\n' + subject + ':\n\n' + body + '\n\n')
				
		# Log the message
		logging.info("Sent message:\n" + body)
		
		# Send out the email
		contacts = db.GqlQuery("SELECT * FROM ContactInfo")
		firstTo = ''
		emailCcs = ''
		for contact in contacts:
			
			# If this contact has the send email announcement flag, send the email
			if contact.sendEmailAnnouncement:
				to = contact.email
				
				# Make sure they actually have an email
				if to != None and to != '':
					# Instead of sending the email, add it to the CCs list
					if firstTo == '':
						firstTo = to
					else:
						emailCcs += to + ', '
			
			# If this contact has the send alt email announcement flag, send the email
			if contact.sendAltEmailAnnouncement:
				to = contact.altEmail
				
				# Make sure they actually have an alt email
				if to != None and to != '':
					# Instead of sending the email, add it to the CCs list
					if firstTo == '':
						firstTo = to
					else:
						emailCcs += to + ', '
				
			# If this contact has the send cell announcement flag, send the text message (deprecated)
			# if contact.sendCellAnnouncement and contact.carrier != contactInfo.other[1]	and contact.carrier != contactInfo.none[1]:
				# to = ''
				# for carrier in contactInfo.carriers:
					# if carrier[1] == contact.carrier:
						# to = carrier[0] % contact.cellPhoneNumber
					
				# # Make sure they actually have a cell number and a carrier
				# if to != '':
					# mail.send_mail(sender=outboundSender, to=to, subject=subject, body=textMessageBody)
					# logging.info("Sent to " + to)
		
		# Send it to all the emails at once. This lets everyone see everyone cc'd onto it
		if emailCcs != '' and firstTo != '':
			mail.send_mail(sender=outboundSender, to=firstTo, cc=emailCcs, subject=subject, body=body)
		elif firstTo != '':
			mail.send_mail(sender=outboundSender, to=firstTo, subject=subject, body=body)
		logging.info("Sent to " + firstTo + ', ' + emailCcs)
		