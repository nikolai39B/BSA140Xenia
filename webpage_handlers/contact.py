# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler
import userInfo

# Database Models
from contactInfo import ContactInfo

class ContactHandler(Handler):
	def renderPage(self, contactHtml=''):
		self.render('contact.html', contactHtml=contactHtml)
		
	def get(self):
		adminStatus = userInfo.loggedOut
		contactHtml = ''
		
		# Determine if the user is allowed to browse the private contacts
		try:
			adminStatus = self.getCurrentUser().adminStatus
			if adminStatus < userInfo.loggedOut:
				contactHtml = self.generatePrivateContactHtml()
			else:
				contactHtml = self.generatePublicContactHtml()
		except:
			contactHtml = self.generatePublicContactHtml()
	
		self.renderPage(contactHtml=contactHtml)
		
	def generatePublicContactHtml(self):
		contacts = db.GqlQuery("SELECT * FROM ContactInfo "
							   "WHERE showPublic = True "
							   "ORDER BY lastName ASC, firstName ASC")
							   
		return self.renderStr('contactPublic.html', contacts=contacts, numContacts=contacts.count())
		
	def generatePrivateContactHtml(self):
		contacts = db.GqlQuery("SELECT * FROM ContactInfo "
							   "ORDER BY lastName ASC, firstName ASC")
							   
		return self.renderStr('contactPrivate.html', contacts=contacts, numContacts=contacts.count(),
			displayContactBar=True)