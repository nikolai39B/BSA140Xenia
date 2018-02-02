# Python libraries
import logging
import re

# GAE libraries
import urllib
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler

# Database Models
from contactInfo import ContactInfo
import contactInfo
import userInfo

class SearchContactsHandler(Handler):
	def renderPage(self, searchText='', searchResults=''):
		self.render('searchContacts.html', searchText=searchText, searchResults=searchResults)
		
	def get(self):
		# Get the search string
		searchText = self.request.get('searchText')
		if searchText == '':
			self.renderPage()
			return		
		splitText = [x.lower() for x in re.split('[ |\(\)\.,-]+', str(searchText)) if x] # This filters out empty str
		
		# Determine whether to search public or private
		user = self.getCurrentUser()
		adminStatus = userInfo.loggedOut
		if user != None:
			adminStatus = user.adminStatus
		searchPrivate = adminStatus < userInfo.loggedOut
		
		# Get the contacts
		contacts = db.GqlQuery("SELECT * FROM ContactInfo "
							   "%s ORDER BY lastName ASC, firstName ASC" % (
							   "WHERE showPublic = True " if not searchPrivate else ""))
		foundContacts = []
		
		# Loop through all contacts and text to find matches
		for contact in contacts:
			for text in splitText:
				if ((contact.firstName != None and text in contact.firstName.lower()) or  
					(contact.lastName != None and text in contact.lastName.lower()) or  
					(contact.position != None and text in contact.position.lower()) or  
					(contact.cellPhoneNumber != None and text in contact.cellPhoneNumber) or  
					(contact.homePhoneNumber != None and text in contact.homePhoneNumber) or  
					(contact.email != None and text in contact.email.lower()) or  
					(contact.altEmail != None and text in contact.altEmail.lower())):
					foundContacts.append(contact)
					break
	
		searchResults = '<div class="content-centered">No contacts found.</div>'
		if foundContacts != []:
			htmlFile = 'contactPrivate.html' if searchPrivate else 'contactPublic.html'
			searchResults = self.renderStr(htmlFile, contacts=foundContacts, 
				numContacts=len(foundContacts), displayContactBar=searchPrivate)

		self.renderPage(searchText, searchResults)
		
		