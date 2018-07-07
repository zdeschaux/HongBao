# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hongbao.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 585)
        MainWindow.setMinimumSize(QtCore.QSize(640, 585))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hongbaoimg = QtGui.QLabel(self.centralwidget)
        self.hongbaoimg.setText(_fromUtf8(""))
        self.hongbaoimg.setPixmap(QtGui.QPixmap(_fromUtf8(":/hongbao/hongbao.png")))
        self.hongbaoimg.setObjectName(_fromUtf8("hongbaoimg"))
        self.gridLayout.addWidget(self.hongbaoimg, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEditFunds = QtGui.QLineEdit(self.centralwidget)
        self.lineEditFunds.setAcceptDrops(False)
        self.lineEditFunds.setReadOnly(True)
        self.lineEditFunds.setObjectName(_fromUtf8("lineEditFunds"))
        self.verticalLayout.addWidget(self.lineEditFunds)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.doubleSpinBoxTotal = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBoxTotal.setObjectName(_fromUtf8("doubleSpinBoxTotal"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxTotal)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.spinBoxQuantity = QtGui.QSpinBox(self.centralwidget)
        self.spinBoxQuantity.setObjectName(_fromUtf8("spinBoxQuantity"))
        self.horizontalLayout_2.addWidget(self.spinBoxQuantity)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.lineEditMessage = QtGui.QLineEdit(self.centralwidget)
        self.lineEditMessage.setObjectName(_fromUtf8("lineEditMessage"))
        self.verticalLayout.addWidget(self.lineEditMessage)
        self.pushButtonPrepare = QtGui.QPushButton(self.centralwidget)
        self.pushButtonPrepare.setObjectName(_fromUtf8("pushButtonPrepare"))
        self.verticalLayout.addWidget(self.pushButtonPrepare)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.listWidgetRanks = QtGui.QListWidget(self.centralwidget)
        self.listWidgetRanks.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.listWidgetRanks.setObjectName(_fromUtf8("listWidgetRanks"))
        self.verticalLayout.addWidget(self.listWidgetRanks)
        self.pushButtonLastFive = QtGui.QPushButton(self.centralwidget)
        self.pushButtonLastFive.setObjectName(_fromUtf8("pushButtonLastFive"))
        self.verticalLayout.addWidget(self.pushButtonLastFive)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_3.addWidget(self.label_7)
        self.lineEditName = QtGui.QLineEdit(self.centralwidget)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_3.addWidget(self.lineEditName)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lineEditPIN = QtGui.QLineEdit(self.centralwidget)
        self.lineEditPIN.setObjectName(_fromUtf8("lineEditPIN"))
        self.horizontalLayout_3.addWidget(self.lineEditPIN)
        self.pushButtonConnect = QtGui.QPushButton(self.centralwidget)
        self.pushButtonConnect.setObjectName(_fromUtf8("pushButtonConnect"))
        self.horizontalLayout_3.addWidget(self.pushButtonConnect)
        self.horizontalLayout_3.setStretch(1, 5)
        self.horizontalLayout_3.setStretch(3, 1)
        self.horizontalLayout_3.setStretch(4, 2)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionConnect = QtGui.QAction(MainWindow)
        self.actionConnect.setObjectName(_fromUtf8("actionConnect"))
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Hong Bao", None))
        self.label.setText(_translate("MainWindow", "Available Funds", None))
        self.label_3.setText(_translate("MainWindow", "Total", None))
        self.label_4.setText(_translate("MainWindow", "Quantity", None))
        self.label_5.setText(_translate("MainWindow", "Message", None))
        self.pushButtonPrepare.setText(_translate("MainWindow", "Prepare Red Packet", None))
        self.label_2.setText(_translate("MainWindow", "Players and Rank", None))
        self.listWidgetRanks.setSortingEnabled(True)
        self.pushButtonLastFive.setText(_translate("MainWindow", "Last Five (5) Results", None))
        self.label_7.setText(_translate("MainWindow", "Name", None))
        self.label_6.setText(_translate("MainWindow", "PIN", None))
        self.pushButtonConnect.setText(_translate("MainWindow", "Connect", None))
        self.actionConnect.setText(_translate("MainWindow", "Connect...", None))
        self.actionSettings.setText(_translate("MainWindow", "Settings", None))

import res_rc
