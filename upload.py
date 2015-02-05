#!/bin/env python2
# coding=utf-8

from urllib import urlencode, quote
import urllib2
import time, uuid
import hmac, hashlib
import json
import requests
import sys

GET_URL = 'http://api-content.dfs.kuaipan.cn/1/fileops/upload_locate'
UPLOAD_URL = '/1/fileops/upload_file'
CONSUMER_KEY = 'xcOTtkfpGekCp9rU'
CONSUMER_SECRET = 'uYOYpz6Y5WaiBUV4'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
ACCESS_TOKEN = ''

"""
params = [
    ('oauth_consumer_key', CONSUMER_KEY),
    ('oauth_token', OAUTH_TOKEN),
    ('oauth_signature_method', 'HMAC-SHA1'),
    ('oauth_timestamp', int(time.time())),
    ('oauth_nonce', uuid.uuid1().hex),
    ('oauth_version', 1.0),
    ]
"""

def get_signature(base_string):
    return hmac.new(CONSUMER_SECRET + '&' + OAUTH_TOKEN_SECRET, base_string, hashlib.sha1).digest().encode('base64').rstrip()

def get_base(method, url, params):
    return '%s&%s&%s' % (method, quote(url, ''), quote(urlencode(params)))

def get_params():
    params = [
        ('oauth_consumer_key', CONSUMER_KEY),
        ('oauth_token', OAUTH_TOKEN),
        ('oauth_signature_method', 'HMAC-SHA1'),
        ('oauth_timestamp', int(time.time())),
        ('oauth_nonce', uuid.uuid4().hex),
        ('oauth_version', 1.0),
    ]
    return params

"""
Params:
    1) Folder absolute address
    2) OAUTH_TOKEN
    3) OAUTH_TOKEN_SECRET
"""
    
if __name__ == '__main__':

#   initial work
    params = get_params()
    params.sort()
    OAUTH_TOKEN = sys.argv[2]
    OAUTH_TOKEN_SECRET = sys.argv[3]

#   get upload url
    base_string = get_base('GET', GET_URL, params)
    signature = get_signature(base_string)

    url = GET_URL + '?' + urlencode(params) + '&oauth_signature=' + signature

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    feedback = json.loads(response.read())
    
    url = feedback['url'].encode('utf-8') + UPLOAD_URL

#   print url

    params = get_params()
    params = params + [
                ('overwrite', 'True'),
                ('path',    '/'+sys.argv[1]),
                ('root',    'app_folder'),
                ]
    params.sort()

#    print params
#	construct post url 

    base_string = get_base('POST', url, params)
    signature = get_signature(base_string)

    url = url+'?'+urlencode(params)+'&oauth_signature='+signature

    files = {'file': open(sys.argv[1], 'rb')}

    r = requests.post(url, files= files)

    print r.status_code
    
    
