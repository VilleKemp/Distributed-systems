import tornado.ioloop
import tornado.web
import tornado.httpclient
import random
import sys

import urllib

from subprocess import Popen
p = Popen("server1.bat", cwd=r"C:\Users\Kempo\Desktop\lecture notes\Distributed systems\Course work\Work")
stdout, stderr = p.communicate()


http_client = tornado.httpclient.AsyncHTTPClient()
post_data = { 'user': 'Keijo',
              'guess': 'Tails'} #A dictionary of your post data
body = urllib.urlencode(post_data) #Make it into a post request
resp= http_client.fetch("http://localhost:8888/coordinator/", method='POST', headers=None, body=body) #Send it off!




