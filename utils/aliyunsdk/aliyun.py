# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
import json
from django.conf import settings

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

ACCESS_KEY_ID = settings.ACCESS_KEY_ID
ACCESS_KEY_SECRET = settings.ACCESS_KEY_SECRET


# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(ACCESS_KEY_ID,ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def send_sms(phone_numbers,code):

    business_id = uuid.uuid1()
    sign_name = settings.SIGN_NAME
    template_code = settings.TEMPLATE_CODE
    template_param = json.dumps({"code":code})

    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name)
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)
    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    print('阿里信息回执：', smsResponse.decode())
    return smsResponse




