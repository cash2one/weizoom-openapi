# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
import json
import time

class ADelivery(api_resource.ApiResource):
	"""
	发货
	"""
	app = 'mall'
	resource = 'delivery'

	@param_required(['order_id', 'express_company_name', 'express_number'],)
	def post(args):


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
		errcode = 995995
		if resp:
			if resp['code'] == 200:
				if resp['data']['result'] == 'SUCCESS':
					errcode = 0
				else:
					if resp['data']['msg'] == u'不能对当前订单发货':
						errcode = 0
					elif resp['data']['msg'] == u'订单状态已经改变':
						errcode = 0
		return {'errcode': errcode}
