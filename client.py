#!/usr/bin/env/python
# -*- coding: utf-8 -*-
ADDRESS = '127.0.0.1'
PORT = 5000
MSG = ''


import os
import time
from random import shuffle
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
 
 
class DFSClientProtocol(WebSocketClientProtocol):
 
    # send message to server
    def onOpen(self):
        self.sendMessage(MSG)

    # get response from server 
    def onMessage(self, msg, binary):
        typeMsg = msg[:3]
        file_name = msg[4:16]
        if typeMsg == '[O]':
            message = msg[17:]
            file_path = str(".\\read\\"+file_name)
            f = open(file_path, 'w')
            f.write(message)
            f.close()
            print "File %s successfully writen at /read/ catalog..." % file_name
        elif typeMsg == '[C]':
            print "File successfully writen at some DFS catalog..."
        reactor.stop()


if __name__ == '__main__':
    import sys
    if len(sys.argv)<4:
        sys.exit("Using client.py [IP] [PORT] [COMMAND]")
    ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    MSG = sys.argv[3]
    factory = WebSocketClientFactory("ws://" + ADDRESS + ":" + str(PORT), debug = False)
    factory.protocol = DFSClientProtocol
    connectWS(factory)
    print 'connecting to %s port %s' % (ADDRESS, PORT)
    reactor.run()