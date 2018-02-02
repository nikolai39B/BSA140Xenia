# GAE libraries
import webapp2
from google.appengine.ext import db

# Represents an individual's contact information
class ContactInfo(db.Model):
	firstName = db.StringProperty(required = True)
	lastName = db.StringProperty(required = True)
	position = db.StringProperty()
	userInfoId = db.StringProperty()
	cellPhoneNumber = db.StringProperty()
	carrier = db.StringProperty()
	sendCellAnnouncement = db.BooleanProperty()
	homePhoneNumber = db.StringProperty()
	email = db.EmailProperty()
	sendEmailAnnouncement = db.BooleanProperty()
	altEmail = db.EmailProperty()
	sendAltEmailAnnouncement = db.BooleanProperty()
	street = db.StringProperty()
	city = db.StringProperty()
	state = db.StringProperty()
	zip = db.IntegerProperty()
	showPublic = db.BooleanProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	
def makePhoneNumberPretty(number):
	return '(%s) %s-%s' % (number[:3], number[3:6], number[6:])
	
	
# List of carriers (deprecated)
# none = ('NO_EMAIL', 'None')
# aTAndT = ('%s@txt.att.net', 'AT&T')
# verizon = ('%s@vtext.com', 'Verizon')
# tMobile = ('1%s@tmomail.net', 'T-Mobile')
# cincinnatiBell = ('%s@gocbw.com', 'Cincinnati Bell')
# sprint = ('%s@messaging.sprintpcs.com', 'Sprint')
# virginMobile = ('%s@vmobl.com', 'Virgin Mobile')
# cingular = ('%s@cingularme.com', 'Cingular')
# nextel = ('%s@messaging.nextel.com', 'Nextel')
# usCellular = ('%s@email.uscc.net', 'US Cellular')
# cricket = ('%s@sms.mycricket.com', 'Cricket')
# tracfone = ('%s@mmst5@tracfone.com', 'TracFone')
# metroPCS = ('%s@mymetropcs.com', 'Metro PCS')
# alltel = ('%s@message.alltel.com', 'Alltel')
# boostMobile = ('%s@myboostmobile.com', 'BoostMobile')
# other = ('NO_EMAIL', 'Other')

# carriers = [
	# none,
	# aTAndT,
	# verizon,
	# tMobile,
	# cincinnatiBell,
	# sprint,
	# virginMobile,
	# cingular,
	# nextel,
	# usCellular,
	# cricket,
	# tracfone,
	# metroPCS,
	# alltel,
	# boostMobile,
	# other
# ]

# List of states
states = [
	'Alabama',
	'Alaska',
	'Arizona',
	'Arkansas', 
	'California', 
	'Colorado', 
	'Connecticut', 
	'Delaware', 
	'Florida', 
	'Georgia', 
	'Hawaii', 
	'Idaho', 
	'Illinois',
	'Indiana', 
	'Iowa',
	'Kansas', 
	'Kentucky', 
	'Louisiana', 
	'Maine', 
	'Maryland', 
	'Massachusetts', 
	'Michigan', 
	'Minnesota', 
	'Mississippi',
	'Missouri', 
	'Montana',
	'Nebraska', 
	'Nevada', 
	'New Hampshire', 
	'New Jersey', 
	'New Mexico', 
	'New York', 
	'North Carolina', 
	'North Dakota', 
	'Ohio',
	'Oklahoma', 
	'Oregon', 
	'Pennsylvania',
	'Rhode Island', 
	'South Carolina', 
	'South Dakota', 
	'Tennessee', 
	'Texas', 
	'Utah', 
	'Vermont', 
	'Virginia', 
	'Washington', 
	'West Virginia', 
	'Wisconsin', 
	'Wyoming',
	'Other'
]
	