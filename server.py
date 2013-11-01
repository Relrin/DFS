#!/usr/bin/env/python
# -*- coding: utf-8 -*-
ADDRESS = '127.0.0.1'
PORT = 5000

SERVERS = 0
FILES = {}
SERVERS_PORT = [5001, 5002, 5003, 5004]
SERVER_NAMES = ('fs1', 'fs2', 'fs3', 'fs4')
BYTES_SERVERS = [0, 0, 0, 0]


import time
import os
from subprocess import Popen, PIPE, STDOUT
from socket import gethostbyaddr
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS


class DFS(WebSocketServerProtocol):

    # get data about used storage on disk
    def __used_servers(self):
        for server in xrange(0, len(BYTES_SERVERS)):
            print "Fileserver #%d: %d bytes" % (int(server+1), int(BYTES_SERVERS[server])) 
   
    # balancer for write operations   
    def __balancer_write(self, msg):
        index_server = 0
        if SERVERS == 2:
            b_server_new = BYTES_SERVERS[:2]
            used_minimal = min(b_server_new)
            index_server = b_server_new.index(used_minimal)
        elif SERVERS == 4:
            used_minimal = min(BYTES_SERVERS)
            index_server = BYTES_SERVERS.index(used_minimal)
        BYTES_SERVERS[index_server] += len(msg) 
        return index_server
    
    # balancer for read operations
    def __balancer_read(self, file_name):
        server = FILES[file_name]
        return SERVER_NAMES.index(server)
    
    # event for create new connection with client
    def onOpen(self):
        peer = self.transport.getPeer()
        print "[USER][%s] User with %s connected" % (time.strftime("%H:%M:%S"), peer)

    # event for disconnect client 
    def connectionLost(self, reason):
        print '[USER][%s] Lost connection from %s' % (time.strftime("%H:%M:%S"), self.transport.getPeer())
    
    # get request from client, and resend request for fileserver
    def onMessage(self, msg, binary):
        self.__used_servers()
        typeMsg = msg[:3]
        file_name = msg[4:16]
        message = msg[17:]
        if typeMsg == '[W]':
            print "[W][%s] Write %s file into DFS" % (time.strftime("%H:%M:%S"), file_name)
            index = self.__balancer_write(message)
            FILES[file_name] = SERVER_NAMES[index]
            p = Popen(["python", "fsclient.py", str(SERVERS_PORT[index]), msg], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            result = p.communicate()[0]
            self.sendMessage(result)
        elif typeMsg == '[R]':
            index = self.__balancer_read(file_name)
            print "[R][%s] Read %s file from DFS" % (time.strftime("%H:%M:%S"), file_name)
            p = Popen(["python", "fsclient.py", str(SERVERS_PORT[index]), msg], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            result = p.communicate()[0]
            self.sendMessage(result)
   

if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        sys.exit("Using server.py [SERVERS]")
    factory = WebSocketServerFactory("ws://" + ADDRESS + ":" + str(PORT), debug = False)
    SERVERS = int(sys.argv[1])
    factory.protocol = DFS
    listenWS(factory)
    print 'Server starting up on %s port %s' % (ADDRESS, PORT)
    reactor.run()