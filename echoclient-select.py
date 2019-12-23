#!/usr/bin/env python

"""
Authors: Vallab Kunigal Badrish & Killian Bailey
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys
import time

port =  65120
size = 1024

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    print("usage: python3 client <hostname>")
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
print("Connected and waiting for the game to start")
bytestream = s.recv(size)
print(bytestream.decode().strip())

end = time.time() + 180

while time.time() < end:
    
    try:
        line = input("%")
    except KeyboardInterrupt:
        break
    s.send(bytes(line, 'ascii'))

bytestream = s.recv(size)
print(bytestream.decode().strip())
s.close()
s.shutdown(socket.SHUT_RDWR)



