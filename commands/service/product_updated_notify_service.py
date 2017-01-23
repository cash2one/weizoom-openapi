# -*- coding: utf-8 -*-
"""
发送钉钉消息

@author bert
"""
import logging
import settings
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog
from commands.handler_register import register
from eaglet.utils.resource_client import Resource
from db.customer import models as customer_models
from db.account import models as account_models
from db.notify import models as notify_models
from util.error_codes import *

import time
import json
import datetime
import requests
import hashlib
# from error_codes.py import *

@register("product_updated")
def process(data, raw_msg=None):
	"""
	商品更新后需通知客户
	请求args:
	woids:自营平台的账户ID
	product_id: 商品的ID
	注意：该消息来源于两部分：
	1、zeus的商品更新按钮和批量同步按钮，都走的module_api的ship_order函数
	2、zeus部分：mall/order_state.py里面的ship()函数
	"""
	try:
		# 从panda获取woids可能会有多个
		woids_list_str = data.get('woids', '[]')
		logging.info("================================woids_list_str:{}".format(woids_list_str))
		woids_list = json.loads(woids_list_str)
		if not woids_list:
			logging.info("==========product_updated=======woid is not openapi's woid====pass===========")
			return
		# 从panda获取product_ids可能会有多个
		product_id = data.get("product_id", None)
		logging.info("================================product_id:{}".format(product_id))
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
		data = {'product_id': product_id}
		for account_info in account_infos:
			app_id = account_info.app_id
			if app_id:
				customer_message = customer_models.CustomerMessage.select().dj_where(app_id=appid).first()
				interface_url = customer_message.interface_url
				msg_id = "%s%s" %(time.time(), product_id)
				message = "update product--product_id: %s, woids:%s"%(product_id,woids_list_str)
				# 单独处理看购平台的发货通知
				if 'apiv.kangou.cn' in interface_url:
					# 看购平台的发货通知的回调
					# http://testapi.kangou.cn/weizoon/XMlmessage/kangweb?data=123&sign=a96db7b8a2483fca057610072fd16ce6
					# sign=md5($key+md5('param1=value1&param2=value2&param3=value3'+$key)) ;
					# $key = "5ec252518c0796f83cb412e9c5d36d57"
					interface_url += "callback/kangweb"
					data['operation'] = 'edit'
					logging.info('===================interface_url======================={}'.format(interface_url))
					key = '5ec252518c0796f83cb412e9c5d36d57'
					mw_one = hashlib.md5("product_id={}".format(product_id)+key)
					mw_two =hashlib.md5(key+ mw_one.hexdigest())
					sign = mw_two.hexdigest()
					data['sign'] = sign
					logging.info("================================message:{}".format(message))
					logging.info("================================sign:{}".format(sign))

				resp = requests.post(interface_url, data=data, timeout=30)

				status = 0
				if resp.status_code == 200:
					status = 1
					logging.info('===================success======================={}{}'.format(repr(resp.url),repr(resp.text)))
				else:
					logging.info('===================failed======================={}{}'.format(repr(resp.url),repr(resp.text)))

				notify_model = notify_models.NotifyMessage(
					msg_id=msg_id,
					type=notify_models.TYPE_UPDATED,
					message=message,
					status=status,
					created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				)
				notify_model.save()
	except Exception as e:
		logging.info(u"Service Exception:--product_updated_notify_service {}".format(unicode_full_stack()))