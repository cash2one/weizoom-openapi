#coding: utf8
from eaglet.core.db import models

import datetime

class App(models.Model):
	"""
	
	"""
	appid = models.CharField(max_length=30)
	app_secret = models.CharField(max_length=100)
	woid = models.CharField(max_length=100)
	is_active = models.BooleanField(default=False)
	#TODO copid
	name = models.CharField(max_length=100)
	apiserver_access_token = models.CharField(max_length=256, default="")
	created_at = models.DateTimeField(default=datetime.datetime.now)
	supplier_ids = models.CharField(max_length=256, default="") #alter table poseidon.app add column supplier_ids varchar(256) default "" ;

	class Meta:
		db_table = 'app'
		verbose_name = 'App'
		verbose_name_plural = 'App'


class AccessToken(models.Model):
	app = models.ForeignKey(App)
	access_token = models.CharField(max_length=256)
	expires_in = models.CharField(max_length=100, verbose_name='expires_in')
	is_active = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'access_token'
		verbose_name = 'access_token'
		verbose_name_plural = 'access_token'

class User(models.Model):
	"""
	从django.contrib.auth.User迁移过来
	"""
	username = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30, default='')
	last_name = models.CharField(max_length=30, default='')
	email = models.EmailField(default='')
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True,)
	date_joined = models.DateTimeField(default=datetime.datetime.now)

	class Meta:
		db_table = 'auth_user'
		verbose_name = 'user'
		verbose_name_plural = 'users'
		#abstract = True
