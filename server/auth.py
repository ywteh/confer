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
kFName = "SESSION_F_NAME"
kLName = "SESSION_L_NAME"

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
        request.session[kFName] = user.f_name
        request.session[kLName] = user.l_name
        return HttpResponseRedirect(redirect_url)
      except User.DoesNotExist:
        try:
          User.objects.get(email=login_email)
          errors.append('Wrong password. Please try again.<br /><a class="blue bold" href="/forgot">Click Here</a> to reset your password.')
        except User.DoesNotExist:
          errors.append('Could not find any account associated with email address: <a href="mailto:%s">%s</a>.<br /><a class="blue bold" href="/register">Click Here</a> to create an account.' %(login_email, login_email))
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
      request.session[kFName] = user.f_name
      request.session[kLName] = user.l_name
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
          'Some unknown error happened.'
          'Please try again or send an email to <a href="mailto:confer@csail.mit.edu">confer@csail.mit.edu</a>.')
    
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
          '<a href="mailto:confer@csail.mit.edu">confer@csail.mit.edu</a>')
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
          '<a href="mailto:confer@csail.mit.edu">confer@csail.mit.edu</a>')
    
    c = {'msg_title': 'Confer Reset Password', 'errors': errors} 
    c.update(csrf(request))
    return render_to_response('confirmation.html', c)

@login_required
def settings (request):
  errors = []
  error = False
  redirect_url = '/'

  if('redirect_url' in request.GET.keys()):
    redirect_url = request.GET['redirect_url']

  if request.method == "POST":
    try:
      if('redirect_url' in request.POST.keys()):
        redirect_url = request.POST['redirect_url']

      user_email = request.POST["user_email"].lower()
      meetups = request.POST["meetups_enabled"] 
      user = User.objects.get(email=user_email)
      if meetups == 'enabled':
        user.meetups_enabled = True
      else:
        user.meetups_enabled = False

      user.save()
      return HttpResponseRedirect(redirect_url)
    except Exception, e:
      errors.append(
          'Some unknown error happened. '
          'Please try again or send an email to '
          '<a href="mailto:confer@csail.mit.edu">confer@csail.mit.edu</a>')
      c = {'errors': errors} 
      c.update(csrf(request))
      return render_to_response('settings.html', c)
  else:
    login = get_login()
    user = User.objects.get(email=login)
    meetups_enabled = user.meetups_enabled
    c = {
        'user_email': login[0],
        'login_id': login[0],
        'login_name': login[1],
        'meetups_enabled': meetups_enabled,
        'redirect_url': redirect_url}
    c.update(csrf(request))
    return render_to_response('settings.html', c)


def get_login(request):
  login_id = None
  login_name = ''
  try:
    login_id = request.session[kLogIn]
    login_name = request.session[kName]
  except:
    pass

  return [login_id, login_name]




