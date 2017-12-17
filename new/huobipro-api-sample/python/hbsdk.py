#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import urllib
import json

from urllib import parse
from urllib import request
from datetime import datetime

# timeout in 5 seconds:
TIMEOUT = 5

API_HOST = 'be.huobi.com'

SCHEME = 'https'

# language setting: 'zh-CN', 'en':
LANG = 'zh-CN'

DEFAULT_GET_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': LANG
}

DEFAULT_POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Accept-Language': LANG
}

class Dict(dict):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def _toDict(d):
    return Dict(**d)

class ApiError(BaseException):
    pass

class ApiNetworkError(BaseException):
    pass

class ApiClient(object):

    def __init__(self, appKey, appSecret, assetPassword=None, host=API_HOST):
        '''
        Init api client object, by passing appKey and appSecret.
        '''
        self._accessKeyId = appKey
        self._accessKeySecret = appSecret.encode('utf-8') # change to bytes
        self._assetPassword = assetPassword
        self._host = host
    
    def get(self, path, **params):
        '''
        Send a http get request and return json object.
        '''
        qs = self._sign('GET', path, self._utc(), params)
        return self._call('GET', '%s?%s' % (path, qs))

    def post(self, path, obj=None):
        '''
        Send a http post request and return json object.
        '''
        qs = self._sign('POST', path, self._utc())
        data = None
        if obj is not None:
            data = json.dumps(obj).encode('utf-8')
        return self._call('POST', '%s?%s' % (path, qs), data)

    def _call(self, method, uri, data=None):
        url = '%s://%s%s' % (SCHEME, self._host, uri)
        print(method + ' ' + url)
        headers = DEFAULT_GET_HEADERS if method=='GET' else DEFAULT_POST_HEADERS
        if self._assetPassword:
            headers['AuthData'] = self._auth_data()
        req = request.Request(url, data=data, headers=headers, method=method)
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            if resp.getcode()!=200:
                raise ApiNetworkError('Bad response code: %s %s' % (resp.getcode(), resp.reason))
            return self._parse(resp.read())

    def _parse(self, text):
        #print('Response:\n%s' % text)
        result = json.loads(text.decode('utf8'), object_hook=_toDict)
        print('result:%s'%result)
        if result.status=='ok':
            return result.data
        raise ApiError('%s: %s' % (result['err-code'], result['err-msg']))

    def _sign(self, method, path, ts, params=None):
        self._method = method
        # create signature:
        if params is None:
            params = {}
        params['SignatureMethod'] = 'HmacSHA256'
        params['SignatureVersion'] = '2'
        params['AccessKeyId'] = self._accessKeyId
        params['Timestamp'] = ts
        # sort by key:
        keys = sorted(params.keys())
        # build query string like: a=1&b=%20&c=:
        qs = '&'.join(['%s=%s' % (key, self._encode(params[key])) for key in keys])
        # build payload:
        payload = '%s\n%s\n%s\n%s' % (method, self._host, path, qs)
        # print('payload:\n%s' % payload)
        dig = hmac.new(self._accessKeySecret, msg=payload.encode('utf-8'), digestmod=hashlib.sha256).digest()
        sig = self._encode(base64.b64encode(dig).decode())
        # print('sign: ' + sig)
        qs = qs + '&Signature=' + sig
        return qs

    def _auth_data(self):
        md5 = hashlib.md5()
        md5.update(self._assetPassword.encode('utf-8'))
        md5.update('hello, moto'.encode('utf-8'))
        s = json.dumps({"assetPwd": md5.hexdigest()})
        return self._encode(s)

    def _utc(self):
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    def _encode(self, s):
        return parse.quote(s, safe='')
