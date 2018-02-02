# Utility Classes
from handlerBase import Handler

class DatabaseHandler(Handler):
	def renderPage(self):
		self.render('bsaDatabase.html')
		
	def get(self):
		self.renderPage()