# -*- coding: utf-8 -*-
"""
测试发消息

@author Victor
"""

from eaglet.utils.command import BaseCommand
import logging
import datetime

from bdem import msgutil


class Command(BaseCommand):
    help = "python manage.py send_message"
    args = ''

    def handle(self, *args, **options):
        topic_name = args[0] if len(args) > 0 else 'test-topic'
        logging.info("topic name: {}".format(topic_name))

        # 示例数据
        data = {"order_id": "20170122165456346^8s", "express_number": "22222", "express_company_name": "ems"}
        msg_name = "send_order_delivered_notify_service"

        # func_name = "customer.update_or_add"

        for i in range(10):
            logging.info(">>>>>current time: {}".format(datetime.datetime.now()))
            data['data'] = i
            msgutil.send_message(topic_name, msg_name, data)

        return
