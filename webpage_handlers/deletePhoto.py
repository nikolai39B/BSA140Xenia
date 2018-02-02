# Python libraries
import time

# GAE libraries
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore

# Utility Classes
from handlerBase import Handler

# Database Models
from imageInfo import ImageInfo
import imageInfo
import userInfo


class DeletePhotoHandler(Handler):
	def renderPage(self, photoBlock='', error=''):
		self.render('deletePhoto.html', photoBlock=photoBlock, error=error)
		
	def get(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Photo')
		if not accessAllowed:
			return
			
		try:
			# Get the photo object and key for the given photo
			photo, key = self.getPhotoAndKey(resource)
			
			# If either the photo or the key could not be found, raise and exception (to be caught by the
			#	proceeding except).
			if photo == None or key == None:
				raise Exception()
			
			# If both were found, get the details (or an empty string for any missing element)
			title, description, date, eventName = imageInfo.getImageDetails(photo)
			
			# Generate the html for the photo
			photoBlock = self.renderStr('photoBlock.html', title=title, imageUrl=photo.imageUrl,
				photoId=photo.blobKey, eventName=eventName, time=date, description=description,
				imageLink=True)
			
			self.renderPage(photoBlock)
			return
		except:
			error = 'Error: no photo found with the given id. Cannot delete photo.'
			
		self.renderPage(error=error)
		
	def post(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Photo')
		if not accessAllowed:
			return
		
		try:
			# Get the photo object and key for the given photo
			photo, key = self.getPhotoAndKey(resource)
			
			# If either the photo or the key could not be found, raise and exception (to be caught by the
			#	proceeding except).
			if photo == None or key == None:
				raise Exception()

			# Delete both the blobstore photo (the actual file) and the datastore object (the photo title,
			#	description, etc.
			ImageInfo.delete(photo)
			blobstore.delete(key)
			
			time.sleep(0.2)
			self.redirect('/photos')
			return
		except:
			error = 'Error: no photo found with the given id. Cannot delete photo.'
			
		self.renderPage(error=error)