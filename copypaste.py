import tornado.ioloop
import tornado.web

import httplib2
httplib2.debuglevel=1
http = httplib2.Http()

class AsyncHandler(tornado.web.RequestHandler):
        @tornado.web.asynchronous
        def get(self):
                self.response, self.content = http.request("http://google.co.in", "GET")
                self._async_callback(self.response)

        def _async_callback(self, response):
                print response.keys()
                self.finish()
                tornado.ioloop.IOLoop.instance().stop()

application = tornado.web.Application([
        (r"/", AsyncHandler)], debug=True)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
