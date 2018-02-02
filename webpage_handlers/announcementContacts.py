# Python libraries
import time
import re

# GAE libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler

# Database Models
from contactInfo import ContactInfo
import userInfo

class AnnouncementContactsHandler(Handler):
	def renderPage(self, announcementContacts=''):
		self.render('announcementContacts.html', announcementContacts=announcementContacts)

	def get(self, resource=None):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Edit Announcement Contacts')
		if not accessAllowed:
			return
			
		self.renderPage(announcementContacts=self.getAnnouncementContacts())
		
	def post(self):
		contacts = db.GqlQuery("SELECT * FROM ContactInfo")
		for contact in contacts:
			# Determine whether the values are checked
			id = contact.key().id()
			cellChecked = self.request.get('cell%s' % id)
			emailChecked = self.request.get('email%s' % id)
			altEmailChecked = self.request.get('altEmail%s' % id)
			
			# (deprecated)
			# if cellChecked != '':
				# contact.sendCellAnnouncement = True
			# else:
				# contact.sendCellAnnouncement = False
				
			if emailChecked != '':
				contact.sendEmailAnnouncement = True
			else:
				contact.sendEmailAnnouncement = False
				
			if altEmailChecked != '':
				contact.sendAltEmailAnnouncement = True
			else:
				contact.sendAltEmailAnnouncement = False
				
			contact.put()
		
		self.redirect('/announcements')
		return
			
	"""
	Returns the announcement contacts selection html.
	
	returns: string
	"""
	def getAnnouncementContacts(self):
		contacts = db.GqlQuery("SELECT * FROM ContactInfo "
							   "ORDER BY lastName ASC, firstName ASC")
		
		contactHtml = ''
		for contact in contacts:
			# Get the info for the contact
			name = '%s %s' % (contact.firstName, contact.lastName)
			id = contact.key().id()
			
			# If the contact doesn't have a cell phone or a carrier, don't display it (deprecated)
			# displayCell = (contact.cellPhoneNumber != '' and contact.cellPhoneNumber != None
				# and contact.carrier != '' and contact.carrier != None and contact.carrier != 'None'
				# and contact.carrier != 'Other')
			# cellChecked = (contact.sendCellAnnouncement == True)
			
			# If the contact doesn't have an email, don't display it
			displayEmail = (contact.email != '' and contact.email != None)
			emailChecked = (contact.sendEmailAnnouncement == True)
			
			# If the contact doesn't have an alt email, don't display it
			displayAltEmail = (contact.altEmail != '' and contact.altEmail != None)
			altEmailChecked = (contact.sendAltEmailAnnouncement == True)
			
			# If the contact has none of them, don't display the contact at all
			# removed: 'not displayCell'
			if not displayEmail and not displayAltEmail:
				continue
				
			contactHtml += self.renderStr('contactSelection.html', name=name, #cell=cellChecked,
				email=emailChecked, altEmail=altEmailChecked, #displayCell=displayCell, 
				displayEmail=displayEmail, displayAltEmail=displayAltEmail, id=id)
			
		return contactHtml
		