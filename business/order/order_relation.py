# -*- coding: utf-8 -*-
"""
@package db.notify.models
通知信息表结构

@author bert
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
from db.order import models as order_models

class OrderRelation(business_model.Model):
	"""
	OrderRelation
	"""
	__slots__ = (
		# 'id', #mongo的id是objectid
		'woid',
		'deal_id',
		'order_id',
		'products',
		'status',
		'created_at',
		'errcode',
		'reason',

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

		order_relation = OrderRelation()
		order_relation._init_slot_from_model(model)
		return order_relation

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
	@param_required(['woid', 'deal_id', 'order_id', 'products', 'status','errcode', 'reason'])
	def save(args):
		order_relation_model = order_models.OrderRelation(
			woid=args['woid'],
			deal_id=args['deal_id'],
			order_id=args['order_id'],
			products=args['products'],
			status=args['status'],
			errcode=args['errcode'],
			reason=args['reason']
			)
		order_relation_model.save()
		order_relaion = OrderRelation.from_model({'model':order_relation_model})
		return order_relaion
	#todo id使用额外参数的方式添加