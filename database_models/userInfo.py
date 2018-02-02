# GAE libraries
import webapp2
from google.appengine.ext import db

# User admin status values (lower represents more permissions)
owner = 0
admin = 1
poster = 2
user = 3
loggedOut = 4

# Represents a user
class UserInfo(db.Model):
	firstName = db.StringProperty(required = True)
	lastName = db.StringProperty(required = True)
	username = db.StringProperty(required = True)
	passwordHash = db.StringProperty(required = True)
	adminStatus = db.IntegerProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)