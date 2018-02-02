# Python libraries
import time

# GAE Libraries
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

# Utility Classes
from handlerBase import Handler

# Database Models
from eventInfo import EventInfo
from imageInfo import ImageInfo
import userInfo

class AddPhotosHandler(blobstore_handlers.BlobstoreUploadHandler, Handler):
	def renderPage(self, uploadUrl, options):
		self.render('addPhotos.html', uploadUrl=uploadUrl, options=options)

	def get(self, resource=None):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Add Photos')
		if not accessAllowed:
			return
		
		# Ensure that the page is not cached - will cause upload errors otherwise
		self.response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
		self.response.headers["Pragma"] = "no-cache"
		self.response.headers["Expires"] = "0"
		
		# Get the default event id (used if redirecting from a specific event page)
		defaultEventId = ''
		try:
			defaultEventId = str(urllib.unquote(resource))
		except:
			pass
		optionTagHtml = self.getEventOptionsList(defaultEventId)
		
		# This inserts the upload url into the page. The file is uploaded and then the user
		#	is redirected back to this page (as a post)
		uploadUrl = blobstore.create_upload_url('/add_photos')
		self.renderPage(uploadUrl, optionTagHtml)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Add Photos')
		if not accessAllowed:
			return
			
		# Get the key to the linked event
		eventId = str(self.request.get('eventId'))
		
		# Get the uploaded files
		uploadFiles = self.get_uploads('file')
		if len(uploadFiles) < 1:
			# If there were no files uploaded, redirect back to the format
			error = 'no file'
			self.redirect('/add_photos?e=%s' % error)
			return
		
		# Define the specific file types that are allowed
		imageTypes = [
			'image/bmp',
			'image/jpeg',
			'image/png'
		]
		
		blobKey = None
		for blobInfo in uploadFiles:
			# Store the ImageInfo instances in the datastore
			if blobInfo.content_type in imageTypes:
				imageUrl = images.get_serving_url(blob_key=blobInfo.key())
				blobKey = str(blobInfo.key())
			
				ii = ImageInfo(blobKey=blobKey, imageUrl=imageUrl,
					contentType=blobInfo.content_type, filename=blobInfo.filename, eventId=eventId,
					created=blobInfo.creation, spotlight=False)
				ii.put()
				
			# If the file is not an image, delete it (to prevent users from uploading non-images
			#	through this form)
			else:
				blobInfo.delete()
		
		time.sleep(1)
		
		# If the user uploaded exactly one image, redirect to the edit photo page for that photo
		if blobKey != None and len(uploadFiles) == 1:
			self.redirect('/edit_photo/%s' % blobKey)
			return
		
		# Otherwise, go to the main photos page		
		self.redirect('/photos')
