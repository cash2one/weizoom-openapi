# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
import time

from business.pay.pay import PayLog
from util.error_codes import *

class APay(api_resource.ApiResource):
	"""
	第三方支付
	"""
	app = 'pay'
	resource = 'third_pay'

	@param_required(['woid', 'order_id'])
	def put(args):
		woid = args['woid']
		order_id = args['order_id']
		
		access_token = args['apiserver_access_token']
		timestamp = str(long(time.time() * 1000))
		data = { 'order_id':order_id, 'timestamp':timestamp, 'woid': woid, u'access_token':access_token, 'pay_interface_type':'2'}
		pay_log = PayLog.from_order_id({
			'order_id': args['order_id'],
			})
		if pay_log:
			errcode = PAY_ORDER_STATUS_ERROR
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}

		resp = Resource.use('default').put({
							'resource': 'pay.pay_result',
							'data': data
						})

		status = 0
		code = 0
		errcode= SYSTEM_ERROR_CODE
		# reason= ''
		if resp:
			code = resp["code"]
			if code == 200:
				if resp['data']['is_success'] == True:
					status = 1
					errcode= SUCCESS_CODE
					PayLog.save({
						'woid': args['woid'],
						'order_id': order_id,
						'status': status,
						'appid': args['appid']
						})
				else:
					msg = resp['data']['msg']
					# reason = msg
					if u'非待支付订单' in msg:
						errcode = PAY_ORDER_STATUS_ERROR
					else:
						errcode = PAY_ORDER_ERROR


		if code == 200 and status:
			return {'order_id': order_id}
		else:
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}




