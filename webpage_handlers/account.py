# Python libraries
import re
import time

# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler
import encryption

# Database Models
from userInfo import UserInfo
import userInfo
from contactInfo import ContactInfo

class AccountHandler(Handler):
	def renderPage(self, newUsername='', usernameError='', usernameMessage='', passwordError='', 
		passwordMessage='', contact='', accountUsername='', resetOtherAccountPasswordError='',
		resetOtherAccountPasswordMessage=''):
		self.render('account.html', newUsername=newUsername, usernameError=usernameError,
			usernameMessage=usernameMessage, passwordError=passwordError, passwordMessage=passwordMessage,
			contact=contact, accountUsername=accountUsername, 
			resetOtherAccountPasswordError=resetOtherAccountPasswordError,
			resetOtherAccountPasswordMessage=resetOtherAccountPasswordMessage)
			
	def renderPageWithContact(self, newUsername='', usernameError='', usernameMessage='', passwordError='', 
		passwordMessage='', accountUsername='', resetOtherAccountPasswordError='',
		resetOtherAccountPasswordMessage=''):
			
		# Generate Contact html
		currentUser = self.getCurrentUser()
		contact = db.GqlQuery("SELECT * FROM ContactInfo "
							  "WHERE userInfoId = :1", str(currentUser.key().id()))
		contact = contact.get()
		
		contactHtml = ''
		if contact != None:
			contactHtml = self.renderStr('contactPrivate.html', contacts=[ contact ], numContacts=1,
				displayContactBar=False)
		
		self.renderPage(newUsername=newUsername, usernameError=usernameError,
			usernameMessage=usernameMessage, passwordError=passwordError, passwordMessage=passwordMessage,
			contact=contactHtml, accountUsername=accountUsername, 
			resetOtherAccountPasswordError=resetOtherAccountPasswordError,
			resetOtherAccountPasswordMessage=resetOtherAccountPasswordMessage)
		
	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Manage Account')
		if not accessAllowed:
			return
				
		# Add change message if applicable
		message = ''
		cng = str(self.request.get('cng'))
		if cng == 'username':
			message = 'Username has been changed.'
		
		self.renderPageWithContact(usernameMessage=message)
		
	def post(self):	
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Manage Account')
		if not accessAllowed:
			return
		
		# Call the approprate function based on the submitted form
		form = self.request.get('form')
		
		if form == 'changeUsername':
			self.changeUsername()
		elif form == 'changePassword':
			self.changePassword()
		elif form == 'updateContact':
			self.updateContact()
		elif form == 'resetOtherAccountPassword':
			self.resetOtherAccountPassword()
		else:
			self.redirect('/account')
			
	"""
	Changes the user's username to the username pulled from the form. Will not modify data if the
	user does not correctly enter in his or her old password.

	returns void
	"""
	def changeUsername(self):
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Manage Account')
		if not accessAllowed:
			return
			
		# Get values
		newUsername = self.request.get('newUsername')
		password = self.request.get('password')
			
		
		# Find user in database
		user = self.getCurrentUser()
		if user == None:
			self.redirect('/')
			return
			
		# Define string conditions
		error = ''
		minLength = 4;
		maxLength = 25;
		reStringUsername = "^[A-Za-z0-9_-]{%s,%s}$" % (minLength, maxLength)
		
		# Check if this is already the username
		if newUsername == user.username:
			error = 'This is already your username.'
			self.renderPageWithContact(newUsername=newUsername, usernameError=error)
			return
			
		# Username must follow reStringUsername regular expression
		if not re.match(reStringUsername, newUsername):
			error = 'No password/invalid username provided. Username must be between 4 and 25 characters.'
			self.renderPageWithContact(newUsername=newUsername, usernameError=error)
			return
			
		# Ensure no user already has this name
		userWithSameName = db.GqlQuery("SELECT * FROM UserInfo "
									   "WHERE username = '%s' " 
									   "LIMIT 1" % newUsername)
		userWithSameName = userWithSameName.get()
		
		if userWithSameName != None:
			error = "Another user already has this username."
			self.renderPageWithContact(newUsername=newUsername, usernameError=error)
			return		
		
		# Make sure the password is the user's current password
		validPassword = encryption.isHashValid(password, user.passwordHash)
		
		if not validPassword:
			error = 'Invalid password entered.'
			self.renderPageWithContact(newUsername=newUsername, usernameError=error)
			return
			
		# Update the user's username in the datastore
		user.username = newUsername
		user.put()
		
		# Update the user's cookie
		usernameHash = encryption.makeHash(newUsername)
		
		# Set expire time base on stayLoggedIn flag
		self.response.set_cookie('user', '%s|%s' % (newUsername, usernameHash),  path='/')
		
		time.sleep(1)
		
		# We redirect instead of re-render so that the cookie updates correctly
		self.redirect('/account?cng=username')
		return
	
	"""
	Changes the user's password to the password pulled from the form. Will not modify data if the
	user does not correctly enter in his or her old password.
	
	returns void
	"""
	def changePassword(self):	
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Manage Account')
		if not accessAllowed:
			return
			
		# Get values
		oldPassword = self.request.get('oldPassword')
		newPassword = self.request.get('newPassword')
		verify = self.request.get('verify')
		
		# Find user in database
		user = self.getCurrentUser()
		if user == None:
			self.redirect('/')
			return
		
		# Make sure the old password is the user's current password
		validPassword = encryption.isHashValid(oldPassword, user.passwordHash)
		
		if not validPassword:
			error = 'Invalid password entered.'
			self.renderPageWithContact(passwordError=error)
			return
			
		# Define string conditions
		error = ''
		minLength = 4;
		maxLength = 25;
		reStringPassword = "^.{%s,%s}$" % (minLength, maxLength)
			
		# Password must follow reStringPassword regular expression
		if not re.match(reStringPassword, newPassword):
			error = 'No password/invalid password provided. Password must be between 4 and 25 characters.'
			self.renderPageWithContact(passwordError=error)
			return
			
		# Old and new passwords must not be the same
		if oldPassword == newPassword:
			error = 'Old and new passwords must be different.'
			self.renderPageWithContact(passwordError=error)
			return
			
		# Verify must match password
		if verify != newPassword:
			error = 'Password and verify do not match.'
			self.renderPageWithContact(passwordError=error)
			return
			
		# Update the user's password in the datastore
		passwordHash = encryption.makeHash(newPassword)
		user.passwordHash = passwordHash
		user.put()
		
		time.sleep(1)
		message = 'Password has been changed.'
		self.renderPageWithContact(passwordMessage=message)
		return
	
	"""
	Redirects the user to the add contact page where they can update their contact information. If
	there is currently no contact linked to this account, one is created.
	
	returns void
	"""
	def updateContact(self):
		accessAllowed = self.verifyAdminStatus(userInfo.user, 'Manage Account')
		if not accessAllowed:
			return
		
		currentUser = self.getCurrentUser()
		contact = db.GqlQuery("SELECT * FROM ContactInfo "
							  "WHERE userInfoId = :1", str(currentUser.key().id()))
		contact = contact.get()
							  
		if contact == None:
			contact = ContactInfo(firstName=currentUser.firstName, lastName=currentUser.lastName,
				position='', cellPhoneNumber='', homePhoneNumber='', email=None, street='', city='',
				zip=-1, showPublic=False, userInfoId=str(currentUser.key().id()))
			contact.put()
			time.sleep(0.2)
				
		self.redirect('/add_contact?contactId=%s' % contact.key().id())
	
	"""
	Resets the password to another account. The new password is the same as their username.
	
	returns void
	"""
	def resetOtherAccountPassword(self):
		accessAllowed = self.verifyAdminStatus(userInfo.owner, 'Reset Other Account Password')
		if not accessAllowed:
			return
			
		# Get values
		username = self.request.get('accountUsername')
			
		# Find the user with this name
		userWithName = db.GqlQuery("SELECT * FROM UserInfo "
								   "WHERE username = '%s' " 
								   "LIMIT 1" % username)
		userWithName = userWithName.get()

		# If there is no user with this username, break out
		if userWithName == None:
			error = 'No user with this username.'
			self.renderPageWithContact(accountUsername=username, resetOtherAccountPasswordError=error)
			return
			
		# Reset the user's password in the datastore
		passwordHash = encryption.makeHash(userWithName.username)
		userWithName.passwordHash = passwordHash
		userWithName.put()
		
		time.sleep(1)
		message = 'Account %s has been reset.' % username
		self.renderPageWithContact(resetOtherAccountPasswordMessage=message)
		return
		
		
		
		