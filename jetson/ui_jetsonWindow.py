# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_jetsonWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_JetsonWindow(object):
    def setupUi(self, JetsonWindow):
        JetsonWindow.setObjectName("JetsonWindow")
        JetsonWindow.resize(865, 616)
        self.centralwidget = QtWidgets.QWidget(JetsonWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setObjectName("image_label")
        self.gridLayout.addWidget(self.image_label, 0, 0, 1, 1)
        self.infor_label = QtWidgets.QLabel(self.centralwidget)
        self.infor_label.setGeometry(QtCore.QRect(0, 0, 201, 181))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.infor_label.setFont(font)
        self.infor_label.setAutoFillBackground(True)
        self.infor_label.setScaledContents(True)
        self.infor_label.setAlignment(QtCore.Qt.AlignCenter)
        self.infor_label.setObjectName("infor_label")
        self.image_label.raise_()
        self.infor_label.raise_()
        JetsonWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(JetsonWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 865, 25))
        self.menubar.setObjectName("menubar")
        JetsonWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(JetsonWindow)
        self.statusbar.setObjectName("statusbar")
        JetsonWindow.setStatusBar(self.statusbar)

        self.retranslateUi(JetsonWindow)
        QtCore.QMetaObject.connectSlotsByName(JetsonWindow)

    def retranslateUi(self, JetsonWindow):
        _translate = QtCore.QCoreApplication.translate
        JetsonWindow.setWindowTitle(_translate("JetsonWindow", "MainWindow"))
        self.image_label.setText(_translate("JetsonWindow", "TextLabel"))
        self.infor_label.setText(_translate("JetsonWindow", "<html><head/><body><p><span style=\" color:#ef2929;\">Device 1</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    JetsonWindow = QtWidgets.QMainWindow()
    ui = Ui_JetsonWindow()
    ui.setupUi(JetsonWindow)
    JetsonWindow.show()
    sys.exit(app.exec_())

