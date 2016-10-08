import json, sys, re, hashlib, smtplib, base64, urllib, os

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
#from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

from multiprocessing import Pool

from utils import *
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

# for async calls
pool = Pool(processes=1)  

'''
LOGIN/REGISTER/RESET
'''
def login_required (f):
  def wrap (request, *args, **kwargs):
      if kLogIn not in request.session.keys():        
        redirect_url = urlquote_plus(request.get_full_path())        
        return HttpResponseRedirect("/login?redirect_url=%s" %(redirect_url))
      return f(request, *args, **kwargs)
  wrap.__doc__ = f.__doc__
  wrap.__name__ = f.__name__
  return wrap


def login_form (request, redirect_url='/', errors=[]):
  c = {
      'redirect_url':redirect_url, 
      'errors':errors, 
      'values':getattr(request, request.method, {})
  }
  c.update(csrf(request))
  return render_to_response('login.html', c)


def register_form (request, redirect_url='/', errors=[]):
  c = {
      'redirect_url':redirect_url, 
      'errors':errors, 
      'values':getattr(request, request.method, {})
  }
  c.update(csrf(request))
  return render_to_response('register.html', c)


def login (request):
  redirect_url = '/'
  reqmethod = getattr(request,request.method)
  if('redirect_url' in reqmethod.keys()):
    redirect_url = urllib.unquote_plus(reqmethod['redirect_url'])

  if not redirect_url or redirect_url == '':
    redirect_url = '/'

  if request.method == "POST":
    errors = []
    login_email = ''

    try:
      login_email = request.POST["login_email"].lower()
      login_password = hashlib.sha1(request.POST["login_password"]).hexdigest()
      user = User.objects.get(email=login_email, password=login_password)
      clear_session(request)
      request.session[kLogIn] = user.email
      request.session[kName] = user.f_name
      request.session[kFName] = user.f_name
      request.session[kLName] = user.l_name
      return HttpResponseRedirect(redirect_url)
    except User.DoesNotExist:
      try:
        User.objects.get(email=login_email)
        errors.append(
            'Wrong password. Please try again.<br /><br />'
            '<a class="blue bold" href="/forgot?email=%s">Click Here</a> '
            'to reset your password.' %(urllib.quote_plus(login_email)))
      except User.DoesNotExist:
        errors.append(
            'Could not find any account associated with email address: '
            '<a href="mailto:%s">%s</a>.<br /><br /><a class="blue bold" '
            'href="/register?redirect_url=%s&email=%s">Click Here</a> '
            'to create an account.' %(login_email, login_email,
                urllib.quote_plus(redirect_url), urllib.quote_plus(login_email)))
      return login_form(
          request, redirect_url = urllib.quote_plus(redirect_url),
          errors = errors) 
    except:
      errors.append('Login failed.')
      return login_form(
          request, redirect_url = urllib.quote_plus(redirect_url),
          errors = errors)          
  else:
    try:
      if request.session[kLogIn]:
        return HttpResponseRedirect(redirect_url)
      else:
        return login_form(request, urllib.quote_plus(redirect_url))
    except:
      return login_form(request, urllib.quote_plus(redirect_url))

email_re = re.compile(
  r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
  # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
  r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
  r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)'  # domain
  r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE)  # ipv4 

