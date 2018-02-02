# GAE libraries
from google.appengine.ext import db

# Utility Classes
from handlerBase import Handler

# Database Models
from userInfo import UserInfo

class CreateAccountConfirmationHandler(Handler):
	def renderPage(self, message = ''):
		self.render('createAccountConfirmation.html', message = message)
		
	def get(self):
		# Get the first and last name for the user 
		firstName = self.request.get('f')
		lastName = self.request.get('l')
		
		# Look up the user in the datastore
		userWithName = db.GqlQuery("SELECT * FROM UserInfo "
								   "WHERE firstName = '%s' and lastName = '%s' "
								   "LIMIT 1" % (firstName, lastName))
		userWithName = userWithName.get()
		
		message = ''
		
		# If the user was found, display the success message
		if (userWithName != None):
			message = "The account for %s %s was successfully created." % (firstName, lastName)
			
		# If the user was not found, display the error. (This could occur if the datastore is running slow
		#	and the entry hasn't quite been added yet. Refreshing the page will not resend the form, but
		#	will recheck the datastore.		
		else:
			message = "Error: there is no account for %s %s. Try refreshing the page." % (firstName,
				lastName)
			
		self.renderPage(message)