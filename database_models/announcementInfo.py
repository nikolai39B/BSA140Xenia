# Python libraries
import datetime

# GAE libraries
import webapp2
from google.appengine.ext import db

# Represents a file object in the datastore
class AnnouncementInfo(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	creatorId = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	
dateFormat = '%m/%d/%y'
timeFormat = '%I:%M %p'

def getCompensatedDatetime(dt):
	return dt - datetime.timedelta(hours=4)