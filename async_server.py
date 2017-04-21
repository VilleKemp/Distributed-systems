import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado import gen
from tornado.log import enable_pretty_logging

import random
import sys
import urllib
import time

import json

import httplib2
httplib2.debuglevel=1
http=httplib2.Http()


enable_pretty_logging()

GATEWAY = "http://localhost:8888/startup/"
COORDPORT = 'coordinatorPort'
nodes = 'nodes'
cache = {COORDPORT:"None", nodes:{}}
nodeWorkload = 0
server = None #server object

class Node:
    #"""Implements Node object logic"""

    def informCoordinator(self):
        """send address to coordinator"""
        address="http://localhost:%s/listnode/" % cache[COORDPORT]
        response, content = http.request(address, method='POST', headers=None, body=str(sys.argv[1]))
        print "Class Node: Port " + str(sys.argv[1]) + " sent to Coordinator in port: " + cache[COORDPORT]
    def Bully(self,nodes):
        """implements the Bully algorithm"""
        pass


class Coordinator:
    #"""Implements Coordinator object logic"""

    def checkWorkload(self, port, workload):
        address = "http://localhost:%s/getstate/" % port
        response, content = http.request(address, method='GET')
        if int(content) <= workload: #assumes that other workloads are correct
            print"class Coordinator: checkState(): workload confirmed at %s with %s" %(address, content)
            cache[nodes][port]+=1 #+1 to selected workload
            return True
        else:
            print "class Coordinator: checkState(): workloads do not match at: %s with %s. (Local info was %s)" %(address, content, workload)
            cache[nodes][port]=int(content) #correct local workload info if actual workload was higher
            return False

    def selectWorker(self):
        """selects the node with lowest workload for performing calculation"""
        min_ = float("inf")
        selected = None

        print "class Coordinator: selectWorker(): cache = "
        print cache[nodes]
        if cache[nodes]:
            for key, value in cache[nodes].items():
                if int(value)< min_:
                    selected = key
                    min_=int(value)

            print "class Coordinator: selectWorker(): selected worker: " + selected

            if not self.checkWorkload(selected, min_):
                self.selectWorker()

        else:
            print "class Coordinator: selectWorker(): no cache[nodes], returning None"
        return selected


    def forwardCalculation(node):
        """Fordwards calculations to a node"""
        pass
    def refreshWorkerLoads(self):
        pass

class NodeHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        """
        Game logic. Takes the users guess and compares it to self generated coinflip.
        """
        #Timeout for testing purposes
        global nodeWorkload
        nodeWorkload +=1
        print "NodeHandler: workload added at %s. Workload %d" %(sys.argv[1], nodeWorkload)
        yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time()+5)
        #generate coin-flip
        value=random.randint(0,1)
        if (value):
            coin = "Heads"
        else:
            coin = "Tails"
        print "Returning coins"
        #turns request body to json format for easier use
        guess=json.loads(self.request.body)

        #checks the winner and generates answer string
        if (guess['guess']==coin):
            answer="You guessed "+guess['guess']+" coin flip was "+ coin +". You win!"
        else:
            answer="You guessed "+guess['guess']+" coin flip was "+ coin +". You lose!"

        self._async_callback(answer)

    def _async_callback(self, response):
        print response
        self.write(response)
        global nodeWorkload
        nodeWorkload -= 1
        print "NodeHandler: workload reduced at %s. Workload %d" %(sys.argv[1], nodeWorkload)
        self.finish()
        #running only 1 IOLoop, stopping closes the server
        #tornado.ioloop.IOLoop.instance().stop()

class CoordinatorHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def get(self):
        print "Coordinator GET"

    @gen.coroutine
    def post (self):
        """
        Takes clients request, forwards it to node
        which calculates the game result and then responds the result to client
        """
        http_client = tornado.httpclient.AsyncHTTPClient()
        worker = server.selectWorker()
        SLAVE = "http://localhost:%s/node/" % worker
        print "CoordinatorHandler POST: Workload sent to " + SLAVE
        #sends post to node for game results
        response = yield http_client.fetch(SLAVE,handle_response, method='POST',body=self.request.body)

        return_value=response.body
        #Return the string which came from the node
        self.write(return_value)
        cache[nodes][worker] -= 1 #remove load from worklist
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
            print "ListNodeHandler POST: Added node to cache: "+ str(cache[nodes])
        else:
            print "ListNodeHandler POST: Couldn't convert content to int" + str(content)

class GetStateHandler(tornado.web.RequestHandler):
    #interface for requesting node's workload info
    @gen.coroutine
    def get(self):

        self.write(str(nodeWorkload))
        self.finish()

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

def handle_response(response):
    if response.error:
        print("Errorhandler: Error %s" % response.error)
    else:
        print(response.body)

if __name__=="__main__":

    application = tornado.web.Application([
        (r"/node/", NodeHandler),
        (r"/coordinator/", CoordinatorHandler),
        (r"/listnode/", ListNodeHandler, dict(cache=cache)),
        (r"/getstate/", GetStateHandler)
        ], debug=1)
    main()
    application.listen(int(sys.argv[1]))
    print "Server in port " + sys.argv[1]
    tornado.ioloop.IOLoop.instance().start()
