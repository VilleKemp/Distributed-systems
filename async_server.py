import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado import gen
from tornado.log import enable_pretty_logging

import random
import sys
import urllib
import time
import httplib2
httplib2.debuglevel=1
http=httplib2.Http()

enable_pretty_logging()

GATEWAY = "http://localhost:8888/startup/"
COORDPORT = 'coordinatorPort'
nodes = 'nodes'
cache = {COORDPORT:"None", nodes:{}}

server = None #server object

class Node:
    #"""Implements Node object logic"""

    def __init__(self):
        pass
    def informCoordinator(self):
        """send address to coordinator"""
        COORDINATOR="http://localhost:%s/listnode/" % cache[COORDPORT]
        response, content = http.request(COORDINATOR, method='POST', headers=None, body=str(sys.argv[1]))
        print "Class Node: Port " + str(sys.argv[1]) + " sent to Coordinator in port: " + cache[COORDPORT]
    def Bully(self,nodes):
        """implements the Bully algorithm"""
        pass



class Coordinator:
    #"""Implements Coordinator object logic"""
    def __init__(self):
        self.workerLoads = dict()

    def selectWorker(self):
        """selects the node with lowest workload for performing calculation"""
        min_ = float("inf")
        selected = None
        if cache[nodes]:
            for key, value in cache[nodes].items():
                if str(value)< min_:
                    selected = key
            cache[nodes][selected]+=1 #+1 to selected workload

        else:
            print "class Coordinator selectWorker(): no cache[nodes], returning None"
        return selected

    def forwardCalculation(node):
        """Fordwards calculations to a node"""
        pass
    def updateWorkerLoads(self):
        pass

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
        print "CoordinatorHandler GET: " + data
        self.write(response.body)
        print response
        self.finish()

    @gen.coroutine
    def post (self):
        """Takes in data and requests calculations from node"""
        print "CoordinatorHandler POST"
        print self.request.body

        http_client = tornado.httpclient.AsyncHTTPClient()
        SLAVE = "http://localhost:%s/node/" % server.selectWorker()
        print "CoordinatorHandler POST: Workload sent to " + SLAVE
        response = yield http_client.fetch(SLAVE, method='GET')
        data=response.body

        self.write(data)
        self.finish()

    def set_default_headers(self):
        self.add_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))
        self.add_header('Access-Control-Request-Method', 'POST')

class ListNodeHandler(tornado.web.RequestHandler):
    #A request handler for the coordinator
    def initialize(self, cache):
        self.cache=cache

    @gen.coroutine
    def post(self):
        #post node's address to the coordinator
        content = self.request.body
        global cache
        if int(content):
            cache[nodes][str(content)]=0 #add node to worker list with 0 load
            print "ListNodeHandler POST: Added node to cache: "+ str(content)
        else:
            print "ListNodeHandler POST: Couldn't convert content to int"


def startServer():
    """Greet Gateway and determine the role of the instance"""
    response, content = http.request(GATEWAY, method='GET', headers=None, body=None) #Send it off!
    print "Response from gateway on get: "+content
    if content == "None":
        #Tell port number to Gateway and instantiate a coordinator
        print "sending port via post"
        post_data = {"port":sys.argv[1]}
        body = urllib.urlencode(post_data)
        response, content = http.request(GATEWAY, method='POST', headers=None, body=str(sys.argv[1]))
        global server
        server = Coordinator()
        cache[COORDPORT]=sys.argv[1]
    elif int(content):
        cache[COORDPORT]=content
        global server
        server = Node()
        server.informCoordinator()

    return server

def main():
    #boot up and determine the role of the instance
    startServer()


if __name__=="__main__":

    application = tornado.web.Application([
        (r"/node/", NodeHandler, dict(cache=cache)),
        (r"/coordinator/", CoordinatorHandler),
        (r"/listnode/", ListNodeHandler, dict(cache=cache))
        ], debug=1)
    main()
    application.listen(int(sys.argv[1]))
    print "Server in port " + sys.argv[1]
    tornado.ioloop.IOLoop.instance().start()