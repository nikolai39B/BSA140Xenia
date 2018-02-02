# GAE libraries
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# Utility Classes
from handlerBase import Handler

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler, Handler):
	# This class should only be accessed through a redirect from a file uploading form.
	def get(self):
		# If there is a request for this page, redirect to the add photos form
		self.redirect('/add_photos')
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(2, 'Add Photos')
		if not accessAllowed:
			return
		
		# Get the uploaded files
		uploadFiles = self.get_uploads('file')
		blobInfo = uploadFiles[0]
		
		imageTypes = [
			'image/bmp',
			'image/jpeg',
			'image/png'
		]
		if not blobInfo.content_type in imageTypes:
			self.redirect('/')
			return
		
		self.redirect('/photo/%s' % blobInfo.key())