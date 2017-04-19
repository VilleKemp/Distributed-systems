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
        """
        Renders the game
        """
        self.render("game.html")
        
class StartupHandler(tornado.web.RequestHandler):

    #Handles new servers connecting to the grid
    def initialize(self, cache):
        self.cache = cache

    def get(self):
        #Tells connecting node the address of the coordinator
        global data
        self.write(data[COORDPORT])
        print "In GET: data updated: "
        print data

    def post(self):
        #receive coordinator's port number
        port = self.request.body
        global data
        if data[COORDPORT]=="None":
            data[COORDPORT]=port
            #modifies the game.html to have the right coordinator port
            self.modify_html(port)
            print "new coordinatorPort: " + str(port)
        print "check" + str(data[COORDPORT])

    def modify_html(self,port):
        """Remakes the game.html to have the right coordinator port"""
        file=open("game.html",'w')
        file.write("""<html>
            <head>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"></script>
            <script>
            $(document).ready(function(){
                $("button").click(function(){
                    document.getElementById("response").innerHTML = "Loading...";
                    $.post("http://localhost:"""+port+"""/coordinator/",
                    JSON.stringify({
                      "guess" : $(this).attr('name'),
                      "filler" : "hh"
                    }),
                    function(response){
                        document.getElementById("response").innerHTML = response;
                    });
                });
            });
            </script>
            </head>
               <body>
              
            <button name="Heads"">HEAD</button>
            <button name= "Tails">TAILS</button>
             <p id="response"></p>


               </body>
             </html>""")
        file.close()
                    
        
if __name__=="__main__":

    application = tornado.web.Application([
        (r"/game/", GameHandler),
        (r"/startup/", StartupHandler, dict(cache = data)),
        ], debug=1)
    application.listen(int(PORT))
    print "gateway in port " + PORT
    tornado.ioloop.IOLoop.instance().start()
