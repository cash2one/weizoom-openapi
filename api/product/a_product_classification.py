# -*- coding: utf-8 -*-
"""@package api.product.a_product_classification
通知信息表结构

@author cdg
"""
import json

from eaglet.core import api_resource
from eaglet.decorator import param_required
from eaglet.core import watchdog
from eaglet.utils.resource_client import Resource
from util.error_codes import *

class AProductClassification(api_resource.ApiResource):
    """
    商品分类信息
    API:
        method: get
        url: mall/product_classifications/

    Args:
        取值以及说明:
          woid  : weapp_owner_id 
          product_id: 商品ID
    """
    app = "mall"
    resource = "product_classifications"

    def get(args):
        try:
            data = {}
            param_data = {'access_token':args['apiserver_access_token']}
            resp = Resource.use('apiserver').get({
                    'resource':'product.product_classifications',
                    'data':param_data
                })
            if not resp or resp['code'] != 200:
                data['errcode'] = FAIL_GET_PRODUCT_CLASSIFICATIONS_CODE
                data['errmsg'] = code2msg[FAIL_GET_PRODUCT_CLASSIFICATIONS_CODE]
                return data
            #获取商品分类信息
            if resp['data']:
                product_classifications = resp['data']

                classification_level_1 = []
                classification_level_2 = []
                #把商品的一级二级分类分成两个组
                for classification in product_classifications:
                    if classification['level'] == 1:
                        classification_level_1.append(classification)
                    if classification['level'] == 2:
                        classification_level_2.append(classification)
                #组织分类信息数据结构
                """
                for example:
                    {
                      'classifications':[
                          {
                            'first_level_id':11,
                            'first_level_name':'衣服',
                            'second_level_info':
                              [
                                {
                                  'second_level_id':1101,
                                  'second_level_name':'短袖'
                                },
                                ....
                              ]
                          },
                          ....
                      ]
                    }
                """
                data = {}
                classifications = []
                level1 = {}
                level2 = []
                level2_1 = {}
                for classification1 in classification_level_1:
                    level1['first_level_id'] = classification1['id']
                    level1['first_level_name'] = classification1['name']
                    for classification2 in classification_level_2:
                        if classification2['father_id'] == classification1['id']:
                            level2_1['second_level_id'] = classification2['id']
                            level2_1['second_level_name'] = classification2['name']
                            level2.append(level2_1)
                    level1['second_level_info'] = level2
                    classifications.append(level1)
                    level2 = []
                data['classifications'] = classifications
            else:
                data['errcode'] = PRODUCT_CLASSIFICATIONS_IS_NULL_CODE
                data['errmsg'] = code2msg[PRODUCT_CLASSIFICATIONS_IS_NULL_CODE]
            return data
        except:
            data['errcode'] = FAIL_GET_PRODUCT_CLASSIFICATIONS_CODE
            data['errmsg'] = code2msg[FAIL_GET_PRODUCT_CLASSIFICATIONS_CODE]
            return data
