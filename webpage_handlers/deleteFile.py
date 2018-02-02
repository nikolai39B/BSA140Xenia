# Python libraries
import time

# GAE libraries
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore

# Utility Classes
from handlerBase import Handler

# Database Models
from fileInfo import FileInfo
import userInfo


class DeleteFileHandler(Handler):
	def renderPage(self, file='', error=''):
		self.render('deleteFile.html', file=file, error=error)
		
	def get(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete File')
		if not accessAllowed:
			return
			
		try:
			# Get the FileInfo object to edit
			file, blobInfo = self.getFileAndBlobInfo(resource)
			if file == None:
				error = 'Could not find FileInfo object with provided id. Cannot delete file.'
				self.renderPage(error=error)
				return
			if blobInfo == None:
				error = 'Could not find BlobInfo object with provided id. Cannot delete file.'
				self.renderPage(error=error)
				return
			
			# Generate the html for the photo
			filesHtml = self.renderStr('file.html', file=file, displayFilebar=False)
			
			self.renderPage(file=filesHtml)
			return
		except:
			error = 'Error: no file found with the given id. Cannot delete file.'
			
		self.renderPage(error=error)
		
	def post(self, resource):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete File')
		if not accessAllowed:
			return
			
		try:
			# Get the FileInfo object to edit
			file, blobInfo = self.getFileAndBlobInfo(resource)
			if file == None:
				error = 'Could not find FileInfo object with provided id. Cannot delete file.'
				self.renderPage(error=error)
				return
			if blobInfo == None:
				error = 'Could not find BlobInfo object with provided id. Cannot delete file.'
				self.renderPage(error=error)
				return
			
			FileInfo.delete(file)
			blobstore.delete(blobInfo.key())
			
			time.sleep(0.2)
			self.redirect('/files')
			return
		except:
			error = 'Error: no file found with the given id. Cannot delete file.'
			
		self.renderPage(error=error)
		