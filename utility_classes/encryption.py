# Python libraries
import os
import random
import hashlib
import string

secret = 'ed5ea900ca13341bf6e01a686cce850e3c100be62fd7b3489178d5fe802a3a4e'

# Class that contains all cookie encryption functionality
#class Encryption:
"""
Makes a random 5 character long salt

returns: string
"""
def makeSalt():
	saltLength = 32
	return ''.join(random.choice(string.letters) for x in xrange(saltLength))

"""
Makes a hash from a given value and salt. If no salt if provided, one is generated.

	value: the value for which to make a hash
	salt: the (optional) salt string
	
returns: string
"""
def makeHash(value, salt = None):
	if not salt:
		salt = makeSalt()
	h = hashlib.sha256(value + secret + salt).hexdigest()
	return '%s|%s' % (h, salt)

"""
Tests if the hash is valid for the given value.

	value: the string value to test
	h: the hash and salt delimited by a pipe
	
returns: boolean
"""
def isHashValid(value, h):
	salt = h.split('|')[1]
	return h == makeHash(value, salt)
	
"""
Returns the username from the hash if the hash is valid. The hash should be of the form u|h|s,
where 'u' is the username, 'h' is the hash, and 's' is the salt.

	h: the hash from which to pull the username

returns: string (or None)
"""
def getCurrentUserFromHash(h):
	username = ""
	hash = ""
	salt = ""
	cookieElements = []
	try:
		# Split the hash into its three sections
		cookieElements = h.split('|')
		username = cookieElements[0]
		hash = cookieElements[1]
		salt = cookieElements[2]
		
	# If the cookie is not valid, return false
	except:
		return None
	else:
		if not isHashValid(username, '%s|%s' % (hash, salt)):
			return None
			
	return username