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
from util.error_codes import *
import json
import time



class AExpressDetail(api_resource.ApiResource):
	"""
	获取订单物流信息
	"""
	app = 'mall'
	resource = 'express_details'

	@param_required(['woid', 'order_id'])
	def get(args):

		order_id = args['order_id']
		woid = args['woid']
		access_token = args['apiserver_access_token']
		timestamp = str(long(time.time() * 1000))
		data = {
			'timestamp':timestamp, 'woid': woid, 'order_id':order_id,u'access_token':access_token
			}
		resp = Resource.use('default').get({
							'resource': 'mall.express_details',
							'data': data
			})


		errcode = SUCCESS_CODE

		if resp:
			code = resp["code"]
			if code == 200:
				order_detail = {}
				data = resp["data"]
				
				for express_detail in data['express_details']:
					for i in ['express_id', 'ftime', 'status', 'id', 'created_at']:
						del express_detail[i]
				return {'express':data}

			if code == 500:
				# msg = '获取物流信息请求参数错误或缺少参数'
				errcode = GET_EXPRESS_DETAILS_PARAMETER_ERROR
				watchdog.error("get express detail failed!! errcode:{}, msg:{}".format(errcode,unicode_full_stack()),log_type='OPENAPI_ORDER')
				return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		else:
			errcode = SYSTEM_ERROR_CODE
			watchdog.error("get express detail failed!! errcode:{}, msg:{}".format(errcode,unicode_full_stack()),log_type='OPENAPI_ORDER')
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		

