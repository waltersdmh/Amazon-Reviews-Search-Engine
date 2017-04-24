import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sys
import os
import main


class WSHandler(tornado.websocket.WebSocketHandler):
    #asynchronous connections through list
    clients = []
    
    def check_origin(self, origin):
        return True
        
    #add client to list on connection
    def open(self):
        print ('new connection')
        self.clients.append(self)
    
    #remove client from the list if they close extension
    #remove all communciation data - this includes their resutls.
    def on_close(self):
        self.clients.remove(self)
        print ('connection closed')
        clientCode = str(self)[-11:-1]
        os.remove(clientCode+".txt")
    
    #on request
    #call main.main
    #create a text file for data transmit using client code. 
    def on_message(self, message):
        print ('message received:  %s' % message)
        clientCode = str(self)[-11:-1]  #client identifier
        main.main(message, clientCode)  #message = key-terms, filter settings, product code
        print ('sending back message: %s' % clientCode+".txt")
        with open(clientCode+".txt", "r") as myfile:    #create file for send
            data=myfile.read().replace('\n', '')        
        self.write_message(data)    #insert data to file

application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
#tornado web-socket. creating using tutorial @: http://www.tornadoweb.org/en/stable/httpserver.html#http-server
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()