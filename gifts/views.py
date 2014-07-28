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

from utils import Signups, create_highrise_account


def splash(request):
	
	inputs = request.POST if request.POST else None
	form = SplashForm(inputs)
	
	try:
		if (inputs) and form.is_valid():
			
			cd = form.cleaned_data
			
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
				
			return HttpResponseRedirect(reverse('confirmation'))
			
		else:
			raise Exception()

	except Exception as err:
		form.errors['__all__'] = form.error_class([err])
		return render_to_response('base_1.html', {'form': form}, context_instance=RequestContext(request))

def confirmation(request):	
	return render_to_response('confirmation.html', {}, context_instance=RequestContext(request))