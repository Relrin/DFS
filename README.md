DFS: a simple distributed file system
===

The simplest distributed file system written in Python 2.7.5
- client.py (client application)
- server.py (server and balancer, which send client file to fileserver or from it to client)
- fileserver.py (server, which working with directory and read/write files)
- fsclient.py (client for fileserver.py)

Requirements
====
- Twisted
- Autobahn.ws
