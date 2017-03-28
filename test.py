import tornado.ioloop
import tornado.web
import tornado.httpclient
import random
import sys

import urllib

http_client = tornado.httpclient.AsyncHTTPClient()
post_data = { 'message': 'test data' } #A dictionary of your post data
body = urllib.urlencode(post_data) #Make it into a post request
resp=http_client.fetch("http://localhost:8888/form/", method='POST', headers=None, body=body) #Send it off!
data= resp
print yield resp


