# Python libraries
import time

# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler

# Database Models
from announcementInfo import AnnouncementInfo
import announcementInfo
from userInfo import UserInfo
import userInfo


class DeleteAnnouncementHandler(Handler):
	def renderPage(self, announcement='', error=''):
		self.render('deleteAnnouncement.html', announcement=announcement, error=error)
		
	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Announcement')
		if not accessAllowed:
			return
			
		announcement = self.getCurrentAnnouncement()
		if announcement == None:
			error = 'Error: no announcement found with the given id. Cannot delete nnouncement.'
			self.renderPage(error=error)
			return
			
		creator = UserInfo.get_by_id(int(announcement.creatorId))
		creator = '%s %s' % (creator.firstName, creator.lastName)
			
		compDT = announcementInfo.getCompensatedDatetime(announcement.created)
		date = compDT.strftime(announcementInfo.dateFormat)
		time = compDT.strftime(announcementInfo.timeFormat)
		
		announcementHtml = self.renderStr('announcement.html', announcement=announcement,
			creator=creator, date=date, time=time, displayAnnouncementbar=False)
			
		self.renderPage(announcement=announcementHtml)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Announcement')
		if not accessAllowed:
			return
			
		announcement = self.getCurrentAnnouncement()
		if announcement == None:
			error = 'Error: no announcement found with the given id. Cannot delete nnouncement.'
			self.renderPage(error=error)
			return
			
		AnnouncementInfo.delete(announcement)
		time.sleep(0.2)
			
		self.redirect('/announcements')
			
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
		