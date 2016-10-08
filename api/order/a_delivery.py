# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
import json
import time

from util.error_codes import *

class ADelivery(api_resource.ApiResource):
	"""
	发货
	"""
	app = 'mall'
	resource = 'delivery'

	@param_required(['order_id', 'express_company_name', 'express_number'],)
	def put(args):


		order_id = args['order_id']
		express_company_name = args['express_company_name']
		express_number = args['express_number']

		data = {
				'order_id': order_id,
				'express_company_name': express_company_name,
				'express_number': express_number
				}
		resp = Resource.use('zeus').put({
			'resource':'mall.delivery',
			'data': data
			})
		errcode = SYSTEM_ERROR_CODE
		if resp:
			if resp['code'] == 200:
				if resp['data']['result'] == 'SUCCESS':
					errcode = SUCCESS_CODE
				else:
					if resp['data']['msg'] == u'不能对当前订单发货':
						errcode = DELIVERY_ORDER_HAS_MULTIPLE_CHILD_ORDERS
					elif resp['data']['msg'] == u'订单状态已经改变':
						errcode = DELIVERY_ORDER_STATUS_ERROR
					elif resp['data']['msg'] == u'订单不存在':
						errcode = DELIVERY_ORDER_NOT_EXIST
					watchdog.info("delivery failed!! errcode:{}, order_id:{}".format(errcode,order_id),log_type='OPENAPI_ORDER')

		if errcode == SYSTEM_ERROR_CODE:
			watchdog.error("delivery failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
		return {'errcode': errcode}