def register (request):
  redirect_url = '/'
  reqmethod = getattr(request,request.method)
  if('redirect_url' in reqmethod.keys()):
    redirect_url = urllib.unquote_plus(reqmethod['redirect_url'])

  if not redirect_url or redirect_url == '':
    redirect_url = '/'

  if request.method == "POST":
    errors = []
    email = ''
    try:
      error = False

      email = request.POST["email"].lower()
      password = request.POST["password"]
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

      if(error):
        return register_form(request, redirect_url = urllib.quote_plus(redirect_url), errors = errors)

      hashed_password = hashlib.sha1(password).hexdigest()
      user = User(email=email, password=hashed_password, f_name=f_name, l_name=l_name)
      user.save()
      clear_session(request)
      request.session[kLogIn] = user.email
      request.session[kName] = user.f_name
      request.session[kFName] = user.f_name
      request.session[kLName] = user.l_name

      encrypted_email = encrypt_text(user.email)

      subject = "Welcome to Confer"

      msg_body = '''
      Dear %s,

      Thanks for registering to Confer. 

      Please click the link below to start using Confer:

      http://confer.csail.mit.edu/verify/%s

      ''' % (user.f_name + ' ' + user.l_name, encrypted_email)

      pool.apply_async(send_email, [user.email, subject, msg_body])

      return HttpResponseRedirect(redirect_url)
    except IntegrityError:
      errors.append(
          'Account already exists. Please <a class="blue bold" href="/login?login_email=%s">Log In</a>.'
          % (urllib.quote_plus(email)))
      return register_form(request, redirect_url = urllib.quote_plus(redirect_url), errors = errors)
    except:
      errors.append("Some error happened while trying to create an account. Please try again.")
      return register_form(request, redirect_url = urllib.quote_plus(redirect_url), errors = errors)
  else:
      return register_form(request, redirect_url = urllib.quote_plus(redirect_url))


def clear_session (request):
  request.session.flush()
  if kLogIn in request.session.keys():
    del request.session[kLogIn]
  if kName in request.session.keys():
    del request.session[kName]
  if kFName in request.session.keys():
    del request.session[kFName]
  if kLName in request.session.keys():
    del request.session[kLName]


def logout (request):
  clear_session(request)
  c = {
    'msg_title': 'Thank you for using Confer!',
    'msg_body': 'Your have been logged out.<br /><br /><ul><li><a class= "blue bold" href="/home">Click Here</a> to browse confer as guest.<br/><br /></li><li><a class= "blue bold" href="/login">Click Here</a> to log in again.</li></ul>'
  } 
  c.update(csrf(request))
  return render_to_response('confirmation.html', c)


def forgot (request):
  if request.method == "POST":
    errors = []
    try:
      user_email = request.POST["email"].lower()
      User.objects.get(email=user_email)

      encrypted_email = encrypt_text(user_email)

      subject = "Confer Password Reset"

      msg_body = '''
      Dear %s,

      Please click the link below to reset your confer password:

      http://confer.csail.mit.edu/reset/%s

      ''' % (user_email, encrypted_email)

      pool.apply_async(send_email, [user_email, subject, msg_body])

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
          'Please try again or send an email to '
          '<a href="mailto:confer@csail.mit.edu">confer@csail.mit.edu</a>.')
    
    c = {'errors': errors, 'values': request.POST} 
    c.update(csrf(request))
    return render_to_response('forgot.html', c)
  else:
    c = {'values': request.GET} 
    c.update(csrf(request))
    return render_to_response('forgot.html', c)

def verify (request, encrypted_email):
  errors = []
  c = {'msg_title': 'Confer Account Verification'}
  try:
    user_email = decrypt_text(encrypted_email)
    user = User.objects.get(email=user_email)
    c.update({
        'msg_body': 'Thanks for verifying your email address! <a class= "blue bold" href="/home">Click Here</a> to start using Confer.'
    })
    clear_session(request)
    request.session[kLogIn] = user.email
    request.session[kName] = user.f_name
    request.session[kFName] = user.f_name
    request.session[kLName] = user.l_name
  except:
    errors.append(
        'Wrong verify code in the URL. '
        'Please try again or send an email to '
        '<a href="mailto:confer@csail.mit.edu">confer@csail.mit.edu</a>')
  
  c.update({'errors': errors})
  c.update(csrf(request))
  return render_to_response('confirmation.html', c)


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


def get_login(request):
  login_id = None
  user = None
  try:
    login_id = request.session[kLogIn]
    user = User.objects.get(email=login_id)
  except:
    pass

  return [login_id, user]



