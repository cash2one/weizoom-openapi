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
from util.error_codes import *

class AProductCatalogs(api_resource.ApiResource):
    """
    商品分类信息
    API:
        method: get
        url: mall/product_catalogs/

    Args:
        取值以及说明:
          woid  : weapp_owner_id 
          product_id: 商品ID
    """
    app = "mall"
    resource = "product_catalogs"

    @param_required(['woid'])
    def get(args):
        #返回三方的响应数据结构
        data = {}
        try:
            param_data = {'access_token':args['apiserver_access_token']}
            resp = Resource.use('apiserver').get({
                    'resource':'product.product_catalogs',
                    'data':param_data
                })
            if not resp or resp['code'] != 200:
                data['errcode'] = FAIL_GET_PRODUCT_CATALOGS_CODE
                data['errmsg'] = code2msg[FAIL_GET_PRODUCT_CATALOGS_CODE]
                return data
            #获取商品分类信息
            product_catalogs = resp['data'] or ''
            catalog_level_1 = []
            catalog_level_2 = []
            #把商品的一级二级分类分成两个组
            for catalog in product_catalogs:
                if catalog.level == '1':
                    catalog_level_1.append(catalog)
                if catalog.level == '2':
                    catalog_level_2.append(catalog)
            #组织分类信息数据结构
            """
            for example:
                {'catalogs':[{'first_level_id':11,'first_level_name':'衣服','second_level_info':[{'second_level_id':1101,'second_level_name':'短袖'},....]]}
            """
            data = {}
            catalogs = []
            level1 = {}
            level2 = []
            level2_1 = {}
            for catalog1 in catalog_level_1:
                level['first_level_id'] = catalog1.id
                level['first_level_name'] = catalog1.name
                for  catalog2 in catalog_level_2:
                    if catalog2.father_id == catalog1.id:
                        level2_1['second_level_id'] = catalog2.id
                        level2_1['second_level_name'] = catalog2.name
                        level2.append(level2_1)
                level['second_level_info'] = level2
                catalogs.append(level1)
                level2 = []

            data['catalogs'] = catalogs
            return data
        except:
            data['errcode'] = FAIL_GET_PRODUCT_CATALOGS_CODE
            data['errmsg'] = code2msg[FAIL_GET_PRODUCT_CATALOGS_CODE]
            return data