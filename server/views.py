import json, sys, re, hashlib, smtplib, base64, urllib, os

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

from utils.view_utils import *
from models import *

p = os.path.abspath(os.path.dirname(__file__))
if(os.path.abspath(p+"/..") not in sys.path):
	sys.path.append(os.path.abspath(p+"/.."))


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''

kLogIn = "SESSION_LOGIN"
kConf = "SESSION_CONF"
kName = "SESSION_NAME"

'''
LOGIN/REGISTER/RESET
'''
def login_required (f):
    def wrap (request, *args, **kwargs):
        if kLogIn not in request.session.keys():
        	if(len(args)>0):
        		redirect_url = urlquote_plus("/%s/%s" %(args[0], f.__name__))
        	else:
        		redirect_url = "/"
        	return HttpResponseRedirect("/login?redirect_url=%s" %(redirect_url))
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def login_form (request, redirect_url='/', errors=[]):
    c = {'redirect_url':redirect_url, 'errors':errors}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def register_form (request, redirect_url='/', errors=[]):
    c = {'redirect_url':redirect_url, 'errors':errors}
    c.update(csrf(request))
    return render_to_response('register.html', c)


def login (request):
    redirect_url = '/'
    if('redirect_url' in request.GET.keys()):
    	redirect_url = request.GET['redirect_url']

    if not redirect_url or redirect_url == '':
      redirect_url = '/'

    if request.method == "POST":
    	errors = []
    	if('redirect_url' in request.POST.keys()):
    		redirect_url = request.POST['redirect_url']
        try:
            login_email = request.POST["login_email"].lower()
            login_password = hashlib.sha1(request.POST["login_password"]).hexdigest()
            user = User.objects.get(email=login_email, password=login_password)
            request.session.flush()
            request.session[kLogIn] = user.email
            request.session[kName] = user.f_name
            return HttpResponseRedirect(redirect_url)
        except User.DoesNotExist:
        	try:
        		User.objects.get(email=login_email)
        		errors.append('Wrong password.')
        	except User.DoesNotExist:
        		errors.append("Couldn't locate account with email address: %s" %(login_email))
        	return login_form(request, redirect_url = redirect_url, errors = errors) 
        except:
            errors.append('Login failed.')
            return login_form(request, redirect_url = redirect_url, errors = errors)          
    else:
        return login_form(request, redirect_url)

def register (request):
    redirect_url = '/'
    if('redirect_url' in request.GET.keys()):
    	redirect_url = request.GET['redirect_url']
    if request.method == "POST":
    	errors = []
        try:
            error = False
            if('redirect_url' in request.POST.keys()):
				redirect_url = request.POST['redirect_url']
            email = request.POST["email"].lower()
            password = request.POST["password"]
            password2 = request.POST["password2"]
            f_name = request.POST["f_name"]
            l_name = request.POST["l_name"]
            if(email_re.match(email.strip()) == None):
            	errors.append("Invalid Email.")
            	error = True
            if(f_name.strip() == ""):
            	errors.append("Empty First Name.")
            	error = True
            if(l_name.strip() == ""):
            	errors.append("Empty Last Name.")
            	error = True
            if(password == ""):
            	errors.append("Empty Password.")
            	error = True
            if(password2 != password):
            	errors.append("Password and Confirm Password don't match.")
            	error = True

            if(error):
            	return register_form(request, redirect_url = redirect_url, errors = errors)
            hashed_password = hashlib.sha1(password).hexdigest()
            user = User(email=email, password=hashed_password, f_name=f_name, l_name=l_name)
            user.save()
            request.session.flush()
            request.session[kLogIn] = user.email
            request.session[kName] = user.f_name
            return HttpResponseRedirect(redirect_url)
        except IntegrityError:
            errors.append("Account already exists. Please Log In.")
            return register_form(request, redirect_url = redirect_url, errors = errors)
        except:
            errors.append("Some error happened while trying to create an account. Please try again.")
            return register_form(request, redirect_url = redirect_url, errors = errors)
    else:
        return register_form(request, redirect_url = redirect_url)


def logout (request):
    request.session.flush()
    if kLogIn in request.session.keys():
    	del request.session[kLogIn]
    if kName in request.session.keys():
    	del request.session[kName]
    return HttpResponseRedirect('/')


def forgot (request):
  if request.method == "POST":
    errors = []
    try:
      user_email = request.POST["user_email"].lower()
      User.objects.get(email=user_email)

      decrypted_email = encrypt_text(user_email)

      subject = "Confer Password Reset"

      msg_body = '''
      Dear %s,

      Please click the link below to reset your confer password:

      http://confer.csail.mit.edu/reset/%s

      ''' % (user_email, decrypted_email)

      send_email(user_email, subject, msg_body)

      c = {
        'msg_title': 'Confer Reset Password',
        'msg_body': 'A link to reset your password has been sent to your email address.'
      } 
      c.update(csrf(request))

      return render_to_response('confirmation.html', c)

    except User.DoesNotExist:
      errors.append(
          "Invalid Email Address.")
    except:
      errors.append(
          "Some unknown error happened."
          "Please try again or send an email to confer@csail.mit.edu.")
    
    c = {'errors': errors} 
    c.update(csrf(request))
    return render_to_response('forgot.html', c)
  else:
    return render_to_response('forgot.html', csrf(request))


