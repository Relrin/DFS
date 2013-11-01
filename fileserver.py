#!/usr/bin/env/python
# -*- coding: utf-8 -*-
ADDRESS = '127.0.0.1'
PORT = 5001
CATALOG_NAME = ''
FILES_PATH = ''


import time
from socket import gethostbyaddr
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS


class FS(WebSocketServerProtocol):
    
    # event for new connection with client
    def onOpen(self):
        peer = self.transport.getPeer()
        print "[USER][%s] User with %s connected" % (time.strftime("%H:%M:%S"), peer)

    # event for disconnect
    def connectionLost(self, reason):
        print '[USER][%s] Lost connection from %s' % (time.strftime("%H:%M:%S"), self.transport.getPeer())
    
    # get request from client
    def onMessage(self, msg, binary):
        typeMsg = msg[:3]
        file_name = msg[4:16]
        if typeMsg == '[W]':
            print "[W][%s] Write %s file into %s" % (time.strftime("%H:%M:%S"), file_name, CATALOG_NAME)
            message = msg[17:]
            file_path = FILES_PATH + file_name
            f = open(file_path, 'w')
            f.write(message)
            f.close()
            print "File %s successfully writen..." % file_name
            self.sendMessage('[C]['+file_name+']OK')
        elif typeMsg == '[R]':
            print "[R][%s] Read %s file from %s" % (time.strftime("%H:%M:%S"), file_name, CATALOG_NAME)
            print "File %s successfully read..." % file_name
            file_path = FILES_PATH + file_name
            f = open(file_path, 'r')
            message = '[O]['+file_name+']' + f.read()
            f.close()
            self.sendMessage(message)
    
   
if __name__ == '__main__':
    import sys
    if len(sys.argv)<4:
        sys.exit("Using fileserver.py [IP] [PORT] [file_catalog_name]")
    ADDRESS = str(sys.argv[1])
    PORT = int(sys.argv[2])
    CATALOG_NAME = str(sys.argv[3])
    FILES_PATH = '.\\data\\' + CATALOG_NAME + '\\'
    factory = WebSocketServerFactory("ws://" + ADDRESS + ":" + str(PORT), debug = False)
    factory.protocol = FS
    listenWS(factory)
    print 'Server starting up on %s port %s' % (ADDRESS, PORT)
    reactor.run()