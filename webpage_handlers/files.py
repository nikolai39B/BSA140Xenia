# Python libraries
import time
import re

# GAE libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# Database Models
from fileInfo import FileInfo
import userInfo

class FilesHandler(blobstore_handlers.BlobstoreUploadHandler, Handler):
	def renderPage(self, files='', title='', file='', description='', error='', uploadUrl = ''):
		self.render('files.html', files=files, title=title, file=file, description=description,
			error=error, uploadUrl=uploadUrl)

	def get(self, resource=None):
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Files')
		if not accessAllowed:
			return
			
		# Ensure that the page is not cached - will cause upload errors otherwise
		self.response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
		self.response.headers["Pragma"] = "no-cache"
		self.response.headers["Expires"] = "0"
		
		# Get any error messages
		error = self.request.get('e')
		
		# This inserts the upload url into the page. The file is uploaded and then the user
		#	is redirected back to this page (as a post)
		uploadUrl = blobstore.create_upload_url('/files')
		self.renderPage(files=self.getFiles(), error=error, uploadUrl=uploadUrl)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Add File')
		if not accessAllowed:
			return
		
		# Get the values for the file
		uploadFile = self.get_uploads('file')
		
		# Test the file details
		error = ''
		if len(uploadFile) < 1:
			# If there were no files uploaded, redirect back to the form
			error += 'Please select a file to upload.'
			
		if len(uploadFile) > 1:
			# If multiple files were uploaded, redirect back to the form
			error += 'Please select only one file.'
			
		# If there are errors, display them
		if error != '':
			self.redirect('/files?e=%s' % error)
			return
		
		# Otherwise, store the file
		else:			
			file = uploadFile[0]
			blobKey = str(file.key())
			
			fi = FileInfo(title=file.filename, blobKey=blobKey)
			fi.put()
			
			time.sleep(0.5)
			self.redirect('/edit_file/%s' % fi.key().id())
			
	"""
	This function generates the html for all of the uploaded files.
	
	returns: string
	"""
	def getFiles(self):
		# Get the files and generate the html
		files = db.GqlQuery("SELECT * from FileInfo "
							"ORDER BY title")
			
		filesHtml = ''
		for file in files:
			filesHtml += self.renderStr('file.html', file=file, displayFilebar=True)
		
		return filesHtml