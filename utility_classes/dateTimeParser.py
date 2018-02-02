# Python libraries
import datetime
import re

"""
Parses the given string into a DateTime object.

	dateAsStr: the DateTime as a string in the form 'yyyy-mm-ddThh:mm', where yyyy is year, mm is
		month, dd is day, hh is hour, and mm is minute.
		
returns: DateTime
"""
def parseStringToDateTime(dateAsStr):
	#Form: yyyy-mm-ddThh:mm
	try:
		# Pull all of the numbers out of the given string
		date = re.findall(r"[0-9]+", str(dateAsStr))
		
		# Loop through all number strings and convert them to integers
		ii = 0
		for s in date:
			date[ii] = int(s)
			ii += 1
			
		# Assemble and return the new DateTime
		return datetime.datetime(year=date[0], month=date[1], day=date[2], hour=date[3],
			minute=date[4])
	except:
		return None
		
"""
Formats the given DateTime object into a string (parsable by the parseStringToDateTime function.

	dateAsObject: the given DateTime object
	
returns: string
"""
def parseDateTimeToString(dateAsObj):
	#Form: yyyy-mm-ddThh:mm
	try:
		# Assemble and return the new string
		return '%d-%02d-%02dT%02d:%02d' % (dateAsObj.year, dateAsObj.month, dateAsObj.day,
			dateAsObj.hour, dateAsObj.minute)
	except:
		return None