# -*- coding: utf-8 -*-
import json
#import time
from datetime import datetime

import settings
from client import Client
from db.account.models import User, UserProfile
from utils import string_util
from db.member import models as member_models
from db.mall import models as mall_models
from eaglet.core import watchdog
from business.account.member import Member

tc = None

BOUNDARY = 'BoUnDaRyStRiNg'
MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY

class WeappClient(Client):
	def __init__(self, enforce_csrf_checks=False, **defaults):
		super(WeappClient, self).__init__(**defaults)

	def request(self, **request):
		if settings.DUMP_TEST_REQUEST:
			print '\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
			print '{{{ request'
	
		response = super(WeappClient, self).request(**request)
	
		if settings.DUMP_TEST_REQUEST:
			print '}}}'
			print '\n{{{ response'
			print self.cookies
			print '}}}'
			print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
		return response


	def reset(self):
		self.cookies = SimpleCookie()
		if hasattr(self, 'user'):
			self.user = User()



###########################################################################
# login: 登录系统
###########################################################################
class Obj(object):
	def __init__(self):
		pass

def login(user, password=None, **kwargs):
	if not password:
		password = 'test'

	if 'context' in kwargs:
		context = kwargs['context']
		if hasattr(context, 'client'):
			if context.client.webapp_user and context.client.webapp_user.username == user:
				#如果已经登录了，且登录用户与user相同，直接返回
				return context.client
			else:
				#如果已经登录了，且登录用户不与user相同，退出登录
				context.client.webapp_user = None

	#client = WeappClient(HTTP_USER_AGENT='WebKit MicroMessenger Mozilla')
	client = Client()
	client.webapp_user = Obj()
	client.webapp_user.username = user

	if 'context' in kwargs:
		context = kwargs['context']
		context.client = client

	return client


###########################################################################
# get_user_id_for: 获取username对应的user的id
###########################################################################
def get_user_id_for(username):
	return User.get(User.username == username).id


def get_member_for(username, webapp_id):
	"""
	获取username对应的会员
	"""
	if isinstance(username, unicode):
		member_nickname_str = username.encode('utf-8')
	else:
		member_nickname_str = username
	username_hexstr = string_util.byte_to_hex(member_nickname_str)
	buf = []
	buf.append('=======================')
	buf.append(webapp_id)
	buf.append(username_hexstr)
	buf.append('=======================')
	print '\n'.join(buf)
	try:
		return member_models.Member.get(webapp_id=webapp_id, username_hexstr=username_hexstr)
	except:
		member = member_models.Member(id=1, grade_id=0)
		return member


###########################################################################
# nginx: 模拟nginx的转换
###########################################################################
def nginx(url):
	if url.startswith('/workbench/'):
		return '/termite%s' % url
	else:
		return url


def get_date(str):
	"""
		将字符串转成datetime对象
		今天 -> 2014-4-18
	"""
	#处理expected中的参数
	today = datetime.now()
	if str == u'今天':
		delta = 0
	elif str == u'昨天':
		delta = -1
	elif str == u'前天':
		delta = -2
	elif str == u'明天':
		delta = 1
	elif str == u'后天':
		delta = 2
	elif u'天后' in str:
		delta = int(str[:-2])
	elif u'天前' in str:
		delta = 0-int(str[:-2])
	else:
		tmp = str.split(' ')
		if len(tmp) == 1:
			strp = "%Y-%m-%d"
		elif len(tmp[1]) == 8:
			strp = "%Y-%m-%d %H:%M:%S"
		elif len(tmp[1]) == 5:
			strp = "%Y-%m-%d %H:%M"
		return datetime.strptime(str, strp)

	return today + timedelta(delta)

def get_date_to_time_interval (str):
	"""
		将如下格式转化为字符串形式的时间间隔
		今天 -> 2014-2-13|2014-2-14
		"3天前-1天前" 也转为相同的格式
	"""
	date_interval = None
	if u'-' in str:
		m = re.match(ur"(\d*)([\u4e00-\u9fa5]{1,2})[-](\d*)([\u4e00-\u9fa5]{1,2})", unicode(str))
		result = m.group(1, 2, 3, 4)
		if result:
			if result[1] == u'天前' and result[3] == u'天前':
				date_interval = "%s|%s" % (datetime.strftime(datetime.now()-timedelta(days=int(result[0])), "%Y-%m-%d"), datetime.strftime(datetime.now() - timedelta(days=int(result[2])),"%Y-%m-%d"))
			if result[1] == u'天前' and result[2] == u'' and result[3] == u'今天':
				date_interval = "%s|%s" % (datetime.strftime(datetime.now() - timedelta(days=int(result[0])),"%Y-%m-%d"), datetime.strftime(datetime.now(),"%Y-%m-%d"))
			if result[1] == u'今天' and result[3] == u'明天':
				date_interval = "%s|%s" % (datetime.strftime(datetime.now(), "%Y-%m-%d"), datetime.strftime(datetime.now() + timedelta(days=1),"%Y-%m-%d"))
	return date_interval

def get_date_str(str):
	date = get_date(str)
	return date.strftime('%Y-%m-%d')

def get_datetime_str(str):
	"""保留小时数
	"""
	date = get_date(str)
	return '%s 00:00:00' % date.strftime('%Y-%m-%d')

