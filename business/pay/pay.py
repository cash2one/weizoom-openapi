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
from db.pay import models as pay_models

class PayLog(business_model.Model):
	"""
	Pay
	"""
	__slots__ = (
		# 'id', #mongo的id是objectid
		'woid',
		'order_id',
		'status',
		'errcode',
		'reason',
		'created_at',

	)

	# @staticmethod
	# @param_required(['appid', 'secret'])
	# def get(args):
	# 	"""工厂方法

	# 	@param[in] 'appid', 'secret'
	# 	@return App对象
	# 	"""
	# 	app_obj = App.get_from_cache(args)
	# 	return app_obj

	@staticmethod
	@param_required(['model'])
	def from_model(args):
		"""
		
		"""
		model = args['model']

		pay_log = PayLog()
		pay_log._init_slot_from_model(model)
		return pay_log

	# @staticmethod
	# @param_required(['appid', 'secret'])
	# def get_from_cache(args):
	# 	appid = args["appid"]
	# 	secret = args["secret"]
	# 	#TODO from redis
	# 	try:
	# 		db_model = account_models.App.get(appid=appid, app_secret=secret)
	# 		return App.from_model({
	# 			"model": db_model
	# 			})
	# 	except :
	# 	 	return None


	def __init__(self):
		business_model.Model.__init__(self)


	@staticmethod
	@param_required(['woid','order_id', 'status','errcode', 'reason'])
	def save(args):
		pay_log_model = pay_models.PayLog(
			woid=args['woid'],
			order_id=args['order_id'],
			status=args['status'],
			errcode=args['errcode'],
			reason=args['reason']
			)
		pay_log_model.save()
		pay_log = PayLog.from_model({'model':pay_log_model})
		return pay_log
	#todo id使用额外参数的方式添加