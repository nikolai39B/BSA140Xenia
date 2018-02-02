#import dropbox
import time

from handlerBase import Handler
#from dropboxInfo import DropboxInfo

from google.appengine.api import memcache

class SyncDropboxHandler(Handler):
	def renderPage(self):
		self.render('syncDropbox.html')

	def get(self):
		accessAllowed = self.verifyAdminStatus(0, 'Sync Dropbox')
		if not accessAllowed:
			return
			
		self.renderPage();
	"""
	def post(self):
		accessAllowed = self.verifyAdminStatus(0, 'Sync Dropbox')
		if not accessAllowed:
			return
			
		memcache.delete("session")
		
		dInfo = DropboxInfo()
		authorizeUrl, session = dInfo.getAuthorizeUrlAndSession()
		
		memcache.add(key="session", value=session)
		
		self.redirect(authorizeUrl)
		return
	"""