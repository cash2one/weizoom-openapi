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
import json
import time

from business.order.order_relation import OrderRelation
from util.error_codes import *

class AOrder(api_resource.ApiResource):
	"""
	创建订单及修改订单
	"""
	app = 'mall'
	resource = 'order'

	@param_required(['woid', 'order_id'])
	def get(args):
		woid = args['woid']
		order_id = args['order_id'].split('^')[0]
		
		access_token = args['apiserver_access_token']
		timestamp = str(long(time.time() * 1000))
		data = {'order_id':order_id, 'timestamp':timestamp, 'woid': woid, 
			u'access_token':access_token
			}
		resp = Resource.use('apiserver').get({
					'resource': 'mall.order',
					'data': data
				})
		status = 0
		code = 0
		errcode= SUCCESS_CODE

		if resp:
			code = resp["code"]
			if code == 200:
				order_detail = {}
				order = resp["data"]['order']
				
				order_detail['order_id'] = order['order_id']
				order_detail['order_status'] = order['status']
				order_detail['final_price'] = order['final_price']
				order_detail['ship_address'] = order['ship_address']
				order_detail['ship_area'] = order['ship_area']
				order_detail['ship_name'] = order['ship_name']
				order_detail['ship_tel'] = order['ship_tel']
				order_detail['postage'] = order['postage']

				order_detail['created_at'] = order['created_at']
				order_detail['products'] = []
				for product in order['products']:
					order_detail['products'].append({
						'product_id': product['id'],
						'product_name': product['name'],
						'price': product['price'],
						'product_count': product['purchase_count'],
						'product_model_name': product['model']['name'],
						})
				order_detail['sub_orders'] = []
				if order['sub_orders']:
					for sub_order in order['sub_orders']:
						sub_order_detail = {}
						sub_order_detail['order_id'] = sub_order['order_id']
						sub_order_detail['order_status'] = sub_order['status']

						sub_order_detail['express_company_name'] = sub_order['express_company_name']
						sub_order_detail['express_number'] = sub_order['express_number']
						sub_order_detail['delivery_time'] = sub_order['delivery_time']
						sub_order_detail['postage'] = sub_order['postage']

						# sub_order_detail['postage'] = sub_order['postage']
						sub_order_detail['products'] = []
						for sub_order_product in sub_order['products']:
							tmp_sub_order_product = {}
							tmp_sub_order_product['product_id'] = sub_order_product['model']['product_id']
							tmp_sub_order_product['product_name'] = sub_order_product['name']
							tmp_sub_order_product['price'] = sub_order_product['price']
							tmp_sub_order_product['product_count'] = sub_order_product['purchase_count']
							tmp_sub_order_product['product_model_name'] = sub_order_product['model_name']
							tmp_sub_order_product['pic_url'] = sub_order_product['thumbnails_url']

							sub_order_detail['products'].append(tmp_sub_order_product)
						order_detail['sub_orders'].append(sub_order_detail)

				return {'order':order_detail}

			if code == 500:
				# msg = '获取订单详情请求参数错误或缺少参数'
				errcode = GET_ORDER_PARAMETER_ERROR
				return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		else:
			# msg = '获取订单详情请求存在问题，请联系管理员'
			errcode = GET_ORDER_REQUEST_ERROR
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		

	@param_required(['ship_name', 'ship_tel', 'ship_address', 'products', 'woid', 'area'])
	def put(args):
		'''
		下单接口
		'''
		woid = args['woid']
		ship_name = args['ship_name']
		ship_address = args['ship_address']
		area = args['area']
		ship_tel = args['ship_tel']
		products = args['products']
		products_json = json.loads(products)
		product_ids = []
		product_counts = []
		product_model_names = []
		for product in products_json:
			product_ids.append(str(product['product_id']))
			product_counts.append(str(product['product_count']))
			product_model_names.append((product['product_model_name']))
			
		product_ids = "_".join(product_ids)
		product_counts = "_".join(product_counts)
		product_model_names = "$".join(product_model_names)

		
		access_token = args['apiserver_access_token']
		timestamp = str(long(time.time() * 1000))
		data = {u'xa-choseInterfaces': u'2',
			u'product_counts': product_counts, u'ship_address': ship_address, 'woid': woid, 'lock':False,
			u'timestamp': timestamp, u'integral': u'undefined', u'coupon_id': u'0', u'product_model_names': product_model_names,  
			u'ship_tel': ship_tel, u'message': '{}', u'order_type': u'undefined', u'area': area, 
			u'is_order_from_shopping_cart': u'false', u'ship_name': ship_name, 
			 u'product_ids': product_ids, u'access_token':access_token}

		resp = Resource.use('apiserver').put({
							'resource': 'mall.order',
							'data': data
						})
		order_id = ''
		status = 0
		code = 0
		errcode= SYSTEM_ERROR_CODE
		reason= ''

		if resp:
			code = resp["code"]
			if code == 200:
				order_id = resp["data"]['order_id']
				errcode= SUCCESS_CODE
				status =1
			if code == 500:
				reason = resp['data']
				if reason['detail']:
					msg = reason['detail'][0]['msg']
					short_msg = reason['detail'][0]['short_msg']
					if u'库存不足' in msg:
						errcode = PUT_ORDER_LOW_STOCKS
					if u'超出范围' in short_msg:
						errcode = PUT_ORDER_OUT_LIMIT_ZONE
				else:
					errcode = PUT_ORDER_PARAMETER_ERROR

		OrderRelation.save({
			'woid': args['woid'],
			'deal_id': args['deal_id'],
			'order_id': order_id,
			'products': products,
			'status': status,
			'errcode': errcode,
			'reason': str(reason)
			})

		if code == 200:
			return {'order_id': order_id}
		elif code == 500:
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		else:
			watchdog.error("create order failed!! msg:{}".format(unicode_full_stack()),log_type='OPENAPI_ORDER')
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
			
	@param_required(['woid', 'order_id'])
	def post(args):

		woid = args['woid']

		order_id = args['order_id']
		
		access_token = args['apiserver_access_token']

		timestamp = str(long(time.time() * 1000))
		data = {'order_id':order_id, 'timestamp':timestamp, 'woid': woid,
			u'access_token':access_token, 'action':'cancel'
			}
		resp = Resource.use('apiserver').put({
					'resource': 'mall.refund',
					'data': data
				})
		status = 0
		code = 0
		errcode= SUCCESS_CODE

		if resp:
			code = resp["code"]
			if code == 200:
				return {'errcode':errcode}

			if code == 500:
				msg = resp['data']['msg']
				errcode = SUB_ORDER_STATUS_ERROR
				if msg == u'有子订单的状态不是待发货,不能取消订单':
					errcode = CANCEL_ORDER_ERROR
				watchdog.info("cancel order failed!! errcode:{}, msg:{}".format(errcode, msg),log_type='OPENAPI_ORDER')
				return {'errcode':errcode, 'errmsg':code2msg[errcode]}
		else:
			errcode = SYSTEM_ERROR_CODE
			watchdog.error("cancel order failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
			return {'errcode':errcode, 'errmsg':code2msg[errcode]}
