#!/usr/bin/env/python
# -*- coding: utf-8 -*-
OPERATION = ''
ADDRESS = '127.0.0.1'
PORT = 5000


import os
import time
from random import shuffle
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS


class FSClient(WebSocketClientProtocol):

    # event on new connection with client 
    def onOpen(self):
        self.sendMessage(OPERATION)

    # get response from fileserver
    def onMessage(self, msg, binary):
        print "%s" % msg
        reactor.stop()
    
    
if __name__ == '__main__':
    import sys
    if len(sys.argv)<3:
        sys.exit("Using fsclient.py [PORT] [COMMAND]")
    PORT = int(sys.argv[1])
    OPERATION = sys.argv[2]
    factory = WebSocketClientFactory("ws://" + ADDRESS + ":" + str(PORT), debug = False)
    factory.protocol = FSClient
    connectWS(factory)
    reactor.run()
    