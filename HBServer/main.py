import socket
from threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888
print 'Binding to: ' + host + ':' + str(port)
serversocket.bind((host, port))

clientlist = []

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            print('Client sent:', self.sock.recv(1024).decode())
            self.sock.send(b'Oi you sent something to me')

serversocket.listen(5)
print ('Server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    clientlist.append(address[0])
    client(clientsocket, address)
