import logging
import webapp2
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

# Utility Classes
from handlerBase import Handler

class LogSenderHandler(InboundMailHandler):
	#def post(self):
	#	logging.info("Post request recieved!?!?!?!?!")
	
	def receive(self, mail_message):
		logging.info("Received a message from: " + mail_message.sender)
		
# app = webapp.WSGIApplication([LogSenderHandler.mapping()], debug=True)

# def main():
    # run_wsgi_app(application)
# if __name__ == "__main__":
    # main()