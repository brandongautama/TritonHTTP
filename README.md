# TritonHTTP

A Simple Web Server

# Introduction

TritonHTTP is a simple web server that implements a subset of the HTTP/1.1 protocol.

At a high level, a web server listens for connections on a socket (bound to a specific adderss and port on a host machine). Clients connect to this socket and use the TritonHTTP protocol to retrieve files from the server.  

## To run

	python3 httpd.py [port] [doc_root]

The first argument should be the port number, and the second should be the doc-root (given as either an absolute or relative path, with or without the trailing ‘/’):

Example:

    python3 httpd.py 5001 /data/files