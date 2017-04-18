import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado import gen
from tornado.log import enable_pretty_logging

import random
import sys
import urllib
import time

enable_pretty_logging()

class NodeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        self.write('sleepdarting the coinflip:\n')
        yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time()+5)
        value=random.randint(0,1)
        if (value):
            coin = "Heads"
        else:
            coin = "Tails"
        print "Returning coins"
        self._async_callback(coin)

    def _async_callback(self, response):
        print response
        self.write(response)
        self.finish()
        #running only 1 IOLoop, stopping closes the server
        #tornado.ioloop.IOLoop.instance().stop()

class CoordinatorHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()

        response = yield http_client.fetch("http://localhost:8889/node/", method='GET')

        data=self.request.body
        print "Coordinator GET: " + data
        self.write(response.body)
        print response
        self.finish()


    @gen.coroutine
    def post (self):
        print "POST"
        print self.request.body

        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8890/node/", method='GET')
        data=response.body

        self.write(data)
        self.finish()


    def set_default_headers(self):
        self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        self.add_header('Access-Control-Request-Method', 'POST')


if __name__=="__main__":

    application = tornado.web.Application([
        (r"/node/", NodeHandler),
        (r"/coordinator/", CoordinatorHandler),
        ], debug=1)
    application.listen(int(sys.argv[1]))
    print "Server in port " + sys.argv[1]
    tornado.ioloop.IOLoop.instance().start()
