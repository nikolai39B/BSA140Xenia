# Utility Classes
from handlerBase import Handler

class UnauthorizedHandler(Handler):
	def renderPage(self, page = ""):
		# If a page is provided, edit the formatting slightly and add it to the template
		if page != '':
			page = ' (%s)' % page
		self.render('unauthorized.html', page = page)
		
	def get(self):
		# Get the page name of the redirecting page
		page = self.request.get('p')
		self.renderPage(page)