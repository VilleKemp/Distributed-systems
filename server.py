import tornado.ioloop
import tornado.web
import tornado.httpclient
import random
import sys

import urllib

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


class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/form/" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        req=self.request.body
        self.write(req)
        #self.set_header("Content-Type", "text/plain")
        #self.write("You wrote " + self.get_body_argument("message"))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/coin/", CoinHandler),
        (r"/form/", MyFormHandler),
    ])
    application.listen(int(sys.argv[1]))
    tornado.ioloop.IOLoop.current().start()
