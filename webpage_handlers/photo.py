# GAE libraries
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers

# Utility Classes
from handlerBase import Handler

# Database Models
from imageInfo import ImageInfo
import imageInfo
from eventInfo import EventInfo


class PhotoHandler(blobstore_handlers.BlobstoreDownloadHandler, Handler):
	def renderPage(self, photoBlock='', photoId='', error=''):
		self.render('photo.html', photoBlock=photoBlock, photoId=photoId, error=error)
		
	def get(self, resource):
		try:
			# Get the photo object and key for the given photo
			photo, key = self.getPhotoAndKey(resource)
			
			# If either the photo or the key could not be found, raise and exception (to be caught by the
			#	proceeding except).
			if photo == None or key == None:
				raise Exception()
			
			# If both were found, get the details (or an empty string for any missing element)
			title, description, date, event = imageInfo.getImageDetails(photo)
			
			# Generate the html for the photo
			photoBlock = self.renderStr('photoBlock.html', title=title, imageUrl=photo.imageUrl,
				photoId=photo.blobKey, event=event, time=date, description=description,
				displayPhotobar=True)
			
			self.renderPage(photoBlock, key)
			return
		except:
			error = 'Error: no photo found with the given id.'
			
		self.renderPage(error=error)