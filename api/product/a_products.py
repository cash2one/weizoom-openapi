# -*- coding: utf-8 -*-
"""@package wapi.mall.a_data
服务演示数据

"""
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource

from api.error_codes import * 

class AProducts(api_resource.ApiResource):
    """
    商品列表
    API:
        method: get
        url: mall/products/

    Args:
        取值以及说明:
          woid  : weapp_owner_id 
          cur_page : 第几页  --暂时不实现
          count_per_page : 每页商品数量 --暂时不实现
    """
    app = "mall"
    resource = "products"

    @param_required(['woid'])
    def get(args):
        #返回三方的响应数据结构
        data = {}
        reaponse_data = {}
        reaponse_data['errMsg'] = ''
        reaponse_data['innerErrMsg'] = ''
        try:
            param_data = {'access_token':args['apiserver_access_token'], 'woid':args['woid'],'category_id':0}
            resp = Resource.use('apiserver').get({
                    'resource':'mall.products',
                    'data':param_data
                })
            if not resp or resp['code'] != 200:
                data['items'] = []
                reaponse_data['errMsg'] = code2msg['FAIL_GET_PRODUCT_LIST_CODE']
                reaponse_data['innerErrMsg'] = code2msg['FAIL_GET_PRODUCT_LIST_CODE']
                data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
                reaponse_data['data'] = data
                return reaponse_data
            #获取商品列表
            products = resp['data']['products']
            """[
                {
                    "name": "w",
                    "is_member_product": false,
                    "display_price": 2,
                    "sales": 0,
                    "thumbnails_url": "http://chaozhi.weizoom.com/static/upload/20160921/1474448967063_375.jpg",
                    "promotion_js": "null",
                    "supplier": 2,
                    "id": 10,
                    "categories": []
                },
                   ......
               ]
               此为apiserver返回的商品列表的每一个商品的格式，需要手工把
               is_member_product、promotion_js、categories三个字段手工处理掉，无需返回给客户
            """
            for product in products:
                del product['is_member_product']
                del product['promotion_js']
                del product['categories']
            data['items'] = products
            reaponse_data['data'] = data
            return reaponse_data
        except:
            watchdog.error(unicode_full_stack())
            data['items'] = []
            reaponse_data['errMsg'] = code2msg['FAIL_GET_PRODUCT_LIST_CODE']
            reaponse_data['innerErrMsg'] = code2msg['FAIL_GET_PRODUCT_LIST_CODE']
            data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
            reaponse_data['data'] = data
            return reaponse_data