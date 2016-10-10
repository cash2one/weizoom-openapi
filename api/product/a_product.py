# -*- coding: utf-8 -*-
"""@package db.notify.models
通知信息表结构

@author cdg
"""
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.utils.resource_client import Resource

from api.error_codes import *

class AProduct(api_resource.ApiResource):
    """
    商品详情
    API:
        method: get
        url: mall/product/

    Args:
        取值以及说明:
          woid  : weapp_owner_id 
          product_id: 商品ID
    """
    app = "mall"
    resource = "product"

    @param_required(['woid', 'product_id'])
    def get(args):
        #返回三方的响应数据结构
        data = {}
        try:
            param_data = {'access_token':args['apiserver_access_token'], 'woid':args['woid'], 'product_id':args['product_id'], 'category_id':0}
            resp = Resource.use('apiserver').get({
                    'resource':'mall.product',
                    'data':param_data
                })
            if not resp or resp['code'] != 200:
                data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
                data['errmsg'] = code2msg['FAIL_GET_PRODUCT_DETAIL_CODE']
                return data
            #获取商品列表
            product = resp['data']
            """
               1、每一个商品的格式，需要手工把无需传送的字段手工处理掉
               2、商品规格分为单规格和多规格的商品，需要分别判断处理
            """
            if product['models']:
                product_model_name = product['models'][0].get('name','')
            key_list = [
                "product_promotion_title","supplier_user_id","integral_sale","is_in_group_buy","bar_code",
                "hint","product_reviews","product_review","display_index", "shelve_type","type","purchase_price",
                "activity_url","use_supplier_postage","detail_link","used_system_model_properties","weshop_sync",
                "promotion_title","properties","categories", "buy_in_supplier","is_member_product", "supplier_name",
                "shelve_end_time","shelve_start_time","promotion","webapp_owner_integral_setting",
                ]
            #多规格里面,要把price_info中的"display_market_price"去掉,还有"user_code", "market_price",purchase_price
            for key in key_list:
                del product[key]
            if product_model_name and product_model_name != 'standard':
                #多规格商品需要删除的key
                del product["unified_postage_money"], product["owner_id"] 

            # product['sku'] = product['models']
            # del product['models']
            return product
        except:
            data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
            data['errmsg'] = code2msg['FAIL_GET_PRODUCT_DETAIL_CODE']
            return data