# Python libraries
import time
import re

# GAE libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler

# Database Models
from linkInfo import LinkInfo
import userInfo

class DeleteLinkHandler(Handler):
	def renderPage(self, linkBlock='', error=''):
		self.render('deleteLink.html', link=linkBlock, error=error)

	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Link')
		if not accessAllowed:
			return
			
		try:
			# Get the photo object and key for the given photo
			id = int(self.request.get('id'))
			link = LinkInfo.get_by_id(id)
			
			# If either the photo or the key could not be found, raise and exception (to be caught by the
			#	proceeding except).
			if link == None:
				raise Exception()
			
			# Generate the html for the photo
			linkBlock = self.renderStr('link.html', link=link, displayLinkbar=False)
			
			self.renderPage(linkBlock=linkBlock)
			return
		except:
			error = 'Error: no photo found with the given id. Cannot delete photo.'
			
		self.renderPage(error=error)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Photo')
		if not accessAllowed:
			return
		
		try:
			# Get the photo object and key for the given photo
			id = int(self.request.get('id'))
			link = LinkInfo.get_by_id(id)
			
			# If either the photo or the key could not be found, raise and exception (to be caught by the
			#	proceeding except).
			if link == None:
				raise Exception()
			
			LinkInfo.delete(link)
			
			time.sleep(0.2)
			self.redirect('/links')
			return
		except:
			error = 'Error: no link found with the given id. Cannot delete link.'
			
		self.renderPage(error=error)