import dropbox

from handlerBase import Handler
from dropboxInfo import DropboxInfo
from dropboxTokenInfo import DropboxTokenInfo

from google.appengine.ext import db
from google.appengine.api import memcache

class SyncDropboxConfirmationHandler(Handler):
	def renderPage(self, message=''):
		self.render('syncDropboxConfirmation.html', message=message)

	def get(self):
		accessAllowed = self.verifyAdminStatus(0, 'Sync Dropbox')
		if not accessAllowed:
			return
		
		message = ''
		#try:
			# Get the token
		cli = memcache.Client()
		session = cli.gets("session")
			
		token = session.obtain_access_token()
			
			# Remove any stored tokens and add the new token
		db.delete(DropboxTokenInfo.all())			
		dTI = DropboxTokenInfo(accessToken=token.key, accessTokenSecret=token.secret)
		dTI.put();
		
			# Test that everything worked by opening a client
		dInfo = DropboxInfo()
		client = dInfo.getClient()
		
		message = 'The dropbox was successfully synced.'
		#except:
		#	message = 'The dropbox could not be synced. Please try again later.'

		self.renderPage(message)