#coding: utf8
import mongoengine as models

import datetime

class PayLog(models.Document):
	"""
	商品关系,记录创建商品的deal_id和云商通创建的order的order_id
	"""
	woid = models.LongField()
	order_id = models.StringField(default='', max_length=50)  #订单的order_id
	status = models.IntField() #支付状态，成功或者失败 0支付失败 1支付成功
	errcode = models.IntField() #向第三方的返回码
	reason = models.StringField() #来自apiserver的返回结果的详细信息
	appid = models.StringField() #应用appid
	created_at = models.DateTimeField(default=datetime.datetime.now()) #创建时间
	
	meta = {
		'collection': 'mall_pay_log',
		'db_alias': 'open'
	}
