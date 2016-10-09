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
from db.pay import models as pay_models

class PaymentLog(business_model.Model):
	"""
	Pay
	"""
	__slots__ = (
		# 'id', #mongo的id是objectid
		'woid',
		'order_id',
		'status',
		# 'errcode',
		# 'reason',
		'created_at',
	)


	@staticmethod
	@param_required(['model'])
	def from_model(args):
		"""
		
		"""
		model = args['model']
		pay_log = PaymentLog()
		pay_log._init_slot_from_model(model)
		return pay_log




	def __init__(self):
		business_model.Model.__init__(self)

	@staticmethod
	@param_required(['woid','order_id'])
	def from_order_id(args):
		payment_log_models = pay_models.PaymentLog.objects(
			woid=args['woid'],
			order_id=args['order_id'],
			)
		if payment_log_models.count() > 0:
			payment_log_model = payment_log_models.first()
			payment_log = PaymentLog.from_model({'model':payment_log_model})
		else:
			payment_log = ''
		return payment_log

	def update_status(self):
		pay_models.PaymentLog.objects(woid=self.woid,order_id=self.order_id,).update(status=1)

	@staticmethod
	@param_required(['woid','order_id', 'status'])
	def save(args):
		payment_log_model = pay_models.PaymentLog(
			woid=args['woid'],
			order_id=args['order_id'],
			status=args['status'],
			)
		payment_log_model.save()
		payment_log = PaymentLog.from_model({'model':payment_log_model})
		return payment_log
