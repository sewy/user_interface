from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from django.contrib import messages

# Create your models here.

class UsersManager(models.Manager):
	def validate(self, post):
		if len(post['name']) < 3:
			return (False, 'error1')
		elif len(post['username']) < 3:
			return (False, 'error2')
		elif len(post['password']) < 8:
			return (False, 'error3')
		elif post['password'] != post['c_password']:
			return (False, 'error4')
		try:
			if Users.objects.filter(username=post['username'])[0]:
				return (False, 'error5')
		except:
			return (True, post)

	def adduser(self, post):
		Users.objects.create(name=post['name'], username=post['username'], password=bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt(12)))

	def errormessage(self,request, error):
		errorlist={
			'error1': 'Name must be at least 3 characters',
			'error2': 'Username must be at least 3 characters',
			'error3': 'Password must be at least 8 characters',
			'error4': 'Passwords must match',
			'error5': 'That Username is already registered',
			'error6': 'Wrong Email or Password',
			'error7': 'You must enter a destination',
			'error8': 'You must enter a description',
			'error9': 'You must enter from/to dates',
		}
		messages.add_message(request, messages.ERROR, errorlist[error])

	def login(self, post):
		try:
			user = Users.objects.get(username=post['username'])
			if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password.encode():
				return (True, user)
			else:
				return (False, 'error6')
		except:
			return (False, 'error6')
class TravelsManager(models.Manager):
	def addtravel(self, form_data, userid):
		if len(form_data['destination']) < 1:
			return (False, 'error7')
		elif len(form_data['description']) < 1:
			return (False, 'error8')
		elif len(form_data['date_from']) < 1: 
			return (False, 'error9')
		elif len(form_data['date_to']) < 1:
			return (False, 'error9')
		else:
			Travels.objects.create(user=Users.objects.get(id=userid), destination=form_data['destination'], description=form_data['description'], date_from=form_data['date_from'],date_to=form_data['date_to'])
			return (True, form_data)

class TravelslistManager(models.Manager):
	def jointravel(self, userid, travelid):
		Travelslist.objects.create(user=Users.objects.get(id=userid), travel=Travels.objects.get(id=travelid))

class Users(models.Model):
	name = models.CharField(max_length=30)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UsersManager()

class Travels(models.Model):
	user = models.ForeignKey('Users')
	destination = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	date_from = models.CharField(max_length=200)
	date_to = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TravelsManager()

class Travelslist(models.Model):
	user = models.ForeignKey('Users')
	travel = models.ForeignKey('Travels')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TravelslistManager()