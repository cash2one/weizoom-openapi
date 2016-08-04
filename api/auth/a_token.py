# -*- coding: utf-8 -*-
"""@package wapi.mall.a_data
服务演示数据

"""
#import copy
#from datetime import datetime
#import json

from eaglet.core import api_resource
from eaglet.decorator import param_required

from business.auth.access_token import AccessToken
from business.auth.app import App

class AToken(api_resource.ApiResource):
	"""
	access_token
	"""
	app = 'auth'
	resource = 'token'

	@param_required(['appid', 'secret'])
	def get(args):
		appid = args.get('appid', None)
		secret = args.get('secret', None)

		if not appid:
			return {
				"errcode": 40001,
				"errmsg": "invalid appid"
			}

		if not secret:
			return {
				"errcode": 40002,
				"errmsg": "invalid secret"
			}

		app = App.get({
			"appid": appid,
			"secret": secret
			})

		if not app:
			return {
				"errcode": -1,
				"errmsg": "no app"
			}

		access_token = AccessToken.put({
			"app": app
		})

		return {
			"access_token": access_token.access_token,
			"expires_in": access_token.expires_in
		}
