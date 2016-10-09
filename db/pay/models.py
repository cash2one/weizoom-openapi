#coding: utf8
"""
@package db.notify.models
通知信息表结构

@author bert
"""
import mongoengine as models

import datetime

class PaymentLog(models.Document):
	"""
	支付记录表
	"""
	woid = models.LongField()
	order_id = models.StringField(default='', max_length=50)  #订单的order_id
	status = models.IntField() #支付状态，成功或者失败 0支付失败 1支付成功
	# errcode = models.IntField() #向第三方的返回码
	# reason = models.StringField() #来自apiserver的返回结果的详细信息
	created_at = models.DateTimeField(default=datetime.datetime.now()) #创建时间
	
	meta = {
		'collection': 'mall_payment_log',
		'db_alias': 'open'
	}
