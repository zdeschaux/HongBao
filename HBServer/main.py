import errno
import socket
import select
from threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if ip.startswith('192.168.')]
ips.sort()
if ips:
    host = ips[0]
else:
    host = '127.0.0.1'
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
            try:
                ready = select.select([self.sock], [], [], 0.01)
                if ready[0]:
                    data = self.sock.recv(4096).decode()
                if data is not "":
                    print('Client sent:', data)
                data = ""
                self.sock.send(b'Oi you sent something to me')
            except socket.error as error:
                if error.errno == errno.WSAECONNRESET:
                    self.sock.close()
                    print "Client disconnected: " + address[0]
                    break
                else:
                    raise

serversocket.listen(5)
print ('Server started and listening')
canquit = False
while 1:
    ready = select.select([serversocket], [], [], 0.01)
    if ready[0]:
        clientsocket, address = serversocket.accept()
        clientsocket.setblocking(0)
        clientlist.append(client(clientsocket, address))
        print "Client connected: " + address[0]
        canquit = True
    for client in clientlist:
        if not client.isAlive():
            idx = clientlist.index(client)
            clientlist[idx:idx+1] = []
            print "Removed client "  + address[0] + " from list"
    if not clientlist and canquit:
        break


