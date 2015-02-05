#!/usr/bin/env python2
# coding=utf-8

from urllib import urlencode, quote
import urllib2
import time, uuid
import hmac, hashlib
import json

REQUEST_URL = 'https://openapi.kuaipan.cn/open/requestToken'
AUTHORIZE_URL = 'https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token='
ACCESS_URL = 'https://openapi.kuaipan.cn/open/accessToken'

CONSUMER_KEY = 'xcOTtkfpGekCp9rU'
CONSUMER_SECRET = 'uYOYpz6Y5WaiBUV4'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
ACCESS_TOKEN = ''

"""
params FOR EXAMPLE

params = [
    ('oauth_consumer_key', CONSUMER_KEY),
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
    ('oauth_signature_method', 'HMAC-SHA1'),
    ('oauth_timestamp', int(time.time())),
    ('oauth_nonce', uuid.uuid1().hex),
    ('oauth_version', 1.0),
    ]
    return params

if __name__ == '__main__':

#   initial work
    params = get_params()
    params.sort()
    
#   request template token
    base_string = get_base('GET', REQUEST_URL, params)
    signature = get_signature(base_string)

    url = REQUEST_URL+'?'+ urlencode(params) + '&oauth_signature=' + signature

#    print url

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

    feedback = json.loads(response.read())
#	template token
    OAUTH_TOKEN = feedback['oauth_token'].encode('utf-8')
    OAUTH_TOKEN_SECRET = feedback['oauth_token_secret'].encode('utf-8')

#    print OAUTH_TOKEN
#    print OAUTH_TOKEN_SECRET

#   Add token to params

    params = get_params()
    params.append(('oauth_token', OAUTH_TOKEN))
    params.sort()

#   get authorizing
    print 'Please enter this url to authorise this application: \n' + AUTHORIZE_URL + OAUTH_TOKEN

    AUTHORIZE_KEY = raw_input('Verifier: ')

#   ACCESS TOKEN

    base_string = get_base('GET', ACCESS_URL, params)
    signature = get_signature(base_string)
                              
    url = ACCESS_URL + '?' + urlencode(params) + '&oauth_signature=' + signature

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)

#	get authorized token

    feedback = json.loads(response.read())
    OAUTH_TOKEN = feedback['oauth_token'].encode('utf-8')
    OAUTH_TOKEN_SECRET = feedback['oauth_token_secret'].encode('utf-8')

    print 'OAUTH_TOKEN:', OAUTH_TOKEN
    print 'OAUTH_TOKEN_SECRET:', OAUTH_TOKEN_SECRET

#	save token
    f = open('token', 'w')

    folders = raw_input('Please input the folders you want to backup(separated by ;)\ne.g: /home/user/Documents\n')
    f.write('TOKEN='+OAUTH_TOKEN+'\nTOKEN_SECRET='+OAUTH_TOKEN_SECRET+'\nFOLDERS='+folders+'\n')
    f.close()
