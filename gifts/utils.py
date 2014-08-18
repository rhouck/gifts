from parse_rest.datatypes import Object
import datetime
from django.utils.timezone import utc
from random import choice
import pyrise
import string

from settings import HIGHRISE_CONFIG, DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, LIVE

from django.core.mail import send_mail, get_connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from inlinestyler.utils import inline_css

def send_welcome_email(to_email, count, ref):

    plaintext = get_template('email_template/plain_text.txt')
    htmly     = get_template('email_template/index.html')
    d = Context({'count': count, 'ref': ref})
    subject = "Great move | Surprisr"
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    
    html_content = inline_css(html_content)

    connection = get_connection(username=DEFAULT_FROM_EMAIL, password=EMAIL_HOST_PASSWORD, fail_silently=False)
    if LIVE:
    	msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [to_email], [HIGHRISE_CONFIG['email']], connection=connection)
    else:
    	msg = EmailMultiAlternatives(subject, text_content, DEFAULT_FROM_EMAIL, [to_email], connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def gen_alphanum_key():
    key = ''
    for i in range(8):
        key += choice(string.uppercase + string.lowercase + string.digits)
    return key

def send_email(subject, body, to_email=DEFAULT_FROM_EMAIL):

	send_mail(subject, body, DEFAULT_FROM_EMAIL,[to_email], fail_silently=False)
	return True


def current_time_aware():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


class Signups(Object):
    pass
class Referrals(Object):
    pass
class Counter(Object):
    pass

def get_count():

	count = Counter.Query.all()
	cur = None
	for c in count:
		cur = c
	
	try:
		cur.count += 1
		cur.save()
	except:
		pass
	
	return cur.count

def get_signup_by_ref(ref):
	signup = Signups.Query.get(ref=str(ref))
	return signup



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

