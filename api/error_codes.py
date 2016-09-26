# -*- coding: utf-8 -*-

import product

__author__ = 'bert'

"""
Api全局错误代码定义以及对应的说明

"""

SYSTEM_BUSY_CODE = -1
SUCCESS_CODE = 0
INVALID_ACCESS_TOKEN_CODE = 40001
ILLEGAL_ACCESS_TOKEN_CODE = 40002
ILLEGAL_OPENID_CODE = 40003
ILLEGAL_WOID_CODE = 40004
LACK_ACCESS_TOKEN_CODE = 40005
LACK_CALLBACK_URI = 40006
ACCESS_TOKEN_EXPIRED_CODE = 40007
#系统自身错误信息
SYSTEM_ERROR_CODE = 995995
#查询商品详情的返回码
FAIL_GET_PRODUCT_DETAIL_CODE = '41001'
FAIL_GET_PRODUCT_LIST_CODE = '41002'


code2msg = {
	'SYSTEM_BUSY_CODE' : u'系统繁忙 ',
	'SUCCESS_CODE' : u'请求成功 ',
	'INVALID_ACCESS_TOKEN_CODE' : u'获取access_token无效',
	'ILLEGAL_ACCESS_TOKEN_CODE' : u'不合法的access_token',
	'ILLEGAL_OPENID_CODE' : u'不合法的openid',
	'ILLEGAL_WOID_CODE' : u'不合法的woid',
	'LACK_ACCESS_TOKEN_CODE' : u'缺少access_token参数',
	'LACK_CALLBACK_URI' : u'缺少callback_uri参数',
	'ACCESS_TOKEN_EXPIRED_CODE' : u'access_token过期',

	'SYSTEM_ERROR_CODE' : u'系统自身异常',

	#查询商品详情的返回信息
	'FAIL_GET_PRODUCT_DETAIL_CODE' : u'查询商品详情失败，请联系管理员',
	'FAIL_GET_PRODUCT_LIST_CODE': u'查询商品列表失败，请联系管理员'

}