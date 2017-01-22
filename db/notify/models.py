# -*- coding: utf-8 -*-
"""@package db.notify.models
通知信息表结构

@author bert
"""

import eaglet.core.db as models

import datetime

TYPE_DELIVERED = "delivered"

class NotifyMessage(models.Model):
	"""
	notify 通知记录
	"""
	msg_id = models.CharField(max_length=100)
	type = models.CharField() #消息类型（发货 取消）
	message = models.CharField(max_length=1000)  #记录消息信息
	reason = models.CharField() #记录请求信息
	status = models.IntField() #发送状态，成功或者失败 0支付失败 1支付成功
	retry_time = models.IntField() #重试次数
	created_at = models.DateTimeField(default=datetime.datetime.now()) #创建时间
	
	meta = {
		'collection': 'notify_message',
		'db_alias': 'open'
	}
