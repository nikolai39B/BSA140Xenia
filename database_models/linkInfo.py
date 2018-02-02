# GAE libraries
import webapp2
from google.appengine.ext import db

# Represents an link on the /links page
class LinkInfo(db.Model):
	title = db.StringProperty(required = True)
	link = db.StringProperty(required = True)
	description = db.TextProperty()
	showPublic = db.BooleanProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)