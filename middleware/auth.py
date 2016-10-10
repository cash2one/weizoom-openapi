# -*- coding: utf-8 -*-
import logging
import hashlib
import json

from eaglet.core.cache import utils as cache_util
from eaglet.core import redirects
from eaglet.core import watchdog
#from eaglet.core.cache import utils as cache_utils
__author__ = 'bert'

class Auth(object):
	def process_request(self, req, res):
		#TODO 将这部分放到 lua ＋ nginx中（或者kong中）
		if '/auth/access_token' in req.path or 'console' in req.path:
			return 
		access_token = req.params.get('access_token', None)
		if not access_token:
			raise redirects.HTTPMiddlewareError( {
				"errcode": 40003,
				"errmsg": "invalid access_token"
			})

		app = cache_util.get_cache_wrapper(hashlib.md5(access_token).hexdigest())
		if not app:
			raise redirects.HTTPMiddlewareError( {
				"errcode": 40003,
				"errmsg": "invalid access_token"
			})
		
		req.context['appid'] = json.loads(app)['appid']
		req.context['woid'] = json.loads(app)['woid']
		req.context['apiserver_access_token'] = json.loads(app)['apiserver_access_token']
		req.context['supplier_ids'] = json.loads(app)['supplier_ids']
		watchdog.info("auth:woid:%s" % req.context['woid'])
		watchdog.info("auth:apiserver_access_token:%s" % req.context['apiserver_access_token'])
