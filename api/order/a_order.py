# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
import json
import time

from business.order.order_relation import OrderRelation


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
		if int(woid) == 3:
			access_token = 'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
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
		errcode= 0

		if resp:
			code = resp["code"]
			if code == 200:
				order_detail = {}
				order = resp["data"]['order']
				
				order_detail['order_id'] = order['order_id']
				order_detail['order_status'] = order['status']
				order_detail['total_price'] = order['final_price']
				order_detail['ship_address'] = order['ship_address']
				order_detail['ship_name'] = order['ship_name']
				order_detail['ship_tel'] = order['ship_tel']
				
				order_detail['created_at'] = order['created_at']
				order_detail['sub_orders'] = []
				for sub_order in order['sub_orders']:
					sub_order_detail = {}
					sub_order_detail['order_id'] = sub_order['order_id']
					sub_order_detail['order_status'] = sub_order['status']

					sub_order_detail['express_company_name'] = sub_order['express_company_name']
					sub_order_detail['express_number'] = sub_order['express_number']
					sub_order_detail['delivery_time'] = sub_order['delivery_time']
					sub_order_detail['postage'] = sub_order['postage']

					sub_order_detail['postage'] = sub_order['postage']
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

				return {'order':order_detail, 'success':True, 'errcode':errcode}


			if code == 500:
				msg = '获取订单详情请求参数错误或缺少参数'
				errcode = 72000
				return {'order_id': order_id, 'success':False, 'errcode':errcode}
		else:
			msg = '获取订单详情请求存在问题，请联系管理员'
			errcode = 72001
			return {'order_id': order_id, 'success':False, 'errcode':errcode}
		

	@param_required(['ship_name', 'ship_tel', 'ship_address', 'products', 'woid'])
	def put(args):
		woid = args['woid']
		ship_name = args['ship_name']
		ship_address = args['ship_address']
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

		if int(woid) == 3:
			access_token = 'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
		timestamp = str(long(time.time() * 1000))
		data = {u'xa-choseInterfaces': u'2',
			u'product_counts': product_counts, u'ship_address': ship_address, 'woid': woid, 
			u'timestamp': timestamp, u'integral': u'undefined', u'coupon_id': u'0', u'product_model_names': product_model_names,  
			u'ship_tel': ship_tel, u'message': '{}', u'order_type': u'undefined', u'area': u' ', 
			u'is_order_from_shopping_cart': u'false', u'ship_name': ship_name, 
			 u'product_ids': product_ids, u'access_token':access_token}

		resp = Resource.use('apiserver').put({
							'resource': 'mall.order',
							'data': data
						})
		order_id = ''
		status = 0
		code = 0
		errcode= 0
		reason= ''

		if resp:
			code = resp["code"]
			if code == 200:
				order_id = resp["data"]['order_id']
				status =1
			if code == 500:
				reason = resp['errMsg']
				if reason['detail']:
					msg = reason['detail'][0]['msg']
					if u'库存不足' in msg:
						errcode = 71000
				else:
					msg = '创建订单请求参数错误或缺少参数'
					errcode = 71001

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
			return {'order_id': order_id, 'success':True, 'errcode':errcode}
		elif code == 500:
			return {'order_id': order_id, 'success':False, 'errcode':errcode}
		else:
			errcode = 995995
			watchdog.error("create order failed!! msg:{}".format(unicode_full_stack()),log_type='OPENAPI_ORDER')
			return {'order_id': order_id, 'success':False, 'errcode':errcode}
			
	@param_required(['woid', 'order_id'])
	def post(args):

		woid = args['woid']

		order_id = args['order_id']
		if int(woid) == 3:
			access_token = 'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'

		timestamp = str(long(time.time() * 1000))
		data = {'order_id':order_id, 'timestamp':timestamp, 'woid': u'3',
			u'access_token':access_token, 'action':'cancel'
			}
		resp = Resource.use('apiserver').put({
					'resource': 'mall.refund',
					'data': data
				})
		status = 0
		code = 0
		errcode= 0

		if resp:
			code = resp["code"]
			if code == 200:
				return {'success':True, 'errcode':errcode}

			if code == 500:
				
				msg = resp['data']['msg']
				errcode = 73000
				if msg == u'有子订单的状态不是待发货,不能取消订单':
					errcode = 73001
				watchdog.info("cancel order failed!! errcode:{}, msg:{}".format(errcode, msg),log_type='OPENAPI_ORDER')
				return {'success':False, 'errcode':errcode}
		else:
			
			errcode = 995995
			watchdog.error("cancel order failed!! errcode:{}, msg:{}".format(errcode, unicode_full_stack()),log_type='OPENAPI_ORDER')
			return {'success':False, 'errcode':errcode}
