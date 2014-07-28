from parse_rest.datatypes import Object
import datetime
from django.utils.timezone import utc
from random import choice
import pyrise

from settings import HIGHRISE_CONFIG, DEFAULT_FROM_EMAIL

from django.core.mail import send_mail

def send_email(to_email, subject, body):

	send_mail(subject, body, DEFAULT_FROM_EMAIL,[to_email], fail_silently=False)
	return True

def gen_alphanum_key():
    key = ''
    for i in range(6):
        key += choice(string.lowercase + string.uppercase + string.digits)
    return key

def current_time_aware():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class Signups(Object):
    pass

def create_highrise_account(email, tag=None):
	
	pyrise.Highrise.set_server(HIGHRISE_CONFIG['server'])
	pyrise.Highrise.auth(HIGHRISE_CONFIG['auth'])

	try:

		cust = pyrise.Person()

		cust.contact_data = pyrise.ContactData(email_addresses=[pyrise.EmailAddress(address=email, location='Home'),],)

		cust.first_name = email

		cust.save()
		
		if tag:
			cust.add_tag(tag)

		return cust.id
		
	except:
	    
	    return None

