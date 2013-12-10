import json, sys, re, hashlib, smtplib, base64, urllib, os, difflib

from auth import *
from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.db.utils import IntegrityError

from utils import *
from models import *

p = os.path.abspath(os.path.dirname(__file__))
if(os.path.abspath(p+"/..") not in sys.path):
  sys.path.append(os.path.abspath(p+"/.."))

'''
@author: Ted Benson <eob@csail.mit.edu>
@date: Dec 10, 2013
'''

def papersCts(request, conf):
  conf = conf.lower()
  try:
    Conference.objects.get(unique_name=conf)
    return render_to_response('widget/papers.cts', {
      'csslink': None,
      'widgetlink': None,
      'paperslink': None
    })
  except:
    return HttpResponseRedirect('/')
  
def papersWidget(request, conf):
  conf = conf.lower()
  try:
    Conference.objects.get(unique_name=conf)
    return render_to_response('widget/papersWidget.html', {
      'paperslink': None
    })
  except:
    return HttpResponseRedirect('/')
 
