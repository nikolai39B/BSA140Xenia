# Utility Classes
from handlerBase import Handler

class LogoutHandler(Handler):
	def get(self):
		# Delete the user cookie (effectively logging the user out) and redirect to the home page
		self.response.set_cookie('user', '')
		self.redirect('/')