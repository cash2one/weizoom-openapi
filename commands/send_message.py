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
        topic_name = args[0] if len(args) > 0 else 'product'
        logging.info("topic name: {}".format(topic_name))

        # 示例数据
        # data = {"order_id": "20170122165456346^8s", "express_number": "22222", "express_company_name": "ems"}
        # msg_name = "delivery_item_shipped"

        data = {
                'product_id':1111,
                'woids': '[6]'
            }
        msg_name = "product_updated"

        # func_name = "customer.update_or_add"

        logging.info(">>>>>current time: {}".format(datetime.datetime.now()))
        msgutil.send_message(topic_name, msg_name, data)

        return
