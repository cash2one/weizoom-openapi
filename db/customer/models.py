#coding: utf8
from eaglet.core.db import models

from db.account.models import User

import datetime

#应用状态
STATUS_UNACTIVATED = 0 #待激活
STATUS_CHECKING = 1 #审核中
STATUS_ACTIVATED = 2 #已激活
STATUS_REJECT = 3 #已驳回
STATUS_STOPED = 4 #已停用
class CustomerMessage(models.Model):
	"""
	客户信息
	"""
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50, null=True)  #开发者姓名
	mobile_number = models.CharField(max_length=20, null=True)  #手机号
	email = models.CharField(max_length=50, null=True) #邮箱
	server_ip = models.CharField(max_length=50, null=True) #服务器IP
	interface_url = models.CharField(max_length=1024, null=True) #接口回调地址
	is_deleted = models.BooleanField(default=False)
	app_id = models.CharField(max_length=50, null=True) #app_id
	app_secret = models.CharField(max_length=50, null=True) #app_secret
	created_at = models.DateTimeField(auto_now_add=True)  #添加时间

	class Meta(object):
		db_table = 'customer_message'


class CustomerServerIps(models.Model):
	"""
	多个服务器IP
	"""
	customer = models.ForeignKey(CustomerMessage)
	name = models.CharField(max_length=1024) # Ip名
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'customer_message_server_ips'