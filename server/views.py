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
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''

def home (request):
  try:
    conferences = Conference.objects.all().values()
    login = get_login(request)
    return render_to_response('home.html', {
          'conferences':conferences,
          'login_id': login[0],
          'login_name': login[1]
        }
    )
  except:
    pass

def team (request):
  current_team = json.loads(
      open(p+'/fixtures/' + 'team.json').read())
  past_collaborators = json.loads(
      open(p+'/fixtures/' + 'collaborators.json').read())
  login = get_login(request)
  return render_to_response(
      'team.html', {'current_team': current_team,
      'past_collaborators': past_collaborators,
      'login_id': login[0],
      'login_name': login[1]
    }
  )

def conf (request, conf):
  conf = conf.lower()
  try:
    request.session[kConf] = conf
    Conference.objects.get(unique_name=conf)
    return HttpResponseRedirect('/%s/papers' %(conf))
  except Conference.DoesNotExist:
    try:
      c = Conference.objects.get(confer_name=conf)
      request.session[kConf] = c.unique_name
      return HttpResponseRedirect('/%s/papers' %(c.unique_name))
    except:
      return HttpResponseRedirect('/')
  except:
    return HttpResponseRedirect('/')

def papers (request, conf):
  conf = conf.lower()
  try:
    Conference.objects.get(unique_name=conf)
    request.session[kConf] = conf
    login = get_login(request)
    return render_to_response('papers.html', {
        'conf':conf,
        'login_id': login[0],
        'login_name': login[1]
      }
    )
  except:
    return HttpResponseRedirect('/')
  
  

def schedule (request, conf):
  conf = conf.lower()
  try:
    Conference.objects.get(unique_name=conf)
    request.session[kConf] = conf
    login = get_login(request)
    return render_to_response('schedule.html', {
        'conf':conf,
        'login_id': login[0],
        'login_name': login[1]
      }
    )
  except:
    return HttpResponseRedirect('/')


def paper (request, conf):
  conf = conf.lower()
  try:
    request.session[kConf] = conf
    login = get_login(request)
    return render_to_response('paper.html', {
        'conf':conf,
        'login_id': login[0],
        'login_name': login[1]
      }
    )
  except:
    return HttpResponseRedirect('/')

@login_required
def meetups (request, conf):
  conf = conf.lower()
  try:
    similar_people = []
    request.session[kConf] = conf
    login = get_login(request)
    user = User.objects.get(email=login[0])
    meetups_enabled = user.meetups_enabled
    if meetups_enabled:
      similar_people = get_similar_people(login[0], conf)
    return render_to_response('meetups.html', {
        'conf':conf,
        'similar_people': similar_people,
        'meetups_enabled': meetups_enabled,
        'login_id': login[0],
        'login_name': login[1]
      }
    )
  except Exception, e:
    print e
    return HttpResponseRedirect('/')



@csrf_exempt
def data (request):
  recs = []
  likes = []
  error = False
  msg = 'OK'
  login = None
  login_name = None
  try:
    login = request.session[kLogIn]
    login_name = request.session[kName]
    conf = request.session[kConf]
    registration = get_registration(login, conf)
    data = None

    try:
      data = Likes.objects.get(registration = registration)
    except:
      pass

    if not data or not data.likes:
      default_likes = []
      try:
        prefs = json.loads(
            open(p+'/../data/%s/prefs.json' %(conf)).read())
        name = request.session[kFName] + ' ' + request.session[kLName]
        name = name.lower()
        if name in prefs:
          default_likes = prefs[name]
        else:
          matches = difflib.get_close_matches(name, prefs.keys())
          if len(matches) > 0:
            default_likes = prefs[matches[0]]

      except Exception, e:
        pass

      data = Likes(registration = registration, likes=json.dumps(default_likes))
      data.save()

    likes.extend(json.loads(data.likes))

  except Exception, e:
    error = True
    msg = str(e)

  return HttpResponse(json.dumps({
      'login_id': login,
      'login_name': login_name,
      'recs':recs, 
      'likes':likes,
      'error': error,
      'msg':msg}), mimetype="application/json")


@csrf_exempt
@login_required
def log (request, action):
  try:
    login = request.session[kLogIn]
    conf = request.session[kConf]
    registration = get_registration(login, conf)
    insert_log(registration, action)
    return HttpResponse(
        json.dumps({'error':False}), mimetype="application/json")

  except:
    return HttpResponse(
        json.dumps({'error':True}), mimetype="application/json")


@csrf_exempt
@login_required
def like (request, like_str):
  login = request.session[kLogIn]
  likes = []
  recs = []
  error = False
  msg = "OK"
  try:
    papers = json.loads(request.POST["papers"])
    conf = request.session[kConf]
    registration = get_registration(login, conf)
    data = None
    insert_log(registration, like_str, papers)
    try:
      data = Likes.objects.get(registration = registration)
      likes.extend(json.loads(data.likes))
    except:
      data = Likes(registration = registration, likes = json.dumps([]))
      data.save()   
    
    for paper_id in papers:
      if(like_str=='star' and (paper_id not in likes) and paper_id != ''):
        likes.append(paper_id)
      if(like_str=='unstar' and (paper_id in likes) and paper_id != ''):
        likes.remove(paper_id)

    likes = list(set(likes))    
    data.likes = json.dumps(likes)
    data.save()
    recs = []

  except Exception, e:
    error = True
    msg = str(e)

  return HttpResponse(
    json.dumps({
        'recs':recs,
        'likes':likes,
        'error':error,
        'msg':msg
      }
    ),
    mimetype="application/json"
  )



'''
Confer APIs
'''


@csrf_exempt
def likes (request):
  likes = []
  error = False
  msg = 'OK'
  login = None
  conf = None
  try:
    login = request.POST["login_id"]
    conf = request.POST["conf_id"]
    registration = get_registration(login, conf)
    data = None

    try:
      data = Likes.objects.get(registration = registration)
      likes.extend(json.loads(data.likes))
    except:
      pass

  except Exception, e:
    error = True
    msg = str(e)

  return HttpResponse(json.dumps({
      'login_id': login,
      'conf':conf,
      'likes':likes,
      'error': error,
      'msg':msg}), mimetype="application/json")



@csrf_exempt
def similar_people (request):
  login = None
  similar_people = []
  conf = None
  error = False
  msg = "OK"
  try:
    login = request.POST["login_id"]
    conf = request.POST["conf_id"]

    similar_people = get_similar_people(login, conf)
  
  except Exception, e:
    error = True
    msg = str(e)

  return HttpResponse(json.dumps({
        'login_id': login,
        'conf':conf,
        'similar_people': similar_people,
        'error': error,
        'msg':msg
      }), mimetype="application/json")







