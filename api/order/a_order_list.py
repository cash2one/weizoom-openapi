# -*- coding: utf-8 -*-
"""
@package db.notify.models
通知信息表结构

@author bert
"""

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from util.error_codes import *
import json
import time


class AOrderList(api_resource.ApiResource):
	"""
	获取订单列表
	apiserver 每页20条
	"""
	app = 'mall'
	resource = 'order_list'

	@param_required(['woid', 'cur_page'])
	def get(args):
		count_per_page = args.get('count_per_page', 20)
		woid = args['woid']
		cur_page = int(args['cur_page'])
		if args.has_key('order_status') and str(args['order_status']).isdigit():
			order_type = int(args['order_status'])
		else:
			order_type = -1
		
		access_token = args['apiserver_access_token']
		timestamp = str(long(time.time() * 1000))
		data = {'timestamp':timestamp, 'woid': woid, 'order_type':order_type, 'cur_page':cur_page,
			u'access_token':access_token, 'count_per_page':count_per_page
			}
		resp = Resource.use('default').get({
							'resource': 'mall.order_list',
							'data': data
			})


		errcode= 0
		page_info = {}
		if resp:
			code = resp["code"]
			if code == 200:
				order_detail = {}
				data = resp["data"]
				tmp_orders = []
				for order in data['orders']:
					tmp_data = {
					'order_id':order['order_id'],
					'final_price': order['final_price'],
					'order_status': order['status'],
					
					'product_count': order['product_count'],
					'created_at': order['created_at'],
					'products':[]
					}
					for product in order['products']:
						tmp_product = {
						'product_id': product['id'],
						'product_name': product['name'],
						'product_count': product['purchase_count'],
						'pic_url': product['thumbnails_url'],
						'product_model_name': product['model']['name'],
						'price': product['model']['price'],
						}
						tmp_data['products'].append(tmp_product)
					tmp_orders.append(tmp_data)
				page_info = {
					'max_page': data['page_info']['max_page'],
					'cur_page': data['page_info']['cur_page'],
					'total_count': data['page_info']['object_count'],
				}

				return {'orders':tmp_orders, 'page_info':page_info}

			if code == 500:
				
				errcode = GET_ORDER_LIST_ERROR
				watchdog.info("get order list failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
				return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		else:
			errcode = SYSTEM_ERROR_CODE
			watchdog.error("get order list failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		

