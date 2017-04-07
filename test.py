import tornado.ioloop
import tornado.web
import tornado.httpclient
import random
import sys

import urllib

import httplib2
httplib2.debuglevel=1
http = httplib2.Http()

from subprocess import Popen
p = Popen("server1.bat", cwd=r"C:\Users\Kempo\Desktop\lecture notes\Distributed systems\Course work\Work")
stdout, stderr = p.communicate()



post_data = { 'user': 'Keijo',
              'guess': 'Tails'} #A dictionary of your post data
body = urllib.urlencode(post_data) #Make it into a post request
response,content= http.request("http://localhost:8888/coordinator/", method='GET', headers=None, body=body) #Send it off!

print "Response "+ content





