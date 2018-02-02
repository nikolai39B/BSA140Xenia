# Python libraries
import time
import re

# GAE libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler

# Database Models
import announcementInfo
from announcementInfo import AnnouncementInfo
from userInfo import UserInfo
import userInfo

class AnnouncementsHandler(Handler):
	def renderPage(self, announcements='', title='', content='', error=''):
		self.render('announcements.html', announcements=announcements, title=title, content=content,
			error=error)

	def get(self, resource=None):
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Announcements')
		if not accessAllowed:
			return
			
		self.renderPage(announcements=self.getAnnouncements())
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Announcements')
		if not accessAllowed:
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
			self.renderPage(announcements=self.getAnnouncements(), title=title, content=content,
				error=error)
			return
			
		else:
			aI = AnnouncementInfo(title=title, content=content, creatorId=creatorId)
			aI.put()
			
			self.sendAnnouncement(aI)
			
			time.sleep(0.2)
			self.redirect('/announcements')
			return
			
	"""
	This function generates the html for the past 20 announcements.
	
	returns: string
	"""
	def getAnnouncements(self):
		# Get the files and generate the html
		announcements = db.GqlQuery("SELECT * from AnnouncementInfo "
									"ORDER BY created "
									"LIMIT 20")
			
		announcementsHtml = ''
		for announcement in announcements:
			creator = UserInfo.get_by_id(int(announcement.creatorId))
			creator = '%s %s' % (creator.firstName, creator.lastName)
			
			compDT = announcementInfo.getCompensatedDatetime(announcement.created)
			date = compDT.strftime(announcementInfo.dateFormat)
			time = compDT.strftime(announcementInfo.timeFormat)
			
			announcementsHtml += self.renderStr('announcement.html', announcement=announcement,
				creator=creator, date=date, time=time, displayAnnouncementbar=True)
		
		return announcementsHtml