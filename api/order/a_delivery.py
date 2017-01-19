# -*- coding: utf-8 -*-
"""
@package db.notify.models
通知信息表结构

@author bert
"""

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from openapi_mns_conf import TOPIC
from business.pay.pay import PayLog
import json
import time
from bdem import msgutil

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
		data_mns = []

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

		# 获取app_id传送到mns进行消息处理
		pay_log = PayLog.from_order_id({
			"order_id": order_id
			})
		if pay_log:
			app_id = pay_log.appid
		else:
			watchdog.info("order paylog is not exits, delivery mns message send  failed!!  order_id:{}, msg:{}".format(order_id, unicode_full_stack()),log_type='OPENAPI_ORDER')
			errcode = DELIVERY_ORDER_HAS_NO_PAYLOG
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		topic_name = TOPIC['delivery_service']
		data_mns['order_id'] = order_id
		data_mns['app_id'] = app_id or ''
		data_mns['express_company_name'] = express_company_name
		data_mns['express_number'] = express_number
		if resp:
			if resp['code'] == 200:
				if resp['data']['result'] == 'SUCCESS':
					errcode = SUCCESS_CODE
					data = {'errcode': errcode}
					msgutil.send_message(topic_name, 'send_order_delivered_notify_service', data)
					return data
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
		return {'errcode':errcode, 'errmsg':code2msg[errcode]}
