# Utility Classes
from handlerBase import Handler

class LoginConfirmationHandler(Handler):
	def renderPage(self, message = ''):
		self.render('loginConfirmation.html', message = message)
		
	def get(self):
		message = "You have been successfully logged in!"
		self.renderPage(message)