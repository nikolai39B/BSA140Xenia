# Python libraries
import datetime
import time

# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler
import encryption

class LoginHandler(Handler):
	def renderPage(self, username = "", error = "", stayLoggedIn=""):
		self.render('login.html', username = username, error = error, stayLoggedIn=stayLoggedIn)
		
	def get(self):
		self.renderPage()
		
	def post(self):
		# Get username, password, verify, and email
		username = self.request.get("username")
		password = self.request.get("password")
		stayLoggedIn = self.request.get("stayLoggedIn")
		
		# Pause (to make hacking more difficult)
		time.sleep(0.5)
		
		# Ensure the user entered both a username and a password
		if username == '' or password == '':
			error = 'Enter both a username and a password to log in.'
			self.renderPage(username, error, stayLoggedIn)
			return
		
		# Find user in database
		user = db.GqlQuery("SELECT * FROM UserInfo "
						   "WHERE username = '%s' " 
						   "LIMIT 1" % username)
		user = user.get()
		
		# If the user does not exist, display the error
		if user == None:
			error = "Invalid username or password."
			self.renderPage(username, error, stayLoggedIn)
			return
			
		# Check the password against the database
		validPassword = encryption.isHashValid(password, user.passwordHash)
		
		# If the password is invalid, display the error
		if not validPassword:
			error = "Invalid username or password."
			self.renderPage(username, error, stayLoggedIn)
			return
		
		# If the login info is valid, set the cookie and redirect to the login confirmation page
		usernameHash = encryption.makeHash(username)
		
		# Set expire time base on stayLoggedIn flag
		if stayLoggedIn != "":
			expireTime = datetime.datetime.now() + datetime.timedelta(weeks = 4)
			self.response.set_cookie('user', '%s|%s' % (str(username), usernameHash),  path='/',
				expires=expireTime)
		else:
			self.response.set_cookie('user', '%s|%s' % (str(username), usernameHash),  path='/')
			
		self.redirect('/login_confirmation')