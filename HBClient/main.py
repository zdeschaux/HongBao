import sys
import socket
import select
import errno
import base64
from PyQt4 import QtCore, QtGui
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from hongbao import Ui_MainWindow, _translate
import res_rc

def clickable(widget):
 
     class Filter(QtCore.QObject):
     
         clicked = QtCore.pyqtSignal()
         
         def eventFilter(self, obj, event):
         
             if obj == widget:
                 if event.type() == QtCore.QEvent.MouseButtonRelease:
                     if obj.rect().contains(event.pos()):
                         self.clicked.emit()
                         # The developer can opt for .emit(obj) to get the object within the slot.
                         return True
             
             return False
     
     filter = Filter(widget)
     widget.installEventFilter(filter)
     return filter.clicked

class ServerConn(QtCore.QThread):

    hbin = QtCore.pyqtSignal()
    hbres = QtCore.pyqtSignal(float)
    hblog = QtCore.pyqtSignal(str)
    hblast = QtCore.pyqtSignal(str)

    def __init__(self, conn, sigdict):
        QtCore.QThread.__init__(self, parent=app)
        
        self.hbout = sigdict['hbout']
        self.hbget = sigdict['hbget']
        self.lastfiveget = sigdict['lastfiveget']
        self.closeserverconn = sigdict['closeserverconn']

        self.hbout.connect(self.sendhb)
        self.hbget.connect(self.gethb)
        self.lastfiveget.connect(self.lastfive)
        self.closeserverconn.connect(self.closeconn)

        self.conn = conn
        self.start()

    def run(self):  
        while 1:
            try:
                data = ""
                ready = select.select([self.conn], [], [], 0.01)
                if ready[0]:
                    data = base64.b64decode(self.conn.recv(4096))

                # Establish a new connection
                if data is not "":
                    print self.addr[0] + ' sent: ' + data
                    if data.startswith("NEWHB"):
                        print "Received new Hong Bao!"
                        self.hbin.emit()
                    elif data.startswith("HBGET"):
                        print "Received results of Hong bao!"
                        self.hbres.emit(float(data.split("HBGET ")[1]))
                    elif data.startswith("NEWLOG"):
                        print "Received new log!"
                        self.hblog.emit(data.split("NEWLOG ")[1])
                    elif data.startswith("LASTFIVE"):
                        print "Received last five results!"
                        self.hblast.emit(data.split("LASTFIVE ")[1])
                    elif data.startswith("ACK"):
                        pass
                    else:
                        raise socket.error(errno.WSAECONNRESET, "Did not catch on connection")

            # Likely broken connection from client side, close
            except socket.error as error:
                if error.errno == errno.WSAECONNRESET:
                    self.conn.close()
                    print self.addr[0] + " disconnected"
                    break
                else:
                    raise

    def sendhb(self, total, qty, msg):
        self.conn.send(base64.b64encode(str("HBSEND TOTAL: "+str(total)+" QTY: "+str(qty)+" MSG: "+msg)))

    def gethb(self):
        self.conn.send(base64.b64encode(str("HBOPEN")))

    def lastfive(self):
        self.conn.send(base64.b64encode(str("LASTFIVE")))

    def closeconn(self):
        self.conn.shutdown(socket.SHUT_RDWR)

class RCDSTool(QtGui.QMainWindow):

    hbout = QtCore.pyqtSignal(float, float, str)
    hbget = QtCore.pyqtSignal()
    lastfiveget = QtCore.pyqtSignal()
    closeserverconn = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(RCDSTool, self).__init__(parent)

        # Set up UI
        self.ui = Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() |
                              QtCore.Qt.WindowSystemMenuHint |
                              QtCore.Qt.WindowMinMaxButtonsHint)
        self.ui.setupUi(self)

        # Server communication
        self.connthread = None
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
        clickable(self.ui.hongbaoimg).connect(self.Collect)
        self.ui.pushButtonLastFive.clicked.connect(self.LastFive)

        #self.ui.pushButtonConnect.setDisabled(True)
        #self.ui.pushButtonPrepare.setDisabled(True)
        #self.ui.pushButtonLastFive.setDisabled(True)

    # Handle connection to server
    def Connect(self):
        self.name = str(self.ui.lineEditName.text())
        self.pin = str(self.ui.lineEditPIN.text())

        # Find a server
        ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if ip.startswith('192.168.')]
        ips.sort()
        ips = [ip for ip in ips if '192.168.' in ip]
        for ip in ips:
            if self.host is '':
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

                        if self.DeepConnect(conn, ip, host):
                            return
                        
                    # If it can't connect, don't care
                    except:
                        pass
            else:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.settimeout(0.01)
                conn.connect((host, self.port))
                conn.settimeout(None)
                print host
                if not self.DeepConnect(conn):
                    self.host = ''
                    self.Connect()

    def DeepConnect(self, conn, ip, host):
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
                return False

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
                try:
                    if data == "ACK":
                        self.client = ip
                        self.host = host
                        self.hostpubkey = hostpubkey
                        self.cipherwr = cipherwr
                        sigdict =   {
                                    'hbout':self.hbout,
                                    'hbget':self.hbget,
                                    'lastfiveget':self.lastfiveget,
                                    'closeserverconn':self.closeserverconn
                                    }
                        self.connthread = ServerConn(conn, sigdict)
                        print "Connected to a valid server"
                        return True
                except Exception as e:
                    print e
        return False

    def Disconnect(self):
        self.closeserverconn.emit()

    def Prepare(self):
        self.hbout.emit(0.0, 0.0, "A message")

    def Collect(self):
        self.hbget.emit()

    def LastFive(self):
        self.lastfiveget.emit()

    def UpdateLog(self, msg):
        pass

    def UpdateStatus(self, msg):
        pass

    def CloseEvent(self, event):
        if self.connthread != None:
            print "Closing open connection"
            self.emit(QtCore.SIGNAL("closeserverconn"))

        event.accept()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RCDSTool()
    myapp.show()
    sys.exit(app.exec_())
