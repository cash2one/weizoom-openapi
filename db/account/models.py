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
	created_at = models.DateTimeField(default=datetime.datetime.now)

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