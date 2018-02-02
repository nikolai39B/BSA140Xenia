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

class CreateAccountHandler(Handler):
	def renderPage(self, firstName = '', lastName = '', username = '', error = '', defaultAdminStatus = 3):
		self.render('createAccount.html', firstName = firstName, lastName = lastName, username = username, 
		error = error, defaultAdminStatus = defaultAdminStatus)
		
	def get(self):
		accessAllowed = self.verifyAdminStatus(userInfo.admin, 'Create Account')
		if not accessAllowed:
			return
		
		self.renderPage()
		
	def post(self):	
		accessAllowed = self.verifyAdminStatus(userInfo.admin, 'Create Account')
		if not accessAllowed:
			return
		
		# Get all the account information
		firstName = self.request.get('firstName')
		lastName = self.request.get('lastName')
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		adminStatus = int(self.request.get('adminStatus'))
		
		# Define string conditions
		error = ''
		minLength = 4;
		maxLength = 25;
		reStringUsername = "^[A-Za-z0-9_-]{%s,%s}$" % (minLength, maxLength)
		reStringPassword = "^.{%s,%s}$" % (minLength, maxLength)
		
		# First and last names must be all letters
		if firstName == '' or (not firstName.isalpha()):
			error += 'No first name/invalid first name provided.<br>'
		if lastName == '' or (not lastName.isalpha()):
			error += 'No last name/invalid last name provided.<br>'
			
		# Username must follow reStringUsername regular expression
		if not re.match(reStringUsername, username):
			error += 'No username/invalid username provided. Username must be between 4 and 25 characters.<br>'
		
		# Username must be unique
		userWithSameName = db.GqlQuery("SELECT * FROM UserInfo "
									   "WHERE username = '%s' " 
									"LIMIT 1" % username)
		userWithSameName = userWithSameName.get()
		if userWithSameName != None:
			error += "Another user already has this username.<br>"
			
		# Password must follow reStringPassword regular expression
		if not re.match(reStringPassword, password):
			error += 'No password/invalid password provided. Password must be between 4 and 25 characters.<br>'
			
		# Verify must match password
		if verify != password:
			error += 'Password and verify do not match.<br>'
			
		# Admin status must be between 1 and 3 (to create owners, edit this property from the GAE
		#	datastore viewer
		if adminStatus < userInfo.admin or adminStatus > userInfo.user:
			error += 'Error parsing admin status.<br>'
		
		# If there are errors, display them
		if (error != ''):
			self.renderPage(firstName, lastName, username, error, adminStatus)
		
		# If there are no errors, create the account and redirect to the welcome page
		else:
			passwordHash = encryption.makeHash(password)
			ui = UserInfo(firstName = firstName, lastName = lastName, username = username,
				passwordHash = passwordHash, adminStatus = adminStatus)
			ui.put()
			
			time.sleep(1)
			self.redirect('/create_account_confirmation?f=%s&l=%s' % (firstName, lastName))
			