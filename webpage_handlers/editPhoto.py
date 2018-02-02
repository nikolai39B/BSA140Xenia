# Python libraries
import time

# GAE libraries
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers

# Utility Classes
from handlerBase import Handler
import dateTimeParser

# Database Models
from imageInfo import ImageInfo
import imageInfo
from eventInfo import EventInfo
import userInfo

class EditPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler, Handler):
	def renderPage(self, photoId='', title='', imageUrl='', options='', date='', description='', error='',
		spotlight=''):
		self.render('editPhoto.html', photoId=photoId, title=title, imageUrl=imageUrl, options=options,
			time=date, description=description, spotlight=spotlight, error=error)
		
	def get(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit Photo')
		if not accessAllowed:
			return
			
		try:
			# Get the photo object and key for the given photo
			photo, key = self.getPhotoAndKey(resource)
			
			# If either the photo or the key could not be found, raise and exception (to be caught by the
			#	proceeding except).
			if photo == None or key == None:
				raise Exception()
				
			# Get the photo details, and parse the date into a usable string format
			title, description, date, event = imageInfo.getImageDetails(photo)
			date = dateTimeParser.parseDateTimeToString(date)
			spotlight = ''
			if (photo.spotlight == True):
				spotlight = 'selected'

			# Generate the option tags for the event select
			optionTagHtml = self.getEventOptionsList(photo.eventId)
				
			self.renderPage(photoId=key, title=title, imageUrl=photo.imageUrl, options=optionTagHtml,
				date=date, description=description, spotlight=spotlight)
			return
		except:
			error = 'Error: no photo found with the given id. Cannot edit photo.'
			
		self.renderPage(error=error)
		
	def post(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit Photo')
		if not accessAllowed:
			return
			
		title = self.request.get('title')
		spotlight = self.request.get('spotlight')
		eventId = self.request.get('eventId')
		date = dateTimeParser.parseStringToDateTime(self.request.get('time'))
		description = self.request.get('description')
		
		#try:		
		# Get the photo object and key for the given photo
		photo, key = self.getPhotoAndKey(resource)
		
		# If either the photo or the key could not be found, raise and exception (to be caught by the
		#	proceeding except).
		if photo == None or key == None:
			raise Exception()
			
		# Update the entries in photo and push them to the datastore
		photo.title = title
		photo.spotlight = (spotlight != '')
		photo.eventId = eventId
		photo.date = date
		photo.description = description
		photo.put()
		
		# Pause to allow the datastore to update and redirect to the photo permalink page
		time.sleep(0.2)		
		self.redirect('/photo/%s' % key)
		return
		#except:
		#	error = 'Error: no photo found with the given id. Cannot edit photo.'
			
		self.renderPage(error=error)