# Python libraries
import logging
import webapp2

# GAE libraries
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import db
from google.appengine.api import mail

# Utility Classes
from handlerBase import Handler

# Database Models
from announcementInfo import AnnouncementInfo
from contactInfo import ContactInfo
import contactInfo
from userInfo import UserInfo
import userInfo

class EmailCatcherHandler(InboundMailHandler, Handler):
	def receive(self, message):
		# Get sender
		sender = message.sender
		logging.info("Received a message from: " + sender)
		
		# Check for an erroneous message to the sender email, and notify the user
		if 'announcesender@bsa140xenia.appspotmail.com' in message.to.lower():
			self.sendAnnounceSenderAlert(str(sender))
			return
		
		# Make sure we caught the right email address
		if not 'announce@bsa140xenia.appspotmail.com' in message.to.lower():
			self.sendBounceAlert(str(sender))
			return

		# Check sender email
		sender = str(sender)
		user = None
		contacts = db.GqlQuery("SELECT * FROM ContactInfo")
		for contact in contacts:
			email = ''
			if contact.email != None:
				email = str(contact.email)
				
			altEmail = ''
			if contact.altEmail != None:
				altEmail = str(contact.altEmail)
				
			#logging.info("%s %s: %s (%s), %s (%s)" % (
			#	contact.firstName, contact.lastName,
			#	email, email in sender and email != '',
			#	altEmail, altEmail in sender and altEmail != ''))
				
			# We use 'in' here because sometimes senders are of the form:
			# Will Hauber <tsdrifter@yahoo.com>, so otherwise they won't be picked up
			# This is slightly dangerous, as a rouge email such as XXXXXtsdrifter@yahoo.com
			# would get through, but honestly it shouldn't be a problem
			if (email in sender and email != '') or (altEmail in sender and altEmail != ''):
				try:
					# Try to get the user for this contact
					user = UserInfo.get_by_id(int(contact.userInfoId))
					if user == None:
						raise Exception
					break
				except:
					logging.info('Contact found for %s (email), but no associated user found.' % sender)
		
		# If the email did not return results, check the cell number
		if user == None:
			senderNumber = sender.split('@')
			senderNumber = senderNumber[0]
			
			# Remove a leading '1' if necessary
			if len(senderNumber) == 11:
				senderNumber = senderNumber[1:]
				
			# If the sender number is not a valid form, break out
			if len(senderNumber) != 10:
				self.sendNoVerifyAlert(str(sender))
				return
			
			contacts = db.GqlQuery("SELECT * FROM ContactInfo")
			
			for contact in contacts:
				if str(contact.cellPhoneNumber) == str(senderNumber):
					try:
						# Try to get the user for this contact
						user = UserInfo.get_by_id(int(contact.userInfoId))
						if user == None:
							raise Exception
						break
					except:
						logging.info('Contact found for %s (cell number), but no associated user found.' % sender)
		
		# If there is no user or if the user doesn't have privileges, log and return
		if user == None:
			self.sendNoVerifyAlert(str(sender))
			return
			
		if user.adminStatus >= userInfo.user:
			logging.info("Sender found in contacts (%s), but no privilege." % user.username)
			self.sendNoPrivilegeAlert(str(sender))
			return
		
		logging.info("Sender found in contacts (%s). Sending announcement." % user.username)
		
		# Get subject
		subject = 'No Subject'
		try:
			subject = message.subject			
			logging.info("Subject: " + subject)
		except AttributeError:
			logging.info("No subject. Proceeding with default subject 'Announcement'")
		if subject == 'No Subject':
			subject = 'Announcement'			
				
		# Attempt to get the content nicely
		bodies = message.bodies('text/plain')
		content = ''
		for contentType, body in bodies:
			content += body.decode()
			
		# If we are here, then there seems to be no content. Just to be safe, parse the raw message.
		# This workaround allows text to announcement to work.
		if content == '':
			logging.info("trying to parse the raw email")
			for part in message.original.walk():
				charset = part.get_content_charset()
				if part.get_content_type() == 'text/plain':
					part_str = part.get_payload(decode=1)
					content += part_str.decode(charset)
		
		# If there is still no content, bail out
		if content == '':
			logging.info("There is no content to this announcement.")
			return
		content = str(content)
			
		logging.info("Content: " + content)
		
		# Create the announcement
		aI = AnnouncementInfo(title=subject, content=content, creatorId=str(user.key().id()))
		aI.put()
		logging.info('Announcement created.')
		
		self.sendAnnouncement(aI)
		return
		
	"""
	Let the recipient know that their message was sent to the announceSender@bsa140xenia.appspotmail.com,
	and that this address cannot send outgoing mail.
	
		recipient: the email address of the person to send the alert to
	
	returns void
	"""
	def sendAnnounceSenderAlert(self, recipient):
		outboundSender = "announceSender@bsa140xenia.appspotmail.com"
		subject = "Announcement Not Sent - Invalid Email"
		message = ("%s,\n\n" % recipient + 
			"You have sent an email to announceSender@bsa140xenia.appspotmail.com. This most often " +
			"occurs by accidentally replying to a previous annoucement. This address is " +
			"not capable of receiving mail. If you wish to send an announcement, please send a " +
			"message to announce@bsa140xenia.appspotmail.com instead." +
			"\n\nThanks,\nBSA Troop 140 Web Administrator")
			
		mail.send_mail(sender=outboundSender, to=recipient, subject=subject, body=message)
		logging.info("Sent announce sender alert to " + recipient)
	
	"""
	Let the recipient know that they we could not verify their contact.
	
		recipient: the email address of the person to send the alert to
	
	returns void
	"""
	def sendNoVerifyAlert(self, recipient):
		outboundSender = "announceSender@bsa140xenia.appspotmail.com"
		subject = "Announcement Not Sent - No Verify"
		message = ("%s,\n\n" % recipient + 
			"You have sent an email to announce@bsa140xenia.appspotmail.com; however, we could " +
			"not verify this contact in our database. As a result, the announcement was not sent. " +
			"Please contact the web administrator for more details." +
			"\n\nThanks,\nBSA Troop 140 Web Administrator")
			
		mail.send_mail(sender=outboundSender, to=recipient, subject=subject, body=message)
		logging.info("Sent no verify alert to " + recipient)
	
	"""
	Let the recipient know that they do not have the privileges to send annoucements.
	
		recipient: the email address of the person to send the alert to
	
	returns void
	"""
	def sendNoPrivilegeAlert(self, recipient):
		outboundSender = "announceSender@bsa140xenia.appspotmail.com"
		subject = "Announcement Not Sent - No Privilege"
		message = ("%s,\n\n" % recipient + 
			"You have sent an email to announce@bsa140xenia.appspotmail.com; however, your " +
			"account does not have adequate privileges to send announcements. Please contact " +
			"the web administrator for more details." +
			"\n\nThanks,\nBSA Troop 140 Web Administrator")
			
		mail.send_mail(sender=outboundSender, to=recipient, subject=subject, body=message)
		logging.info("Sent no privilege alert to " + recipient)
	
	"""
	Let the recipient know we could not handle their email.
	
		recipient: the email address of the person to send the alert to
	
	returns void
	"""
	def sendBounceAlert(self, recipient):
		outboundSender = "announceSender@bsa140xenia.appspotmail.com"
		subject = "Bounce Alert"
		message = ("%s,\n\n" % recipient + 
			"You have sent an email to a bsa140xenia.appspotmail.com domain email that is not " +
			"recognized. Please contact the web administrator for more details." +
			"\n\nThanks,\nBSA Troop 140 Web Administrator")
			
		mail.send_mail(sender=outboundSender, to=recipient, subject=subject, body=message)
		logging.info("Sent bounce alert to " + recipient)
	