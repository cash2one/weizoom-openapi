# -*- coding: utf-8 -*-

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.utils.resource_client import Resource
import time

from business.pay.pay import PayLog

class APay(api_resource.ApiResource):
	"""
	创建订单及修改订单
	"""
	app = 'pay'
	resource = 'third_pay'

	@param_required(['woid', 'order_id'])
	def put(args):
		woid = args['woid']
		order_id = args['order_id']
		if int(woid) == 3:
			access_token = 'N7W7Q2gmONrBnr27O/HJ5zjMa9HADm25lRkijLzYLHsvNHJoZP/53hbqL8V9rZKxpupcgSKzmL/tvGtu5RaDTw%3D%3D'
		timestamp = str(long(time.time() * 1000))
		data = { 'order_id':order_id, 'timestamp':timestamp, 'woid': woid, u'access_token':access_token, 'pay_interface_type':'2'}
		print "data",data
		resp = Resource.use('apiserver').put({
							'resource': 'pay.pay_result',
							'data': data
						})
		print resp

		
		status = 0
		code = 0
		errcode= 0
		reason= ''
		print "*"*100
		print resp
		print "*"*100
		if resp:
			code = resp["code"]
			if code == 200:
				if resp['data']['is_success'] == True:
					status =1
				else:
					msg = resp['data']['msg']
					reason = msg
					if u'非待支付订单' in msg:
						errcode = 71000
			if code == 500:
				reason = resp['errMsg']
				msg = '支付请求参数错误或缺少参数'
				errcode = 71001
		PayLog.save({
			'woid': args['woid'],
			'order_id': order_id,
			'status': status,
			'errcode': errcode,
			'reason': str(reason)
			})
		if code == 200 and status:
			return 200,{'order_id': order_id, 'success':True}
		elif code == 200 and not status:
			return errcode,{'order_id': order_id, 'success':False}
		elif code == 500:
			return errcode,{'order_id': order_id, 'success':False}
		else:
			return 995995,{'order_id': order_id, 'success':False}




