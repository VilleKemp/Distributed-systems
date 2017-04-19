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
PORT = '8888'
COORDPORT = 'coordinatorPort'
data = {COORDPORT:"None"}
class GameHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("game.html")

class StartupHandler(tornado.web.RequestHandler):

    #Handles new servers connecting to the grid
    def initialize(self, cache):
        self.cache = cache

    def get(self):
        """Tells connecting node the address of the coordinator"""
        global data
        self.write(data[COORDPORT])
        print "In GET: data updated: "
        print data

    def post(self):
        """receive coordinator's port number, to be used only when the coordinator is down"""
        content = self.request.body
        global data
        if data[COORDPORT]=="None":
            data[COORDPORT]=content
            print "new coordinatorPort: " + str(content)
        print "check" + str(data[COORDPORT])

if __name__=="__main__":

    application = tornado.web.Application([
        (r"/game/", GameHandler),
        (r"/startup/", StartupHandler, dict(cache = data)),
        ], debug=1)
    application.listen(int(PORT))
    print "gateway in port " + PORT
    tornado.ioloop.IOLoop.instance().start()
