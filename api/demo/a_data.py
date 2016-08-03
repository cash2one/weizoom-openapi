# -*- coding: utf-8 -*-
"""@package wapi.mall.a_data
服务演示数据

"""
#import copy
#from datetime import datetime
#import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.demo.data import Data

class AData(api_resource.ApiResource):
	"""
	优惠券
	"""
	app = 'demo'
	resource = 'data'

	@param_required(['id'])
	def get(args):
		data = Data.get({
			"id": args.get('id', None)
		})

		return {
			"id": data.id,
			"name": data.name,
			"age": data.age
		}
