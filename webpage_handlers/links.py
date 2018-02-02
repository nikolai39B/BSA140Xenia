# Python libraries
import time
import re

# GAE libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler

# Database Models
from linkInfo import LinkInfo
import userInfo

class LinksHandler(Handler):
	def renderPage(self, links='', title='', link='', public='', description='', error='', newLink=True):
		self.render('links.html', links=links, title=title, link=link, public=public, 
			description=description, error=error, newLink=newLink)

	def get(self):
		# Get the link id to edit
		linkObj = None
		try:
			id = int(self.request.get('id'))
			linkObj = LinkInfo.get_by_id(id)
		except:
			pass
		
		
		if linkObj == None:
			self.renderPage(links=self.getLinks())
			
		else:
			title = linkObj.title
			link = linkObj.link
			description = linkObj.description
			public = linkObj.showPublic
			if public:
				public = 'checked'
			else:
				public = ''
			self.renderPage(links=self.getLinks(), title=title, link=link, public=public,
				description=description, newLink=False)
		
	def post(self):
		# Ensure the user can add links
		accessAllowed = self.verifyAdminStatus(userInfo.poster, 'Add Link')
		if not accessAllowed:
			return
		
		# Get the link to edit
		linkObj = None
		try:
			id = int(self.request.get('id'))
			linkObj = LinkInfo.get_by_id(id)
		except:
			pass
		
		# Get the values for the link
		title = self.request.get('title')
		link = self.request.get('link')
		public = self.request.get('public')
		description = self.request.get('description')
		
		error = ''
		
		# Check the entries to make sure they are valid
		reLink = '^[^\.\s]+\.\S+$'
		reHttp = '^https?://'
		
		if title == '':
			error += 'Please provide a title for the link.<br>'
			
		if link == '':
			error += 'Please provide the url for the link.<br>'
			
		elif not re.match(reLink, link):
			error += 'Please provide a valid url for the link.<br>'
			
		# Add http:// to the front if necessary
		elif not re.match(reHttp, link):
			link = 'http://' + link
			
		if error != '':
			self.renderPage(links=self.getLinks(), title=title, link=link, public=public,
				description=description, error=error, newLink=(linkObj == None))
		
		else:			
			# If there is no object to edit, create a new one
			if linkObj == None:
				linkObj = LinkInfo(title=title, link=link, description=description,
					showPublic=(public != ''))
			
			# Otherwise, edit the current object
			else:
				linkObj.title = title
				linkObj.link = link
				linkObj.description = description
				linkObj.showPublic = (public != '')
				
			linkObj.put()
			
			time.sleep(0.2)
			self.redirect('/links')			
			
	"""
	This function generates the 
	
	returns: string
	"""
	def getLinks(self):
		# Determine if the user is signed in
		signedIn = False
		if self.getCurrentUser() != None:
			signedIn = True
		
	
		# Get the links and generate the html
		links = db.GqlQuery("SELECT * from LinkInfo "
							"ORDER BY title")
			
		linksHtml = ''
		for link in links:
			# Skip the link if it is private and the user is not signed in
			if not link.showPublic and not signedIn:
				continue
		
			linksHtml += self.renderStr('link.html', link=link, displayLinkbar=True)
		
		return linksHtml