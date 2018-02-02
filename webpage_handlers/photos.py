# GAE libraries
from google.appengine.ext import db
from google.appengine.ext import blobstore

# Utility Classes
from handlerBase import Handler

# Database Models
from imageInfo import ImageInfo
import imageInfo
from eventInfo import EventInfo


class PhotosHandler(Handler):
	def renderPage(self, photoBlocks=''):
		self.render('photos.html', photoBlocks=photoBlocks)
		
	def get(self):
		# Retrieve all the ImageInfo objects from the datastore
		photos = db.GqlQuery("SELECT * from ImageInfo "
							 "ORDER BY spotlight DESC, created DESC ")
				
		photoHtml = ''		
		for photo in photos:
			# Get the details for each photo
			title, description, date, event = imageInfo.getImageDetails(photo)
			
			# Ensure that blob file for photo exists
			blobInfo = blobstore.BlobInfo.get(photo.blobKey)
			if blobInfo == None:
				continue
					
			# Add the photo html to the block
			photoHtml += self.renderStr('photoBlock.html', title=title, imageUrl=photo.imageUrl,
				photoId=photo.blobKey, description=description, event=event, time=date,
				imageLink=True, displayPhotobar=True)
	
		self.renderPage(photoHtml)