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
from eaglet.core.exceptionutil import unicode_full_stack

from util.error_codes import *

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
                data['errmsg'] = code2msg[FAIL_GET_PRODUCT_DETAIL_CODE]
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
                "activity_url","detail_link","used_system_model_properties","weshop_sync",
                "promotion_title","properties","categories", "buy_in_supplier","is_member_product", "supplier_name",
                "shelve_end_time","shelve_start_time","promotion","is_deleted","webapp_owner_integral_setting",
                ]
            #多规格里面,要把price_info中的"display_market_price"去掉,还有"user_code", "market_price",purchase_price
            for key in key_list:
                del product[key]
            if product_model_name and product_model_name != 'standard':
                #多规格商品需要删除的key
                del product["owner_id"] 

            if product['classification_id'] and product['classification_id'] != 0:
                classification_info = {}
                data = {}
                param_data = {'access_token':args['apiserver_access_token']}
                resp = Resource.use('apiserver').get({
                        'resource':'product.product_classification',
                        'data':param_data
                    })

                if not resp or resp['code'] != 200:
                    data['errcode'] = FAIL_GET_PRODUCT_CLASSIFICATIONS_CODE
                    data['errmsg'] = code2msg[FAIL_GET_PRODUCT_CLASSIFICATIONS_CODE]
                    return data
                #获取商品分类信息
                data_classifications = resp['data']

                if not data_classifications:
                    product['product_classification'] = 0
                    del product['classification_id']
                else:
                    #此为全部分类信息的集合
                    for classification in data_classifications:
                        if product['classification_id'] == classification['id']:
                            #商品详情里面分类信息组成
                            classification_info['second_level_id'] = classification['id']
                            classification_info['second_level_name'] = classification['name']
                            classification_info['first_level_id'] = classification['father_id']
                    for classification in data_classifications:
                        if classification['level'] == 1 and classification_info['first_level_id'] == classification['id']:
                            classification_info['first_level_name'] = classification['name']
                    product['product_classification'] = classification_info
                    del product['classification_id']

            else:
                product['product_classification'] = 0
                del product['classification_id']
            return product
        except:
            watchdog.error("get product_detail faled !!!=======>>>{}".format(unicode_full_stack()))
            data['errcode'] = FAIL_GET_PRODUCT_DETAIL_CODE
            data['errmsg'] = code2msg[FAIL_GET_PRODUCT_DETAIL_CODE]
            return data