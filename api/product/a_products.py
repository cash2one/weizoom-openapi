# -*- coding: utf-8 -*-
"""@package db.notify.models
通知信息表结构

@author cdg
"""
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.core.exceptionutil import unicode_full_stack
from eaglet.utils.resource_client import Resource

from util.error_codes import * 
import requests

COUNT_PER_PAGE = 200

class AProducts(api_resource.ApiResource):
    """
    商品列表
    API:
        method: get
        url: mall/products/

    Args:
        取值以及说明:
          woid  : weapp_owner_id 
          cur_page : 第几页
          count_per_page : 每页商品数量
    """
    app = "mall"
    resource = "products"

    @param_required(['woid'])
    def get(args):
        #返回三方的响应数据结构
        data = {}
        reaponse_data = {}
        try:
            # param_data = {'access_token':args['apiserver_access_token'], 'woid':args['woid'],'category_id':0, 'cur_page':args['cur_page']}
            # 如果请求的页数大于最大页数，那么gaia只返回最后一页的数据
            gaia_data = {
                'corp_id': args['woid'],
                'cur_page': args.get('page', 1),
                'count_per_page': args.get('count_per_page', COUNT_PER_PAGE)
            }
            gaia_data['count_per_page'] = 200 if int(gaia_data['count_per_page'])>200 else gaia_data['count_per_page']
            resource = 'product.onshelf_products'
            resp = Resource.use('gaia').get({
                'resource': resource,
                'data': gaia_data
            })

            if not resp or resp['code'] != 200:
                data['errmsg'] = code2msg[FAIL_GET_PRODUCT_LIST_CODE]
                data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
                return data
            #获取商品列表
            resp_data = resp['data']
            if resp_data.get('products',''):
                products = resp_data['products']
                page_send_info = resp_data['pageinfo']
            else:
                data['errmsg'] = code2msg[EMPTY_GET_PRODUCT_LIST_CODE]
                data['errcode'] = EMPTY_GET_PRODUCT_LIST_CODE
                return data
            """{
                "code": 200,
                "data": {
                    "items": [
                        {
                            "id": 11,
                            "name": "短袖T恤",
                            "thumbnails_url": "http://chaozhi.weizoom.com/static/upload/20160921/1474450258043_377.jpg"
                        },
                        {
                            "id": 10,
                            "name": "吊裆裤",
                            "thumbnails_url": "http://chaozhi.weizoom.com/static/upload/20160921/1474448967063_375.jpg"
                        }
                    ],
                    "page_info":{
                        u'max_page': 3000,
                        u'object_count': 5999,
                        u'cur_page': 1,
                    }
                },
                "errMsg": "",
                "innerErrMsg": ""
                }
               此为即将返回的商品列表的格式
            """
            products=[{'id':product['id'],'name':product['name'],'thumbnails_url':product['image']} for product in products]
            page_info = {}
            page_info['max_page'] = page_send_info['max_page']
            page_info['object_count'] = page_send_info['object_count']
            page_info['cur_page'] = page_send_info['cur_page']
            data['items'] = products
            data['page_info'] = page_info
            return data
        except:
            watchdog.error("get product_list faled !!!=======>>>{}".format(unicode_full_stack()))
            data['errmsg'] = code2msg[FAIL_GET_PRODUCT_LIST_CODE]
            data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
            return data