# Utility Classes
from handlerBase import Handler

class PageErrorHandler(Handler):
	def renderPage(self, error='Error'):
		self.render('pageError.html', error=error)

	def get(self):
		# Display the page with the generic 404 error message
		error = 'The requested page could not be found.'
		self.renderPage(error)