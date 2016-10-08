# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
import json
import time

class ASupplierOrderList(api_resource.ApiResource):
	"""
	获取供货商订单列表
	"""
	app = 'mall'
	resource = 'supplier_order'

	@param_required(['supplier_ids'])
	def get(args):
		supplier_ids = args['supplier_ids']
		supplier_ids = 12
		print "*"*100
		print "supplier_ids",supplier_ids
		found_begin_time = args.get('found_begin_time','')
		found_end_time = args.get('found_end_time','')
		order_status = args.get('order_status','')
		order_id = args.get('order_id','')
		cur_page = args.get('cur_page',1)
		count_per_page = args.get('count_per_page',10) #暂定每页10条
		data = {
				'supplier_ids': supplier_ids,
				'page': cur_page,
				'count_per_page': count_per_page,
				'order_id': order_id,
				'start_time': found_begin_time,
				'end_time': found_end_time,
				'status': order_status,
				}
		resp = Resource.use('zeus').post({
			'resource':'panda.order_list_by_supplier',
			'data': data
			})
		if resp:
			if resp['code'] == 200:

				page_info = {
					'max_page': resp['data']['pageinfo']['max_page'],
					'cur_page': resp['data']['pageinfo']['cur_page'],
					'total_count': resp['data']['pageinfo']['object_count'],
				}
				orders = []
				for order in resp['data']['orders']:
					tmp_order = {
						'order_id': order['order_id'],
						'order_status': order['status'],
						# 'final_price': order['final_price'],
						'created_at': order['created_at'],
						'buyer_name': order['buyer_name'],
						'ship_name': order['ship_name'],
						'ship_address': order['ship_address'],
						'ship_tel': order['ship_tel'],
						'express_company_name': order['express_company_name'],
						'express_number': order['express_number'],
						'postage': order['postage'],
						'customer_message': order['customer_message'],
						'invoice_title': order['bill'],
						'payment_time': order['payment_time'],
						'pay_mode': order['pay_interface_type'],
						'final_price': '%.2f' %(order['total_purchase_price'] + order['postage']),
						'products': []
					}
					for product in order['products']:
						tmp_order['products'].append({
							'price': product['price'],
							'count': product['count'],
							'total_price': product['total_price'],
							'name': product['name'],
							'model_names': product['model_names']
							})
					orders.append(tmp_order)
				return {'orders':orders, 'page_info':page_info}

			if code == 500:
				# msg = u'获取供货商订单列表请求参数错误或缺少参数'
				errcode = 76001
				return {'errcode':errcode}
		else:
			# msg = u'获取供货商订单列表请求存在问题，请联系管理员'
			errcode = 76002
			return {'errcode':errcode}
