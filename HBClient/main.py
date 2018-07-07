from PyQt4 import QtCore, QtGui

class RCDSTool(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(RCDSTool, self).__init__(parent)

    # Set up UI
    self.ui = Ui_MainWindow()
    self.setWindowFlags(self.windowFlags() |
                          QtCore.Qt.WindowSystemMenuHint |
                          QtCore.Qt.WindowMinMaxButtonsHint)
    self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RCDSTool()
    myapp.show()
    sys.exit(app.exec_())
