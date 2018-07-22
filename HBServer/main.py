import os
import errno
import socket
import select
import base64
from threading import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

key = None
pubkey = None
rsa = os.path.join(os.getcwd(), "hbrsa")

if os.path.exists(rsa):
    print "Reading RSA key..."
    try:
        with open(rsa, 'rb') as rsaf:
            key = RSA.importKey(rsaf.readlines())
            pubkey = key.publickey().exportKey()
    except:
        print "Failed reading, generating new RSA key..."
        key = RSA.generate(4096)
        with open(rsa, 'wb') as rsaf:
            rsaf.write(key.exportKey())
else:
    print "No RSA key, generating..."
    key = RSA.generate(4096)
    with open(rsa, 'wb') as rsaf:
        rsaf.write(key.exportKey())


cipherrd = PKCS1_OAEP.new(key)

print "RSA keys loaded."

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

# Client communication stored in threads
class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.cipherwr = None
        self.pubkey = ""
        self.name = ""
        self.pin = ""
        self.start()

    def run(self):
        while 1:
            try:
                data = ""
                ready = select.select([self.sock], [], [], 0.01)
                if ready[0]:
                    data = base64.b64decode(self.sock.recv(4096))

                # Establish a new connection
                if data is not "" and self.cipherwr == None:
                    print self.addr[0] + ' sent: ' + data
                    if data.startswith("?"):
                        self.pubkey = data.split("? ")[1]
                        self.cipherwr = PKCS1_OAEP.new(RSA.importKey(self.pubkey))
                        self.sock.send(base64.b64encode(str('HongBao8888 ' + pubkey)))
                        print "Sent auth msg and key to " + self.addr[0]
                    else:
                        raise socket.error(errno.WSAECONNRESET, "Did not catch on connection")

                # Handle standard requests
                elif data is not "" and self.cipherwr is not None:
                    print self.addr[0] + ' sent: ' + data

                    # Client identification
                    if data.startswith('HBSEND'):
                        print "Received new set of hongbaos"
                    elif data.startswith('HBOPEN'):
                        print "Received request for hb"
                    elif data.startswith('LASTFIVE'):
                        print "Received request for last five hb results"
                    else:
                        try:
                            data = cipherrd.decrypt(data)
                            if data.startswith("NAME:"):
                                self.name = data.split("NAME: ")[1].split(" PIN:")[0]
                                self.pin = data.split("PIN: ")[1]
                                print self.name + " " + self.pin
                                self.sock.send(base64.b64encode('ACK'))
                        except:
                            raise socket.error(errno.WSAECONNRESET, "Did not catch in use")

            # Likely broken connection from client side, close
            except socket.error as error:
                if error.errno == errno.WSAECONNRESET:
                    self.sock.close()
                    print self.addr[0] + " disconnected"
                    break
                else:
                    raise

serversocket.listen(5)
print ('Server started and listening')

canquit = False
while 1:
    # Are there any pending connections?
    ready = select.select([serversocket], [], [], 0.01)
    if ready[0]:

        # Set up new clients waiting
        clientsocket, address = serversocket.accept()
        clientsocket.setblocking(0)
        clientlist.append(client(clientsocket, address))
        print "Client connected: " + address[0]
        canquit = True

    # Have any clients disconnected?
    for client in clientlist:
        if not client.isAlive():
            idx = clientlist.index(client)
            clientlist[idx:idx+1] = []
            print "Removed client "  + address[0] + " from list"

    # Are there any clients?
    if not clientlist and canquit:
        break


