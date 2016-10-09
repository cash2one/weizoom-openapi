# -*- coding: utf-8 -*-
"""
基于MNS的创建service runner

启动之后，不断轮询队列

@author bert
"""

from eaglet.utils.command import BaseCommand

import json

import settings

from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.core import watchdog
import logging

from mns.account import Account
from mns.queue import *
from mns.topic import *
from mns.subscription import *

import time
import service  # load all services
import service_register




WAIT_SECONDS = 10
SLEEP_SECONDS = 10

class Command(BaseCommand):
	help = "python manage.py customer_create_service"
	args = ''

	# topic-queue模型中的queue

	def handle(self, *args, **options):
		global _SERVICE_LIST

		# 准备访问MNS
		self.mns_account = Account(\
			settings.MNS_ENDPOINT, \
			settings.MNS_ACCESS_KEY_ID, \
			settings.MNS_ACCESS_KEY_SECRET, \
			settings.MNS_SECURITY_TOKEN)
		queue = self.mns_account.get_queue(settings.SUBSCRIBE_QUEUE_NAME)
		watchdog.info(queue.get_attributes().queue_name)
		watchdog.info('queue: {}'.format(queue.get_attributes().queue_name),server_name=settings.SERVICE_NAME)
		# TODO: 改成LongPoll更好
		while True:
			#读取消息
			try:
				recv_msg = queue.receive_message(WAIT_SECONDS)
				watchdog.info("Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id),server_name=settings.SERVICE_NAME)

				# 处理消息(consume)
				data = json.loads(recv_msg.message_body)

				if data.get("function",None):
					data['name'] = data["function"]
					data['data'] = data["args"]

				function_name = data['name']
				func = service_register.SERVICE_LIST.get(function_name)
				if func:
					try:
						response = func(data['data'], recv_msg)
						watchdog.info("service response: {}".format(response),server_name=settings.SERVICE_NAME)
					except:
						watchdog.error(u"Service Exception: {}".format(unicode_full_stack()), server_name=settings.SERVICE_NAME)
				else:
					watchdog.info(u"Error: no such service found : {}".format(function_name), server_name=settings.SERVICE_NAME)

			except MNSExceptionBase as e:
				if e.type == "QueueNotExist":
					watchdog.debug("Queue not exist, please create queue before receive message.",server_name=settings.SERVICE_NAME)
					break
				elif e.type == "MessageNotExist":
					watchdog.debug("Queue is empty! Waiting...", server_name=settings.SERVICE_NAME)
				else:
					pass
					watchdog.debug("Receive Message Fail! Exception:%s\n" % e,server_name=settings.SERVICE_NAME)
				time.sleep(SLEEP_SECONDS)
				continue
			except Exception as e:
				watchdog.error(u"Exception: {}".format(unicode_full_stack()), server_name=settings.SERVICE_NAME)

			#删除消息
			try:
				queue.delete_message(recv_msg.receipt_handle)
				watchdog.info("Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle)
			except MNSException,e:
				watchdog.info("Delete Message Fail! Exception:%s\n" % e)
		return
