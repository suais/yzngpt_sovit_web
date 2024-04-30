from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def send_sms(phone="13683697439"):
    """
    pip install aliyun-python-sdk-core
    pip install aliyun-python-sdk-dysmsapi
    """
    access_key_id = ""
    access_key_secret = ""
    client = AcsClient(access_key_id, access_key_secret, 'default')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', '振南知波')
    request.add_query_param('TemplateCode', 'SMS_274905410')
    request.add_query_param('TemplateParam', '{"code":"123456"}')  # 替换为实际的信息
    response = client.do_action(request)