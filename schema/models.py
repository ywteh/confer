from django.db import models

'''
Confer Models

@author: Anant Bhardwaj
@date: Apr 8, 2013
'''

class User(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.CharField(max_length=100, unique = True)
	f_name = models.CharField(max_length=50)
	l_name = models.CharField(max_length=50)
	password = models.CharField(max_length=500)

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "users"




class Likes(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey('User')
	likes = models.TextField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "likes"


class Logs(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey('User')
	action = models.CharField(max_length=50)
	data = models.TextField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "logs"

