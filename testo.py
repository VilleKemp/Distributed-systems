import tornado.ioloop
import tornado.web
import tornado.httpclient
import random
import sys
import argparse

import urllib
from subprocess import call, Popen, PIPE
import httplib2
httplib2.debuglevel=1
http=httplib2.Http()

if __name__ == '__main__':
    #p=Popen(["python", "/home/otso/distributed_systems/Distributed-systems/async_server.py", "8888"])
    #call(["python", "/home/otso/distributed_systems/Distributed-systems/async_server.py", "8889"])
    parser = argparse.ArgumentParser(description='Process server boot parameters')
    parser.add_argument('port', metavar='-p', type=int,
    help="Server's port number integer")
    http_client = tornado.httpclient.AsyncHTTPClient()
    post_data = { 'user': 'Seppo',
                    'guess':'Tails'} #A dictionary of your post data
    body = urllib.urlencode(post_data) #Make it into a post request
    response, content = http.request("http://localhost:8888/coordinator/", method='GET', headers=None, body=body) #Send it off!
    print "Response: "+content
    print "im done t. test"
