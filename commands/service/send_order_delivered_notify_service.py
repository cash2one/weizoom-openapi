# -*- coding: utf-8 -*-
"""
发送钉钉消息

@author bert
"""
import logging
import settings
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog
from commands.service_register import register
from business.pay.pay import PayLog

from db.notify import models as notify_models
from db.customer import models as customer_models

import time
import requests
import hashlib

MESSAGE = """
		<xml>
		<OrderId><![CDATA[{}]]></OrderId>
		<ExpressCompanyName><![CDATA[{}]]></ExpressCompanyName> 
		<ExpressNumber><![CDATA[{}]]></ExpressNumber>
		<Type><![CDATA[{}]]></Type>
		<MsgId>{}</MsgId>
		</xml>
		"""


@register("ship_order")
def send_order_delivered_notify_service(data, raw_msg=None):
	"""
	创建用户的service

	args格式
	```
	{
	"function":"delivered",
	"args":{
	"content":"wtf?",
	"uuid": "80035247"
	}
	}
	```

	@param args dict格式的参数
	"""
	order_id = data.get("order_id", None)
	logging.info(">>>>>>>>>>")
	if order_id:
		pay_log = PayLog.from_order_id({
			"order_id": order_id
			})
		if pay_log:
			customer_message = customer_models.CustomerMessage.objects.get(app_id=pay_log.appid)
			interface_url = customer_message.interface_url

			msg_id = "%s%s" %(int(time.time()), order_id)
			express_company_name = data["express_company_name"]
			express_number = data["express_number"]
			express_company_name = data["express_company_name"]
			message = MESSAGE.format(order_id, express_company_name, express_number, notify_models.TYPE_DELIVERED, msg_id)
			xml_data = dict()
			xml_data['message'] = message
			if 'apiv.kangou.cn' in interface_url:
				# 看购平台的发货通知的回调
				# http://testapi.kangou.cn/weizoon/XMlmessage/kangweb?data=123&sign=a96db7b8a2483fca057610072fd16ce6
				# sign=md5($key.md5('param1=value1&param2=value2&param3=value3'.$key)) ;
				# $key = "5ec252518c0796f83cb412e9c5d36d57"
				if 'ExpressCompanyName' in interface_url:
					interface_url += "/XMlmessage/kangweb"
					key = '5ec252518c0796f83cb412e9c5d36d57'
					mw_one = hashlib.md5("message={}".format(message)+'.'+key)
					mw_two =hashlib.md5(key+'.'+ mw_one.hexdigest())
					sign = mw_two.hexdigest()
					xml_data['sign'] = sign
					
			headers = {'Content-Type': 'application/xml'}
			resp = requests.post(interface_url, data=xml_data, timeout="30", headers=headers)

			status = 0
			if resp.status_code == 200:
				status = 1

			notify_models.NotifyMessage.save({
					"msg_id": msg_id,
					"type": notify_models.TYPE_DELIVERED,
					"message": message,
					"status": status
				})