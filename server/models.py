from django.db import models

'''
Confer Models

@author: Anant Bhardwaj
@date: Apr 8, 2013
'''


class Conference(models.Model):
	id = models.AutoField(primary_key=True)
	unique_name = models.CharField(max_length=50, unique = True)
	name = models.CharField(max_length=50)
	year = models.IntegerField()
	month = models.IntegerField()
	description = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'server'
		db_table = "conferences"


class User(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.CharField(max_length=100, unique = True)
	f_name = models.CharField(max_length=50)
	l_name = models.CharField(max_length=50)
	password = models.CharField(max_length=500)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'server'
		db_table = "users"


class Registration(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey('User')
	conference = models.ForeignKey('Conference')

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'server'
		db_table = "registrations"


class Likes(models.Model):
	id = models.AutoField(primary_key=True)
	registration = models.ForeignKey('Registration')
	likes = models.TextField()

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'server'
		db_table = "likes"


class Logs(models.Model):
	id = models.AutoField(primary_key=True)
	registration = models.ForeignKey('Registration')
	action = models.CharField(max_length=50)
	data = models.TextField()

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'server'
		db_table = "logs"

