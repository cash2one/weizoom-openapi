# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import requests
# from eaglet.utils.resource_client import Resource
import json
import time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}

# products = [
#     # {"product_id":9,"product_model_id":15,"product_name":"热干面", "product_count":12, "product_price":8}, 
#     # {"product_id":8,"product_model_id":14,"product_name":"黄桥烧饼", "product_count":12, "product_price":8},
#     {"product_id":10,"product_model_id":16,"product_name":"iphone5", "product_count":1, "product_price":1000},
#     {"product_id":10,"product_model_id":17,"product_name":"iphone5", "product_count":1, "product_price":1000},
#     {"product_id":10,"product_model_id":18,"product_name":"iphone5", "product_count":1, "product_price":1000},
#     {"product_id":11,"product_model_id":20,"product_name":"iphonett", "product_count":1, "product_price":500},
#     ]
# products = [
#     {"product_id":12,"product_model_name":'standard',"product_count":2,},
#     {"product_id":11,"product_model_name":"standard","product_count":1, },
#     ]
# products = json.dumps(products)
# data = {
#     'woid':3,
#     'ship_name':u'张三',
#     'ship_tel':'13766665555',
#     'ship_address':u'张三李四的地址',
#     'deal_price':17600,
#     'products':products
# }
# resp = Resource.use('apiserver').put({
#                     'resource': 'mall.order',
#                     'data': data
#                 })

# print resp


#创建订单
"""
 {u'xa-choseInterfaces': u'2', u'promotion_ids': u'0_0', u'product_counts': u'1_1', u'ship_address': u'\u6cf0\u5174\u5927\u53a6', 'woid': u'3',
  u'timestamp': u'1474452424189', 'zdepth': '2', u'integral': u'undefined', u'coupon_id': u'0', u'product_model_names': 'standard$standard', 
  'f_zindex': 'undefined_1', u'ship_tel': u'13811223344', u'message': '{}', 'webapp_owner': <business.account.webapp_owner.WebAppOwner object at 0x000000000608E9D8>, 
  '__nocache': '1', '_method': u'put', u'group2integralinfo': '{}', u'order_type': u'undefined', u'area': u'1_1_8', 
  'access_token': 'qSFSuwz0TiIADmwjoy31mTWGfgsRPBTry3l21mwOH8WjEADfI9QCtZXy2Pwejqh1HSYzirY7iS1HIwz1tdMaA7QHPg==', 
  u'is_order_from_shopping_cart': u'true', u'ship_name': u'bill', 'wapi_id': '/mall/order_POST', 
  'webapp_user': <business.account.webapp_user.WebAppUser object at 0x00000000060CA548>, 'zid': 'ae6357c8-cf52-4ae6-999c-f5683a06478a', u'product_ids': u'8_11', 
  u'_ids': u'null'}
"""
"""
创建订单参数说明
xa-choseInterfaces:解析支付方式
promotion_ids:  ,可以不传
product_counts:
ship_address:
woid:
timestamp:
zdepth:?????  eaglet
integral:
coupon_id:
product_model_names:
f_zindex:?????? eaglet
ship_tel:
message:
webapp_owner:
# __nocache:    apiserver填充的
group2integralinfo：解析整单积分信息,可以不传
order_type：
area：
access_token：
is_order_from_shopping_cart：
ship_name：
# wapi_id：    apiserver填充的
webapp_user:
zid:?????
product_ids:
_ids:????

"""
# timestamp = str(long(time.time() * 1000))
# data = {u'xa-choseInterfaces': u'2',
#   u'product_counts': u'1_2', u'ship_address': u'\u6cf0\u5174\u5927\u53a6', 'woid': u'3', 
#     u'timestamp': timestamp, u'integral': u'undefined', u'coupon_id': u'0', u'product_model_names': u'standard$standard',  
#     u'ship_tel': u'13811223344', u'message': '{}', u'order_type': u'undefined', u'area': u'1_1_8', 
#     u'is_order_from_shopping_cart': u'false', u'ship_name': u'bill', 
#     u'product_ids': u'12_11',
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'}

# resp = Resource.use('apiserver').put({
#                     'resource': 'mall.order',
#                     'data': data
#                 })
# # 用requests也可以
# # resp = requests.post("http://api.weapp.com/mall/order?_method=put", data=data)
# print resp

"""
支付  
"""
# timestamp = str(long(time.time() * 1000))
# data = {u'pay_interface_type': u'2', 'order_id':u'20160921205050481', 'timestamp':timestamp, 'woid': u'3', 
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
#     }
# resp = Resource.use('apiserver').put({
#                     'resource': 'pay.pay_result',
#                     'data': data
#                 })
# print resp


