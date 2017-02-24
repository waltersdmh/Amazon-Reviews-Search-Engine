import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sys
import main
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
global searchNo
global reviewArray 

#searchNo = 0
#serverReviewArray = []
#currenturl = ""


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')
        
    
        
        
    def on_message(self, message):
        print ('message received:  %s' % message)#message = keywords
       
        #send message as arugment to main.py
        main.main(message)
       
       
        print ('sending back message: %s' % "data.txt")
        
        with open('data.txt', 'r') as myfile:
            data=myfile.read().replace('\n', '')
        
        self.write_message(data)
        searchNo = 1
 
    def on_close(self):
        print ('connection closed')
       # searchNo = 0
       # serverReviewArray = []
    def check_origin(self, origin):
        return True



 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()