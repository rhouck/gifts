from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout
from django.contrib.auth.views import login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.forms.util import ErrorList

import datetime
import json
import ast
from dateutil.parser import parse


from forms import *
from settings import LIVE

from utils import Signups, create_highrise_account, send_email


def splash(request):
	
	inputs = request.POST if request.POST else None
	
	try:
		# select form type
		if (inputs):
			if inputs['type'] == 'Subscribe':
				sub_form = SubscribeForm(inputs)
				con_form = ContactForm()
			else:
				sub_form = SubscribeForm()
				con_form = ContactForm(inputs)
		else:
			sub_form = SubscribeForm()
			con_form = ContactForm()
			raise Exception()
		
		if inputs['type'] == 'Subscribe' and sub_form.is_valid():
			
			cd = sub_form.cleaned_data
			
			# sign up new subscriber
			if inputs['type'] == 'Subscribe':
				# check if email already exists
				existing = Signups.Query.all().filter(email=cd['email'])
				existing = [e for e in existing]
				#return HttpResponse(len(existing))
				if existing:
					raise Exception("Email already registered in system.")
				
				signup = Signups(email=cd['email'])
				if LIVE:
					signup.type = 'live'
				else:
					signup.type = 'test'
				
				signup.highrise_id = create_highrise_account(cd['email'], tag='landing-page')
				signup.save()
					
				return HttpResponseRedirect(reverse('confirmation', kwargs={'message_type': 'subscribe'}))
			
		# submit contact form
		elif inputs['type'] == 'Contact' and con_form.is_valid():	
			
			cd = con_form.cleaned_data
			body = "%s:\n\n%s" % (cd['email'],cd['message'])
			send_email(subject='Inquiry from site', body=body)
			create_highrise_account(cd['email'], tag='contact-form')
			
			return HttpResponseRedirect(reverse('confirmation', kwargs={'message_type': 'contact'}))

		
		else:
			raise Exception()

		if con_form.is_valid():
			cd = form.cleaned_data

	except Exception as err:
		if inputs and inputs['type'] == 'Subscribe':
			sub_form.errors['__all__'] = sub_form.error_class([err])
		elif inputs and inputs['type'] == 'Contact':
			con_form.errors['__all__'] = con_form.error_class([err])
		return render_to_response('splash.html', {'sub_form': sub_form, 'con_form': con_form}, context_instance=RequestContext(request))


def confirmation(request, message_type):
	
	if message_type == 'subscribe':
		message = "Great!</br>We'll reach out as soon as H&S</br>officially launches."
	elif message_type == 'contact':
		message = "Thank you for the message!</br>We'll get back to you ASAP"
	else:
		raise Http404

	inputs = request.POST if request.POST else None
	form = ContactForm(inputs)

	if (inputs) and form.is_valid():

		cd = form.cleaned_data
		body = "%s:\n\n%s" % (cd['email'],cd['message'])
		send_email(subject='Inquiry from site', body=body)
		create_highrise_account(cd['email'], tag='contact-form')


	return render_to_response('confirmation.html', {'message': message, 'con_form': form}, context_instance=RequestContext(request))
