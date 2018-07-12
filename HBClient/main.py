import sys
import socket
import select
import errno
import base64
from threading import *
from PyQt4 import QtCore, QtGui
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from hongbao import Ui_MainWindow, _translate
import res_rc

class RCDSTool(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(RCDSTool, self).__init__(parent)

        # Set up UI
        self.ui = Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() |
                              QtCore.Qt.WindowSystemMenuHint |
                              QtCore.Qt.WindowMinMaxButtonsHint)
        self.ui.setupUi(self)

        # Server communication
        self.conn = None
        self.client = ''
        self.host = ''
        self.hostpubkey = ''
        self.port = 8888
        self.cipherwr = None

        # Encryption
        self.name = ""
        self.pin = ""
        self.key = RSA.generate(4096)
        self.pubkey = self.key.publickey().exportKey()
        self.cipherrd = PKCS1_OAEP.new(self.key)

        # UI connections
        self.ui.pushButtonConnect.clicked.connect(self.Connect)
        self.ui.pushButtonPrepare.clicked.connect(self.Prepare)
        self.ui.hongbaoimg.linkActivated.connect(self.Collect)
        self.ui.pushButtonLastFive.clicked.connect(self.LastFive)

    # Handle connection to server
    def Connect(self):
        self.name = str(self.ui.lineEditName.text())
        self.pin = str(self.ui.lineEditPIN.text())

        # Find a server
        ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if ip.startswith('192.168.')]
        ips.sort()
        for ip in ips:
            if self.host is '':
                if '192.168.' in ip:
                    baseip = ip.rsplit('.', 1)[0]

                    # Try full subrange
                    for i in range(1, 255):
                        host = str(baseip + '.' + str(i))
                        try:
                            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            conn.settimeout(0.01)
                            conn.connect((host, self.port))
                            conn.settimeout(None)
                            print "Found potential to a server"
                            print host

                            # On successful connection, check that it can communicate
                            conn.send(base64.b64encode(str('? ' + self.pubkey)))
                            print "Sent"
                            data = ""
                            ready = select.select([conn], [], [], 5.0)
                            if ready[0]:
                                data = base64.b64decode(conn.recv(4096))
                            print 'Server sent: ' + data

                            # Did the server send the proper catchphrase and key?
                            if data.startswith('HongBao8888'):
                                hostpubkey = data.split('HongBao8888 ')[1]
                                if len(hostpubkey) == 0:
                                    break

                                # Try sending encrypted login
                                for i in range(5):
                                    cipherwr = PKCS1_OAEP.new(RSA.importKey(hostpubkey))
                                    ciphermsg = str("NAME: " + self.name + " PIN: " + self.pin)
                                    ciphermsg = base64.b64encode(cipherwr.encrypt(ciphermsg))
                                    conn.send(ciphermsg)
                                    ready = select.select([conn], [], [], 5.0)
                                    if ready[0]:
                                        data = base64.b64decode(conn.recv(4096))
                                    print 'Server sent: ' + data

                                    # Server acknowledged, valid
                                    if data == "ACK":
                                        print "Connected to a valid server"
                                        self.client = ip
                                        self.host = host
                                        self.conn = conn
                                        self.hostpubkey = hostpubkey
                                        self.cipherwr = cipherwr
                                        break

                                # If it failed to authenticate, try other addresses
                                if self.host is not '':
                                    break

                        # If it can't connect, don't care
                        except:
                            pass

    def Disconnect(self):
        pass

    def Prepare(self):
        pass

    def Collect(self):
        pass

    def LastFive(self):
        pass

    def UpdateLog(self, msg):
        pass

    def UpdateStatus(self, msg):
        pass

    def SendEncrypted(self, msg):
        pass

    def CheckServer(self):
        pass

    # Event on closing
    def closeEvent(self, event):

        if self.conn is not None:
            self.conn.close()

        # Let the window close
        event.accept() 

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RCDSTool()
    myapp.show()
    sys.exit(app.exec_())
