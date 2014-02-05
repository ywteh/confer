from django.db import models

'''
Confer Models

@author: Anant Bhardwaj
@date: Apr 8, 2013
'''


class Conference(models.Model):
  id = models.AutoField(primary_key=True)
  unique_name = models.CharField(max_length=50, unique = True)
  confer_name = models.CharField(max_length=50, unique = True)
  title = models.TextField()
  subtitle = models.TextField()
  blurb = models.TextField()
  location = models.CharField(max_length = 100) 
  start_date = models.DateField()
  end_date = models.DateField()
  hidden = models.BooleanField(default=False)
  admins = models.TextField(default="[]")


  def __unicode__(self):
    return self.unique_name

  class Meta:
    app_label = 'server'
    db_table = "conferences"
    ordering = ["-start_date"]


class User(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  email = models.CharField(max_length=100, unique = True)
  f_name = models.CharField(max_length=50)
  l_name = models.CharField(max_length=50)
  password = models.CharField(max_length=500)
  meetups_enabled = models.BooleanField(default=False)

  def __unicode__(self):
    return self.f_name + ' ' + self.l_name

  class Meta:
    app_label = 'server'
    db_table = "users"


class App(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  app_id = models.CharField (max_length=100, unique = True)
  app_name = models.CharField (max_length=100)
  app_token = models.CharField (max_length=500)
  user = models.ForeignKey ('User')

  def __unicode__(self):
    return self.app_name

  class Meta:
    app_label = 'server'
    db_table = "apps"


class Registration(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  user = models.ForeignKey('User')
  conference = models.ForeignKey('Conference')

  def __unicode__(self):
    return str(self.id)

  class Meta:
    app_label = 'server'
    db_table = "registrations"


class Permission(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  user = models.ForeignKey('User')
  app = models.ForeignKey('App')
  access = models.BooleanField(default=False)


  def __unicode__(self):
    return self.id

  class Meta:
    app_label = 'server'
    db_table = "permissions"


class Likes(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  registration = models.ForeignKey('Registration')
  likes = models.TextField()

  def __unicode__(self):
    return str(self.id)

  class Meta:
    app_label = 'server'
    db_table = "likes"


class Logs(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  registration = models.ForeignKey('Registration')
  action = models.CharField(max_length=50)
  data = models.TextField()

  def __unicode__(self):
    return str(self.id)

  class Meta:
    app_label = 'server'
    db_table = "logs"
    ordering = ["-timestamp"]

