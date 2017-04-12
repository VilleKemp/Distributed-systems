import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado import gen
from tornado.log import enable_pretty_logging

import random
import sys
import urllib
import time

port = 8888
 
enable_pretty_logging()



class GameHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("game.html")


if __name__=="__main__":

    application = tornado.web.Application([
        (r"/game/", GameHandler),
        ], debug=1)
    application.listen(port)
    print "gateway server in port " + str(port)
    tornado.ioloop.IOLoop.instance().start()
