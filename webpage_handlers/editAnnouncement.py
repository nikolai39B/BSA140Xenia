# Python libraries
import time
import re

# GAE libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler

# Database Models
from announcementInfo import AnnouncementInfo
from userInfo import UserInfo
import userInfo

class EditAnnouncementHandler(Handler):
	def renderPage(self, title='', content='', error=''):
		self.render('editAnnouncement.html', title=title, content=content,	error=error)

	def get(self, resource=None):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit Announcement')
		if not accessAllowed:
			return
			
		# Get the current announcement
		announcement = self.getCurrentAnnouncement()
		if announcement == None:
			error = 'No announcement found with given id. Cannot edit announcement.'
			self.renderPage(error=error)
			return
			
		title = announcement.title
		content = announcement.content
			
		self.renderPage(title=title, content=content)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit Announcement')
		if not accessAllowed:
			return		
		
		# Get the current announcement
		announcement = self.getCurrentAnnouncement()
		if announcement == None:
			error = 'No announcement found with given id. Cannot edit announcement.'
			self.renderPage(error=error)
			return
		
		# Get the announcement details
		title = self.request.get('title')
		content = self.request.get('content')
		creatorId = str(self.getCurrentUser().key().id())
		
		error = ''
		if title == '':
			error += 'Please provide a title.<br>'
		
		if content == '':
			error += 'Please provide content for the announcement.<br>'
			
		if error != '':
			self.renderPage(title=title, content=content, error=error)
			return
			
		else:
			announcement.title = title
			announcement.content = content
			announcement.creatorId = creatorId
			announcement.put()
			
			time.sleep(0.2)
			self.redirect('/announcements')
			return
			
	"""
	Returns the current announcement to edit.
	
	returns: AnnouncementInfo
	"""
	def getCurrentAnnouncement(self):
		announcement = self.request.get('id')
		try:
			announcement = AnnouncementInfo.get_by_id(int(announcement))
			if announcement == None:
				raise Exception()
			
			return announcement
			
		except:
			return None