import dropbox

from google.appengine.ext import db

app_key = 'r35rb9wf4h4rp4b'
app_secret = '5pdlce9sah7bxg8'

class DropboxInfo():
	def getSessionWithToken(self):
		token = db.GqlQuery("SELECT * FROM DropboxTokenInfo "
							"LIMIT 1")
		token = token.get()
	
		session = dropbox.session.DropboxSession(app_key, app_secret, 'dropbox')
		session.set_token(token.accessToken, token.accessTokenSecret)
		return session
	
	def getAuthorizeUrlAndSession(self):
		session = dropbox.session.DropboxSession(app_key, app_secret, 'dropbox')
		request_token = session.obtain_request_token()	
		authorize_url = session.build_authorize_url(request_token,
			'http://localhost:8083/sync_dropbox_confirmation')
		return authorize_url, session

	def getClient(self):
		client = dropbox.client.DropboxClient(self.getSessionWithToken())
		return client