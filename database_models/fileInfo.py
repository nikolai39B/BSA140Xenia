# GAE libraries
import webapp2
from google.appengine.ext import db

# Represents a file object in the datastore
class FileInfo(db.Model):
	title = db.StringProperty(required = True)
	blobKey = db.StringProperty(required = True)
	description = db.TextProperty()
	created = db.DateTimeProperty(auto_now_add = True)