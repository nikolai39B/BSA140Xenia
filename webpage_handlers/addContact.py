# Python libraries
import time
import re
import logging

# GAE libraries
import urllib
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler
import dateTimeParser

# Database Models
from contactInfo import ContactInfo
import contactInfo
from userInfo import UserInfo
import userInfo

class AddContactHandler(Handler):
	def renderPage(self, #carriers=contactInfo.carriers, defaultCarrier=contactInfo.aTAndT[1],
		states=contactInfo.states, defaultState='Ohio', error='', firstName='', lastName='',
		position='', cellNumber='',	homeNumber='', email='', altEmail='', street='', city='', 
		state='', zip='', public='', createNew=True):
		
		# removed: 'carriers=carriers, defaultCarrier=defaultCarrier, '
		self.render('addContact.html', states=states,
			defaultState=defaultState, error=error, firstName=firstName, lastName=lastName, 
			position=position, cellNumber=cellNumber, homeNumber=homeNumber, email=email, 
			altEmail=altEmail, street=street, city=city, state=state, zip=zip, public=public, 
			createNew=createNew)
		
	def get(self):	
		# Get the contact id (used when editing existing contacts)
		contactId = -1
		try:
			contactId = int(self.request.get("contactId"))
		except:
			pass
		contact = ContactInfo.get_by_id(contactId)
		
		if (not self.contactIsForCurrentUser(contactId) and
			not self.verifyAdminStatus(userInfo.poster, 'Add Contact')):
			logging.info("shouldn't display page get")
			return
		
		# If there is no corresponding contact, display a blank form
		if contact == None:
			self.renderPage()
			return
			
		# Get/set values
		firstName = contact.firstName
		lastName = contact.lastName
		position = contact.position
		
		cellNumber = contact.cellPhoneNumber
		#carrier = contact.carrier		
		#if carrier == '' or carrier == None:
		#	carrier=contactInfo.aTAndT[1]
		homeNumber = contact.homePhoneNumber
		
		email = contact.email
		if email == None:
			email = ''
		altEmail = contact.altEmail
		if altEmail == None:
			altEmail = ''
			
		street = contact.street
		state = contact.state
		if state == '' or state == None:
			state='Ohio'
		city = contact.city
		zip = contact.zip
		if zip == -1:
			zip = ''
		public = contact.showPublic
		if public == True:
			public = 'checked'
		else:
			public = ''
			
		# removed: 'defaultCarrier=carrier, '
		self.renderPage(firstName=firstName, lastName=lastName, position=position, cellNumber=cellNumber,
			homeNumber=homeNumber, email=email, altEmail=altEmail, street=street, 
			city=city, defaultState=state,	zip=zip, public=public, createNew=False)
		
	def post(self):				
		# Get the contact id (used when editing existing contacts)
		contactId = -1
		try:
			contactId = int(self.request.get("contactId"))
		except:
			pass
		contact = ContactInfo.get_by_id(contactId)
		
		if not self.contactIsForCurrentUser(contactId) and not self.verifyAdminStatus(userInfo.poster, 'Add Contact'):
			logging.info("shouldn't display page in post")
			return
			
		# Get info
		firstName = self.request.get('firstName')
		lastName = self.request.get('lastName')
		position = self.request.get('position')
		cellNumber = self.request.get('cellNumber')
		#carrier = self.request.get('carrier')
		#if carrier == contactInfo.none[1]:
		#	carrier = None
		homeNumber = self.request.get('homeNumber')
		email = self.request.get('email')
		altEmail = self.request.get('altEmail')
		street = self.request.get('street')
		city = self.request.get('city')
		state = self.request.get('state')
		zip = self.request.get('zip')
		if zip == '':
			zip = -1
		public = self.request.get('public')
		
		# Check that all values are valid
		error = ''
		reName = "^\w[\w\s-]*$"
		reEmail = "^[^@\.]+(\.[^@]+)*@[^@\.]+(\.[^@\.]+)+$"
		reStreet = "^\d+\s\w[\w\s\.]*$"
		reCity = "^\w[\w\s]*$"
		
		# First name, last name, position must be all letters
		if firstName == '' or (not re.match(reName, firstName)):
			error += 'No first name/invalid first name provided.<br>'
		if lastName == '' or (not re.match(reName, lastName)):
			error += 'No last name/invalid last name provided.<br>'
		if position != '' and (not re.match(reName, position)): # Position is optional
			error += 'Invalid position provided.<br>'
		
		# Check cell number
		cellNumbers = [s for s in cellNumber if s.isdigit()]
		if len(cellNumbers) != 10 and cellNumber != '': # Cell number optional
			error += 'Invalid cell number provided. Must be 10 digits long.<br>'
		
		# Check home number
		homeNumbers = [s for s in homeNumber if s.isdigit()]
		if len(homeNumbers) != 10 and homeNumber != '': # Home number optional
			error += 'Invalid home number provided. Must be 10 digits long.<br>'
			
		# Check email
		if not re.match(reEmail, email) and email != '': # Email optional
			error += 'Invalid email provided.<br>'
			
		# Check alt email
		if not re.match(reEmail, altEmail) and altEmail != '': # Alt email optional
			error += 'Invalid alternate email provided.<br>'

		# Only check address if at least one of the elements (besides state) was provided
		if street != '' or city != '' or zip != -1:
			# Check Street
			if street == '':
				error += 'Please provide a street name and number.<br>'
			elif not re.match(reStreet, street):
				error += 'Invalid street provided. Must consist of a street number followed by a road.<br>'
			
			# Check City
			if city == '':
				error += 'Please provide a city.<br>'
			elif not re.match(reCity, city):
				error += 'Invalid city provided.<br>'
				
			# Check Zip
			if zip == '':
				error += 'Please provide a zip code.<br>'
			else:
				zipNumbers = [s for s in zip if s.isdigit()]
				if len(zipNumbers) != 5 or len(zip) != 5:
					error += 'Invalid zip code provided. Must be 5 digits long.'
				else:
					zip = int(zip)
		
		
		# If there are errors, display them
		if error != '':
			update = self.request.get('createContact') == "Update"
			
			# removed: 'defaultCarrier=carrier, '
			self.renderPage(defaultState=state, error=error, firstName=firstName,
			lastName=lastName, position=position, cellNumber=cellNumber, homeNumber=homeNumber,
			email=email, altEmail=altEmail, street=street, city=city, state=state, zip=zip, public=public,
			createNew=not update)
			return
			
		# Otherwise, store the contact
		else:		
			cellNumber = ''
			for num in cellNumbers:
				cellNumber += num
				
			homeNumber = ''
			for num in homeNumbers:
				homeNumber += num
				
			emailProp = None
			if email != '':
				emailProp = db.Email(email)		
				
			altEmailProp = None
			if altEmail != '':
				altEmailProp = db.Email(altEmail)	
		
			# If there is no valid contact provided, create a new contact
			# removed: 'carrier=carrier, '
			if contact == None:
				contact = ContactInfo(firstName=firstName, lastName=lastName, position=position, 
				cellPhoneNumber=cellNumber, homePhoneNumber=homeNumber,
				email=emailProp, altEmail=altEmailProp, street=street, city=city, state=state, zip=zip,
				showPublic=(public == 'checked'))
			
			# If there is a contact already, update it
			else:
				contact.firstName = firstName
				contact.lastName = lastName
				contact.position = position
				contact.cellPhoneNumber = cellNumber
				#contact.carrier = carrier (deprecated)
				contact.homePhoneNumber = homeNumber
				contact.email = emailProp
				contact.altEmail = altEmailProp
				contact.street = street
				contact.city = city
				contact.state = state
				contact.zip = zip
				contact.showPublic = (public == 'checked')
			
			# Store the contact info
			
			contact.put()
			
			time.sleep(0.2)
			self.redirect('/contact')
			
			
	def contactIsForCurrentUser(self, contactId):
		# If the contactId is valid, check if it is for the current user
		contact = ContactInfo.get_by_id(contactId)
		if contact != None and contact.userInfoId != None:
			# Get the contact and current user
			contactUser = UserInfo.get_by_id(int(contact.userInfoId))
			currentUser = self.getCurrentUser()
			
			# If they both exist, check if they are the same
			if contactUser != None and currentUser != None:				
				return contactUser.username == currentUser.username
		
		