def reset (request, encrypted_email):
  errors = []
  error = False
  if request.method == "POST":
    try:
      user_email = request.POST["user_email"].lower()
      password = request.POST["new_password"]
      password2 = request.POST["new_password2"]

      if password == "":
        errors.append("Empty Password.")
        error = True

      if password2 != password:
        errors.append("Password and Confirm Password don't match.")
        error = True

      if error:
        c = {
          'user_email': user_email,
          'encrypted_email': encrypted_email,
          'errors': errors
        }
        c.update(csrf(request))
        return render_to_response('reset.html', c)

      else:
        hashed_password = hashlib.sha1(password).hexdigest()
        user = User.objects.get(email=user_email)
        user.password = hashed_password
        user.save()
        c = {
          'msg_title': 'Confer Reset Password',
          'msg_body': 'Your password has been changed successfully.'
        } 
        c.update(csrf(request))
        return render_to_response('confirmation.html', c)
    except:
      errors.append(
          'Some unknown error happened. '
          'Please try again or send an email to '
          'confer@csail.mit.edu.')
      c = {'errors': errors} 
      c.update(csrf(request))
      return render_to_response('reset.html', c)
  else:
    try:
      user_email = decrypt_text(encrypted_email)
      User.objects.get(email=user_email)
      c = {
          'user_email': user_email,
          'encrypted_email': encrypted_email
      }
      c.update(csrf(request))
      return render_to_response('reset.html', c)
    except:
      errors.append(
          'Wrong reset code in the URL. '
          'Please try again or send an email to '
          'confer@csail.mit.edu.')
    
    c = {'msg_title': 'Confer Reset Password', 'errors': errors} 
    c.update(csrf(request))
    return render_to_response('confirmation.html', c)

@login_required
def settings (request):
  errors = []
  error = False
  if request.method == "POST":
    try:
      user_email = request.POST["user_email"].lower()
      meetups = request.POST["meetups_enabled"] 
      user = User.objects.get(email=user_email)
      if meetups == 'enabled':
        user.meetups_enabled = True
      else:
        user.meetups_enabled = False

      user.save()
      c = {
        'msg_title': 'Confer Account Settings',
        'msg_body': 'Your settings have been updated successfully.'
      } 
      c.update(csrf(request))
      return render_to_response('confirmation.html', c)
    except Exception, e:
      errors.append(
          'Some unknown error happened. '
          'Please try again or send an email to '
          'confer@csail.mit.edu.')
      c = {'errors': errors} 
      c.update(csrf(request))
      return render_to_response('settings.html', c)
  else:
    login = request.session[kLogIn]
    user = User.objects.get(email=login)
    meetups_enabled = user.meetups_enabled
    c = {'user_email': login, 'meetups_enabled': meetups_enabled}
    c.update(csrf(request))
    return render_to_response('settings.html', c)


'''
PAGES
'''

def home (request):
	try:
		conferences = Conference.objects.all().values()
		return render_to_response('home.html', {'conferences':conferences})
	except:
		pass

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

@login_required
def papers (request, conf):
	conf = conf.lower()
	try:
		Conference.objects.get(unique_name=conf)
		request.session[kConf] = conf
		return render_to_response('papers.html', {'conf':conf})
	except:
		return HttpResponseRedirect('/')
	
	

@login_required
def schedule (request, conf):
	conf = conf.lower()
	try:
		Conference.objects.get(unique_name=conf)
		request.session[kConf] = conf
		return render_to_response('schedule.html', {'conf':conf})
	except:
		return HttpResponseRedirect('/')


@login_required
def paper (request, conf):
	conf = conf.lower()
	try:
		request.session[kConf] = conf
		return render_to_response('paper.html', 
		{'conf':conf})
	except:
		return HttpResponseRedirect('/')

@login_required
def meetups (request, conf):
  conf = conf.lower()
  try:
    similar_people = []
    request.session[kConf] = conf
    login = request.session[kLogIn]
    user = User.objects.get(email=login)
    meetups_enabled = user.meetups_enabled
    if meetups_enabled:
      similar_people = get_similar_people(login, conf)
    return render_to_response('meetups.html', {
        'conf':conf,
        'similar_people': similar_people,
        'meetups_enabled': meetups_enabled
    })
  except Exception, e:
    print e
    return HttpResponseRedirect('/')


'''
AJAX Calls
'''

@csrf_exempt
@login_required
def data (request):
	recs = []
	likes = []
	login = request.session[kLogIn]
	error = False
	msg = 'OK'
	try:
		conf = request.session[kConf]
		registration = get_registration(login, conf)
		data = None
		try:
			data = Likes.objects.get(registration = registration)
		except:
			data = Likes(registration = registration, likes = json.dumps([]))
			data.save()
		l = data.likes
		if(l!=None):
			likes.extend(json.loads(l))
		else:
			data.likes = json.dumps([])
			data.save()
		#print likes
		#print recs
	except:
		error = True
		e_type, value, tb = sys.exc_info()
		msg = value.message
	return HttpResponse(json.dumps({
			'login_id': login,
			'login_name': request.session[kName],
			'recs':recs, 
			'likes':likes,
			'error': error,
			'msg':msg
			}), mimetype="application/json")



@csrf_exempt
def get_recs (request):
	try:
		papers = json.loads(request.POST["papers"])
		recs = []
		return HttpResponse(json.dumps(recs), mimetype="application/json")
	except:
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")

@csrf_exempt
def log (request, action):
	try:
		login = request.session[kLogIn]
		conf = request.session[kConf]
		registration = get_registration(login, conf)
		insert_log(registration, action)
		return HttpResponse(json.dumps({'error':False}), mimetype="application/json")
	except:
		print sys.exc_info()
		return HttpResponse(json.dumps({'error':True}), mimetype="application/json")



@csrf_exempt
def like (request, like_str):
	login = request.session[kLogIn]
	likes = []
	res = {}
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

		l = list(set(likes))		
		data.likes = json.dumps(l)
		data.save()
		recs = []
	except:
		error = True
		e_type, value, tb = sys.exc_info()
		msg = value.message
	return HttpResponse(json.dumps({'recs':recs, 'likes':l, 'error':error, 'msg':msg}), mimetype="application/json")




