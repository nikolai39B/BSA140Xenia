# Python libraries
import time

# GAE libraries
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# Utility Classes
from handlerBase import Handler

# Database Models
from fileInfo import FileInfo
import userInfo

class DownloadFileHandler(Handler, blobstore_handlers.BlobstoreDownloadHandler):
	

	def get(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Download File')
		if not accessAllowed:
			return
			
		try:
			# Get the FileInfo object to edit
			file, blobInfo = self.getFileAndBlobInfo(resource)
			if blobInfo == None:
				error = 'Could not find BlobInfo object with provided id. Cannot delete file.'
				self.renderPage(error=error)
				return
			
			# Download the file
			self.send_blob(blobInfo, save_as=blobInfo.filename)
			return
		except:
			pass
		