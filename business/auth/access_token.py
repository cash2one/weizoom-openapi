# -*- coding: utf-8 -*-
"""@package business.account.access_token
业务层内部使用的业务对象，access_token的信息，主要与redis缓存中的帐号数据对应

"""

import json
from bs4 import BeautifulSoup
import math
from datetime import datetime
import time
import urllib
import hashlib

from eaglet.decorator import param_required
from eaglet.core.cache import utils as cache_util
import settings
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from business import model as business_model
from util import auth_util
import logging
from db.account import models as account_models

class AccessToken(business_model.Model):
	"""
	access_token信息
	"""
	__slots__ = (
		'expires_in',
		'access_token'
	)

	@staticmethod
	@param_required(['app'])
	def put(args):
		"""工厂方法

		@param[in] app
		@return AccessToken对象
		"""
		app = args['app']
		access_token = auth_util.encrypt_access_token(app.appid, app.app_secret)
		db_model = account_models.AccessToken.create(
			app=app.id, 
			access_token=access_token,
			expires_in='7200 '
			)
		print ">>>>>>>>>>!"
		cache_util.set_cache_wrapper(hashlib.md5(access_token).hexdigest(),json.dumps(app.to_dict()) ,7200)
		print ">>>>>>>>>>>@"
		return AccessToken.from_model({
			"model": db_model
			})
		

	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	@param_required(['model'])
	def from_model(args):
		"""
		工厂对象，根据member model获取integral业务对象

		@param[in] webapp_owner
		@param[in] model: integral model

		@return Member业务对象
		"""
		model = args['model']

		access_token = AccessToken()
		access_token._init_slot_from_model(model)
		return access_token
	
	