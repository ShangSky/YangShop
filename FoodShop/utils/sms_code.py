# -*- coding: utf-8 -*-
from __future__ import print_function
import ssl
import hmac
import base64
import hashlib
from datetime import datetime as pydatetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
from random import choice


class SmsCode(object):

    def __generate_code(self, code_length):
        """
        生成四位验证码
        :return:
        """
        seeds = '1234567890'
        code = ''.join([choice(seeds) for i in range(code_length)])
        return code

    def send_sms(self, mobile, code_length):
        code = self.__generate_code(code_length)
        secret_id = ""
        secret_key = ""
        source = "market"
        datetime = pydatetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        sign_str = "x-date: %s\nx-source: %s" % (datetime, source)
        sign = base64.b64encode(hmac.new(secret_key.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha1).digest())
        auth = 'hmac id="%s", algorithm="hmac-sha1", headers="x-date x-source", signature="%s"' % (
        secret_id, sign.decode('utf-8'))

        query_params = {'mobile': mobile, 'param': 'code:{}'.format(code), 'tpl_id': ''}
        url = 'http://service-4xrmju6b-1255399658.ap-beijing.apigateway.myqcloud.com/release/dxsms'
        url = url + '?' + urlencode(query_params)
        request = Request(url, headers={'X-Source': source, 'X-Date': datetime, 'Authorization': auth})
        request.get_method = lambda: 'GET'
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        result = urlopen(request, context=ctx).read().decode('utf-8')
        return code, json.loads(result)
