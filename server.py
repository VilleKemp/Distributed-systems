from tornado.ioloop import IOLoop
from tornado import gen
import tornado.web
import tornado.httpclient
import random
import sys
import httplib2

import urllib
http = httplib2.Http()

from tornado.log import enable_pretty_logging
enable_pretty_logging()

class CoinHandler(tornado.web.RequestHandler):
    def get(self):
        value=random.randint(0,1)
        if (value):
            coin = "Heads"
        else:
            coin="Tails"
            
        
        self.write(coin)





class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")

    def post(self):
        http_client = tornado.httpclient.HTTPClient()
        post_data = {"jee": self.request.body[5:9]}
        body = urllib.urlencode(post_data)
        resp=http_client.fetch("http://localhost:8889/form/", method='POST', headers=None, body=body) #Send it off!
        self.write(resp.body)
        print "Mainhandler POST:" + resp.body

class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/form/" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        req=self.request.body
        self.write(req)
        print "Form handler POST: " + req
        
        
        #self.set_header("Content-Type", "text/plain")
        #self.write("You wrote " + self.get_body_argument("message"))
        #send shit
        
        

class CoordinatorHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@gen.engine
    def get(self):
        
        print "Coordinator GET: Send request to Node " 

        #body = urllib.urlencode(data)
        self.response,self.content= http.request("http://localhost:8889/node/","GET") #Send it off!
        print "Coordinator GET response: "  + self.content
        self._async_callback(self.content)

    def _async_callback(self, response):
        print "Controller " +response
        self.write(response)
        self.finish()
        #tornado.ioloop.IOLoop.instance().stop()   
        
                
class NodeHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    #@gen.engine
    def post(self):
        print "NODE POST: "
        data=self.request.body
        

    def get(self):
        print "Node GET: "
        #data=self.request.body
        value=random.randint(0,1)
        if (value):
            coin = "Heads"
        else:
            coin="Tails"
        
        print "Returning"
        self._async_callback(coin)   

    def _async_callback(self, response):
        print "node"+response
        self.write(response)
        self.finish()
        #tornado.ioloop.IOLoop.instance().stop()                
        
    
if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/coin/", CoinHandler),
        (r"/form/", MyFormHandler),
        (r"/coordinator/",CoordinatorHandler),
        (r"/node/",NodeHandler)
    ],debug=True)
    application.listen(int(sys.argv[1]))
    print "Server in port: " + sys.argv[1]
    tornado.ioloop.IOLoop.current().start()

