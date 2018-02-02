# Python libraries
import time
import re

# GAE libraries
import urllib
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler
import dateTimeParser

# Database Models
from contactInfo import ContactInfo
import contactInfo
import userInfo

class DeleteContactHandler(Handler):
	def renderPage(self, contact='', error=''):
		self.render('deleteContact.html', contact=contact, error=error)
		
	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Contact')
		if not accessAllowed:
			return
			
		# Get the contact id (used when editing existing contacts)
		contactId = -1
		try:
			contactId = int(self.request.get("contactId"))
		except:
			pass
		
		# If an id was provided, find the corresponding contact in the datastore
		contact = ContactInfo.get_by_id(contactId)
		
		# If there is no corresponding contact, display the error
		if contact == None:
			error = 'No contact found with id. Cannot delete contact.'
			self.renderPage(error=error)
			return
			
		contactHtml = self.renderStr('contactPrivate.html', contacts=[ contact ], numContacts=1,
			displayContactBar=False)
		self.renderPage(contact=contactHtml)
		
	def post(self):
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Delete Contact')
		if not accessAllowed:
			return
			
		# Get the contact id (used when editing existing contacts)
		contactId = -1
		try:
			contactId = int(self.request.get("contactId"))
		except:
			pass
		
		# If an id was provided, find the corresponding contact in the datastore
		contact = ContactInfo.get_by_id(contactId)
		
		# If there is no corresponding contact, display the error
		if contact == None:
			error = 'No contact found with id. Cannot delete contact.'
			self.renderPage(error=error)
			return
			
		contact.delete()
		
		time.sleep(0.2)
		self.redirect('/contact')
		