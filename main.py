#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Import the basic python libraries
import os
import sys

# Import the GAE specific libraries
import jinja2
import webapp2
from google.appengine.ext import db

# Add the folder paths to the system path for future imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'webpage_handlers'))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'utility_classes'))
sys.path.insert(2, os.path.join(os.path.dirname(__file__), 'database_models'))

# Import the page handers
from homepage import HomepageHandler
from login import LoginHandler
from loginConfirmation import LoginConfirmationHandler
from logout import LogoutHandler
from events import EventsHandler
from eventsCondensed import EventsCondensedHandler
from event import EventHandler
from photos import PhotosHandler
from photo import PhotoHandler
from addPhotos import AddPhotosHandler
from editPhoto import EditPhotoHandler
from deletePhoto import DeletePhotoHandler
from bsaDatabase import DatabaseHandler
from contact import ContactHandler
from addContact import AddContactHandler
from searchContacts import SearchContactsHandler
from deleteContact import DeleteContactHandler
from createAccount import CreateAccountHandler
from createAccountConfirmation import CreateAccountConfirmationHandler
from unauthorized import UnauthorizedHandler
from newEvent import NewEventHandler
from deleteEvent import DeleteEventHandler
from account import AccountHandler
from links import LinksHandler
from deleteLink import DeleteLinkHandler
from files import FilesHandler
from editFile import EditFileHandler
from deleteFile import DeleteFileHandler
from downloadFile import DownloadFileHandler
from announcements import AnnouncementsHandler
from editAnnouncement import EditAnnouncementHandler
from deleteAnnouncement import DeleteAnnouncementHandler
from announcementContacts import AnnouncementContactsHandler
from emailCatcher import EmailCatcherHandler

from pageError import PageErrorHandler

# Create the mapping from urls to webapp handlers
urlMap = [
	('/', HomepageHandler),
	('/login', LoginHandler),
	('/login_confirmation', LoginConfirmationHandler),
	('/logout', LogoutHandler),
	('/events', EventsHandler),
	('/events_condensed', EventsCondensedHandler),
	('/event/([^/]+)?', EventHandler),
	('/photos', PhotosHandler),
	('/photo/([^/]+)?', PhotoHandler),
	('/add_photos', AddPhotosHandler),
	('/add_photos/([^/]+)?', AddPhotosHandler),
	('/edit_photo/([^/]+)?', EditPhotoHandler),
	('/delete_photo/([^/]+)?', DeletePhotoHandler),
	('/database', DatabaseHandler),
	('/contact', ContactHandler),
	('/add_contact', AddContactHandler),
	('/search_contacts', SearchContactsHandler),
	('/delete_contact', DeleteContactHandler),
	('/create_account', CreateAccountHandler),
	('/create_account_confirmation', CreateAccountConfirmationHandler),
	('/unauthorized', UnauthorizedHandler),
	('/new_event', NewEventHandler),
	('/delete_event', DeleteEventHandler),
	('/account', AccountHandler),
	('/links', LinksHandler),
	('/delete_link', DeleteLinkHandler),
	('/files', FilesHandler),
	('/edit_file/([^/]+)?', EditFileHandler),
	('/delete_file/([^/]+)?', DeleteFileHandler),
	('/download_file/([^/]+)?', DownloadFileHandler),
	('/announcements', AnnouncementsHandler),
	('/edit_announcement', EditAnnouncementHandler),
	('/delete_announcement', DeleteAnnouncementHandler),
	('/announcement_contacts', AnnouncementContactsHandler),
	EmailCatcherHandler.mapping(),
	
	# This handler must be at the end, as it catches all 404 error pages
	('/.*', PageErrorHandler)
]

# Initialize the app
app = webapp2.WSGIApplication(urlMap, debug=True)