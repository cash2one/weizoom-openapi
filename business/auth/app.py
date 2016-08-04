# -*- coding: utf-8 -*-
"""@package business.auth.app

"""

import json
from bs4 import BeautifulSoup
import math
from datetime import datetime
import time
import urllib

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
import settings
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business import model as business_model
from util import auth_util
import logging
from db.account import models as account_models

class App(business_model.Model):
	"""
	App
	"""
	__slots__ = (
		'id',
		'appid',
		'app_secret',
		'woid',
		'is_active',
		'name'
	)

	@staticmethod
	@param_required(['appid', 'secret'])
	def get(args):
		"""工厂方法

		@param[in] 'appid', 'secret'
		@return App对象
		"""
		app_obj = App.get_from_cache(args)
		return app_obj

	@staticmethod
	@param_required(['model'])
	def from_model(args):
		"""
		
		"""
		model = args['model']

		app = App()
		app._init_slot_from_model(model)
		return app

	@staticmethod
	@param_required(['appid', 'secret'])
	def get_from_cache(args):
		appid = args["appid"]
		secret = args["secret"]
		#TODO from redis
		try:
			db_model = account_models.App.get(appid=appid, app_secret=secret)
			return App.from_model({
				"model": db_model
				})
		except :
		 	return None


	def __init__(self):
		business_model.Model.__init__(self)
