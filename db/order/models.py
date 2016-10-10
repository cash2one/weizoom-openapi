#coding: utf8
"""
@package db.notify.models
通知信息表结构

@author bert
"""
import mongoengine as models

import datetime

class OrderRelation(models.Document):
	"""
	订单关系表
	记录第三方的deal_id和云商通创建的order的order_id
	"""
	woid = models.LongField()
	deal_id = models.StringField(default='', max_length=50)  #交易流水号
	order_id = models.StringField(default='', max_length=50)  #订单的order_id
	products = models.StringField() #商品集合信息
	status = models.IntField() #状态\0创建订单失败 1 创建订单 
	created_at = models.DateTimeField(default=datetime.datetime.now()) #创建时间
	errcode = models.IntField() #向第三方的返回码
	reason = models.StringField() #来自apiserver的返回结果的详细信息

	meta = {
		'collection': 'mall_order_relation',
		'db_alias': 'open'
	}
