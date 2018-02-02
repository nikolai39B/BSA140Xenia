# Python libraries
import time
import re
import urllib

# GAE libraries
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# Utility classes
from handlerBase import Handler

# Database Models
from fileInfo import FileInfo
import userInfo

class EditFileHandler(blobstore_handlers.BlobstoreUploadHandler, Handler):
	def renderPage(self, title='', description='', filename='', contentType='', error=''):
		self.render('editFile.html', title=title, description=description, filename=filename, 
			contentType=contentType, error=error)

	def get(self, resource=None):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit File')
		if not accessAllowed:
			return
		
		# Get the FileInfo object to edit
		file, blobInfo = self.getFileAndBlobInfo(resource)
		if file == None:
			error = 'Could not find FileInfo object with provided id. Cannot edit file.'
			self.renderPage(error=error)
			return
		if blobInfo == None:
			error = 'Could not find BlobInfo object with provided id. Cannot edit file.'
			self.renderPage(error=error)
			return
			
		# Get the file details
		title = file.title
		description = file.description
		if description == None:
			description = ''
		filename = blobInfo.filename
		contentType = blobInfo.content_type
		
		
		self.renderPage(title=title, description=description, filename=filename, contentType=contentType)
		
	def post(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit File')
		if not accessAllowed:
			return
		
		# Get the FileInfo object to edit
		file, blobInfo = self.getFileAndBlobInfo(resource)
		if file == None:
			error = 'Could not find FileInfo object with provided id. Cannot edit file.'
			self.renderPage(error=error)
			return
		if blobInfo == None:
			error = 'Could not find BlobInfo object with provided id. Cannot edit file.'
			self.renderPage(error=error)
			return
		
		# Get the values for the file
		title = self.request.get('title')
		description = self.request.get('description')
		filename = blobInfo.filename
		contentType = blobInfo.content_type
		
		# Test the file details
		error = ''
		if title == '':
			error += ' Please provide a title for the file.<br>'
			
		# If there are errors, display them
		if error != '':
			self.renderPage(title=title, description=description, filename=filename, 
				contentType=contentType, error=error)
			return
		
		# Otherwise, save the data
		else:			
			file.title = title
			file.description = description
				
			file.put()
			
			time.sleep(0.2)
			self.redirect('/files')	