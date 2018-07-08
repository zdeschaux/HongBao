import sys
import socket
from threading import *
from PyQt4 import QtCore, QtGui

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

        self.conn = None
        self.client = ''
        self.host = ''
        self.port = 8888

        self.ui.pushButtonConnect.clicked.connect(self.Connect)
        self.ui.pushButtonPrepare.clicked.connect(self.Prepare)
        self.ui.hongbaoimg.linkActivated.connect(self.Collect)
        self.ui.pushButtonLastFive.clicked.connect(self.LastFive)

    def Connect(self):
        ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if ip.startswith('192.168.')]
        ips.sort()
        for ip in ips:
            if self.host is '':
                if '192.168.' in ip:
                    baseip = ip.rsplit('.', 1)[0]
                    for i in range(1, 256):
                        host = str(baseip + '.' + str(i))
                        try:
                            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            conn.settimeout(0.01)
                            conn.connect((host, self.port))
                            self.host = host
                            self.conn = conn
                            self.conn.send('e'.encode())
                            print "Connected"
                            print host
                            break
                        except:
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
