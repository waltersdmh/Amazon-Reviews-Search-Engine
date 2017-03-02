import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sys
import os
import main
'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
''' 
 

#searchNo = 0
#serverReviewArray = []
#currenturl = ""


class WSHandler(tornado.websocket.WebSocketHandler):
    
    clients = []
    
    
    def check_origin(self, origin):
        return True
        
        
    def open(self):
        print ('new connection')
        #clientCode = str(self)[-11:-1]
        #print(clientCode)
        self.clients.append(self)
    
        
    def on_close(self):
        self.clients.remove(self)
        print ('connection closed')
        clientCode = str(self)[-11:-1]
        os.remove(clientCode+".txt")
       # searchNo = 0
       # serverReviewArray = []
       
    def on_message(self, message):
        print ('message received:  %s' % message)#message = keywords
        clientCode = str(self)[-11:-1]
        main.main(message, clientCode)
        print ('sending back message: %s' % clientCode+".txt")
        with open(clientCode+".txt", "r") as myfile:
            data=myfile.read().replace('\n', '')
        self.write_message(data)


 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)

    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()