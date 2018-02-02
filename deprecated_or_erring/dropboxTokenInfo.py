import webapp2

from google.appengine.ext import db

# Represents a user
class DropboxTokenInfo(db.Model):
	accessToken = db.StringProperty(required = True)
	accessTokenSecret = db.StringProperty(required = True)