"""
取消订单  
"""
# timestamp = str(long(time.time() * 1000))
# data = {u'pay_interface_type': u'2', 'order_id':u'20160922162029557', 'timestamp':timestamp, 'woid': u'3', 'action':'cancel',
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
#     }
# resp = Resource.use('apiserver').post({
#                     'resource': 'mall.order',
#                     'data': data
#                 })
# print resp

"""
订单详情  
"""
# timestamp = str(long(time.time() * 1000))
# data = {'order_id':u'20160921205050481', 'timestamp':timestamp, 'woid': u'3', 
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
#     }
# resp = Resource.use('apiserver').get({
#                     'resource': 'mall.order',
#                     'data': data
#                 })
# print resp


"""
订单列表
"""
# timestamp = str(long(time.time() * 1000))
# data = {'timestamp':timestamp, 'woid': u'3', 'order_type':-1, 'cur_page':1,
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
#     }
# resp = Resource.use('apiserver').get({
#                     'resource': 'mall.order_list',
#                     'data': data
#                 })
# order = resp['data']['orders'][0]
# print "resp",order
# print order.keys()
# print order['products'][0]
# print resp
 


"""
订单物流详情
"""
# timestamp = str(long(time.time() * 1000))
# data = {'timestamp':timestamp, 'woid': u'3', 'order_id':'20160922174514355^1s', 
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
#     }
# resp = Resource.use('apiserver').get({
#                     'resource': 'mall.express_details',
#                     'data': data
#                 })
# # order = resp['data']['orders'][0]
# # print "resp",order
# # print order.keys()
# # print order['products'][0]
# print resp




"""
测试openapi put order
"""
# products = [
#     {"product_id":13,"product_model_name":'3:7',"product_count":2,},
#     {"product_id":13,"product_model_name":'3:8',"product_count":2,},
#     {"product_id":10,"product_model_name":"standard","product_count":1, },
#     ]
# products = json.dumps(products)
# data = {
#     'woid':3,
#     'ship_name':u'张三',
#     'ship_tel':'13766665555',
#     'ship_address':u'张三李四的地址',
#     'deal_id':'17600',
#     'products':products
# }
# resp = requests.post("http://dev.openapi.com/mall/order?_method=put", data=data)
# print resp
# # print dir(resp)
# print resp.text
"""
测试openapi put order
"""


"""
测试openapi put pay
# """
# woid = 3
# order_id = u'20160922162029557'
# order_ids = ['20160926184550388', '20160926184550078', '20160926184548509' ]
# for order_id in order_ids:
# 	data = {
# 	    'woid':woid,
# 	    'order_id':order_id,
# 	}
# 	resp = requests.post("http://dev.openapi.com/pay/third_pay?_method=put", data=data)
# print resp

# print resp.text
"""
测试openapi put pay
"""

"""
测试openapi get order 
"""
# woid = 3
# order_id = u'20160922114955019'
# data = {'order_id':order_id, 'woid': u'3', }
# resp = requests.get("http://dev.openapi.com/mall/order", data=data)
# print resp.text


"""
测试openapi get order
"""




"""
测试openapi get order
"""
# timestamp = str(long(time.time() * 1000))
# data = {'timestamp':timestamp, 'woid': u'3', 'order_status':-1, 'cur_page':3,
#     u'access_token':'ahQamDeQgZfrWpdR00CsZ6U%2BoRqZ0tVJK0rr27XW1DKudojNeZ2Kz8RpENSpxPDLtg7OhA5WFTLF8E2%2Btg%2BSvg%3D%3D'
#     }
# resp = requests.get("http://dev.openapi.com/mall/order_list", data=data)
# # order = resp['data']['orders'][0]
# print "resp",resp.text

"""
测试openapi order list
"""



"""
测试订单物流
"""
# timestamp = str(long(time.time() * 1000))
# data = {'timestamp':timestamp, 'woid': u'3', 'order_id':'20160922174514355^1s', 
#     }
# resp = requests.get("http://dev.openapi.com/mall/express_details", data=data)

# print '>>>',resp.text


"""
测试订单物流
"""



"""
测试openapi post order(取消订单、退款)
"""

order_id ='20160926162019205^1s'
order_ids = ['20160926165121411', '20160926165123216^2s', '20160926165124218^2s', '20160926165125780^2s', '20160926165126960^2s', '20160926165127176^2s']
order_ids = ['20160926194619314']
for order_id in order_ids:
	data = {
	    'woid':3,
	    'order_id': order_id
	}
	resp = requests.post("http://dev.openapi.com/mall/order", data=data)
	print resp
	# print dir(resp)
	print resp.text
"""
测试openapi post order
"""