def get_datetime_no_second_str(str):
	date = get_date(str)
	return '%s 00:00' % date.strftime('%Y-%m-%d')
	

###########################################################################
# assert_dict: 验证expected中的数据都出现在了actual中
###########################################################################
def assert_dict(expected, actual):
	global tc
	is_dict_actual = isinstance(actual, dict)
	for key in expected:
		expected_value = expected[key]
		if is_dict_actual:
			actual_value = actual[key]
		else:
			actual_value = getattr(actual, key)

		if isinstance(expected_value, dict):
			assert_dict(expected_value, actual_value)
		elif isinstance(expected_value, list):
			assert_list(expected_value, actual_value)
		else:
			try:
				tc.assertEquals(expected_value, actual_value)
			except Exception, e:
				items = ['\n<<<<<', 'e: %s' % str(expected), 'a: %s' % str(actual), 'key: %s' % key, e.args[0], '>>>>>\n']
				e.args = ('\n'.join(items),)
				raise e


###########################################################################
# assert_list: 验证expected中的数据都出现在了actual中
###########################################################################
def assert_list(expected, actual):
	global tc
	tc.assertEquals(len(expected), len(actual))

	for i in range(len(expected)):
		expected_obj = expected[i]
		actual_obj = actual[i]
		if isinstance(expected_obj, dict):
			assert_dict(expected_obj, actual_obj)
		else:
			try:
				tc.assertEquals(expected_obj, actual_obj)
			except Exception, e:
				items = ['\n<<<<<', 'e: %s' % str(expected), 'a: %s' % str(actual), 'key: %s' % key, e.args[0], '>>>>>\n']
				e.args = ('\n'.join(items),)
				raise e


###########################################################################
# assert_expected_list_in_actual: 验证expected中的数据都出现在了actual中
###########################################################################
def assert_expected_list_in_actual(expected, actual):
	global tc

	for i in range(len(expected)):
		expected_obj = expected[i]
		actual_obj = actual[i]
		if isinstance(expected_obj, dict):
			assert_dict(expected_obj, actual_obj)
		else:
			try:
				tc.assertEquals(expected_obj, actual_obj)
			except Exception, e:
				items = ['\n<<<<<', 'e: %s' % str(expected), 'a: %s' % str(actual), 'key: %s' % key, e.args[0], '>>>>>\n']
				e.args = ('\n'.join(items),)
				raise e


###########################################################################
# assert_api_call_success: 验证api调用成功
###########################################################################
def assert_api_call_success(response):
	if 200 != response.body['code']:
		buf = []
		buf.append('>>>>>>>>>>>>>>> response <<<<<<<<<<<<<<<')
		buf.append(str(response))
		watchdog.error("API calling failure: %s" % '\n'.join(buf))
	assert 200 == response.body['code'], "code != 200, call api FAILED!!!!"


###########################################################################
# print_json: 将对象以json格式输出
###########################################################################
def print_json(obj):
	print json.dumps(obj, indent=True)


def table2dict(context):
	expected = []
	for row in context.table:
		data = {}
		for heading in row.headings:
			if ':' in heading:
				real_heading, value_type = heading.split(':')
			else:
				real_heading = heading
				value_type = None
			value = row[heading]
			if value_type == 'i':
				value = int(value)
			if value_type == 'f':
				value = float(value)
			data[real_heading] = value
		expected.append(data)
	return expected


def get_order_has_product(order_code, product_name):
	"""
	从Weapp `test/bdd_util.py`迁移过来

	@todo 待优化；用业务模型描述
	"""
	def _get_product_model_name(product_model_names):
		if product_model_names != "standard":
			pro_id, id = product_model_names.split(":")
			#i = mall_models.ProductModelPropertyValue.get(id=id)
			i = mall_models.ProductModelPropertyValue.select().dj_where(id=id, property_id=pro_id).first()#get(id=id, property_id=pro_id)
			return i.name
	order = mall_models.Order.get(order_id=order_code)

	# 商品是否包含规格
	if ":" in product_name:
		product_name, product_model_name = product_name.split(":")
		
	order_has_product_list = mall_models.OrderHasProduct.select().dj_where(order_id=order.id, product_name=product_name)

	if order_has_product_list.count() == 1:
		# 如果商品不包含规格
		return order_has_product_list[0]
	else:
		# 如果商品包含规格
		# 查找到包含此规格的order_has_product
		for order_has_product in order_has_product_list:
			if product_model_name in _get_product_model_name(order_has_product.product_model_name):
				return order_has_product
	return None


def get_webapp_id_for(username):
	"""
	获取user对应的webapp id
	"""
	user = User.get(username=username)
	profile = UserProfile.get(user=user)
	return profile.webapp_id


def get_product_by(product_name):
	product = mall_models.Product.get(name=product_name)
	return product

def get_member_by_id(member_id):
	return Member.from_id({'webapp_owner': None, 'member_id': member_id})


bdd_mock = {
	'notify_mail': ''
}


def set_bdd_mock(mock_type, mock_content):
	bdd_mock[mock_type] = mock_content


def get_bdd_mock(mock_type):
	return bdd_mock[mock_type]
