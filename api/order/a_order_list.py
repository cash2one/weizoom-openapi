# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
import json
import time


class AOrderList(api_resource.ApiResource):
	"""
	获取订单列表
	apiserver 每页8条
	"""
	app = 'mall'
	resource = 'order_list'

	@param_required(['woid', 'cur_page', 'order_status'])
	def get(args):

		woid = args['woid']
		cur_page = int(args['cur_page'])
		if args.has_key('order_status') and str(args['order_status']).isdigit():
			order_type = int(args['order_status'])
		else:
			order_type = -1
		if int(woid) == 3:
			access_token = 'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
			timestamp = str(long(time.time() * 1000))
			data = {'timestamp':timestamp, 'woid': woid, 'order_type':order_type, 'cur_page':cur_page,
				u'access_token':access_token
				}
			resp = Resource.use('apiserver').get({
								'resource': 'mall.express_details',
								'data': data
				})
		status = 0
		code = 0
		errcode= 0

		if resp:
			code = resp["code"]
			page_info = {}
			if code == 200:
				order_detail = {}
				data = resp["data"]
				tmp_orders = []
				for order in data['orders']:
					tmp_data = {
					'order_id':order['order_id'],
					'total_price': order['final_price'],
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

				return 200,{'orders':tmp_orders, 'success':True, 'page_info':page_info}

			if code == 500:
				
				errcode = 74001
				watchdog.info("get order list failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
				return errcode,{'orders': [], 'success':False, 'page_info': page_info}
		else:
			errcode = 995995
			watchdog.error("get order list failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
			return errcode,{'orders': [], 'success':False, 'page_info': page_info}
		

