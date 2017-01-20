# -*- coding: utf-8 -*-
"""
发送钉钉消息

@author bert
"""
import logging
import settings
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog
from handler_register import register
from eaglet.utils.resource_client import Resource
from db.customer import models as customer_models
from db.account import models as account_models

import time
import requests
import hashlib
# from error_codes.py import *

@register("product_updated_notify_service")
def process(data, raw_msg=None):
	"""
	商品更新后需通知客户
	"""
	# 从panda获取woids可能会有多个
	woids_list_str = data.get('woids', '[]')
	woids_list = json.loads(woids_list)
	# 从panda获取product_ids可能会有多个
	product_id = data.get("product_id", None)
	account_infos = account_models.App.select().dj_where(woid_in=woids_list)
	
	# apiserver_access_token = account_info.apiserver_access_token
	# product_list = []
	# if apiserver_access_token and product_id:
	# 	for id in product_id.split('|'):
	# 		resp = Resource.use('openapi').get({
	# 			"resource": 'mall.product',
	# 			"data": {
	# 				'woid': woid,
	# 				'product_id': product_id,
	# 				'apiserver_access_token': apiserver_access_token
	# 			}
	# 		})
	# 		if not resp or resp['code'] != 200:
	#			data['errcode'] = FAIL_GET_PRODUCT_UPDATE_NOTIFY_CODE
	#			data['errmsg'] = code2msg[FAIL_GET_PRODUCT_UPDATE_NOTIFY_CODE]
	#			watchdog.info("product updated notify failed,can not get new product info!!  product_id:{}, msg:{}".format(product_id, unicode_full_stack()),log_type='OPENAPI_PRODUCT_UPDATE_NOTIFY')
	#		else:
	#			product = resp['data']
	#			product_list.append(product)

    # 准备发送回调的数据
	# data = {'product_list':product_list}
	data = {'product_ids':'|'.join(product_ids)}
	for account_info in account_infos:
		app_id = account_info.app_id
		if app_id:
			customer_message = customer_models.CustomerMessage.select().dj_where(app_id=appid)
			interface_url = customer_message.interface_url
			# 单独处理看购平台的发货通知
			if 'apiv.kangou.cn' in interface_url:
				# 看购平台的发货通知的回调
				# http://testapi.kangou.cn/weizoon/XMlmessage/kangweb?data=123&sign=a96db7b8a2483fca057610072fd16ce6
				# sign=md5($key+md5('param1=value1&param2=value2&param3=value3'+$key)) ;
				# $key = "5ec252518c0796f83cb412e9c5d36d57"
				interface_url += "callback/kangweb"
				key = '5ec252518c0796f83cb412e9c5d36d57'
				mw_one = hashlib.md5("product_ids={}".format(product_ids)+key)
				mw_two =hashlib.md5(key+ mw_one.hexdigest())
				sign = mw_two.hexdigest()
				data['sign'] = sign

			resp = requests.post(interface_url, data=data, timeout=30)

			status = 0
			if resp.status_code == 200:
				status = 1

			notify_models.NotifyMessage.save({
					"msg_id": msg_id,
					"type": notify_models.TYPE_DELIVERED,
					"message": message,
					"status": status
				})