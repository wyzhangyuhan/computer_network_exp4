# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\AppleZhang_Workshop\Codes\CW\udp_chatroom_ver0.3\pyqt_desktop\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 557)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txtSubmitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.txtSubmitBtn.setGeometry(QtCore.QRect(690, 440, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txtSubmitBtn.setFont(font)
        self.txtSubmitBtn.setStyleSheet("QPushButton{background:#3AF674;border-radius:5px;}QPushButton:hover{background:#50E022;}")
        self.txtSubmitBtn.setObjectName("txtSubmitBtn")
        self.userInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.userInput.setGeometry(QtCore.QRect(280, 440, 401, 71))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.userInput.setFont(font)
        self.userInput.setPlainText("")
        self.userInput.setObjectName("userInput")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(30, 490, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("QPushButton{background:#FF2000;border-radius:5px;}QPushButton:hover{background:#C00000;}")
        self.exitButton.setObjectName("exitButton")
        self.emojiBtn = QtWidgets.QPushButton(self.centralwidget)
        self.emojiBtn.setGeometry(QtCore.QRect(280, 410, 31, 24))
        self.emojiBtn.setObjectName("emojiBtn")
        self.searchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.searchBtn.setGeometry(QtCore.QRect(30, 410, 31, 24))
        self.searchBtn.setObjectName("searchBtn")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 180, 221, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.onlinelistLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.onlinelistLayout.setContentsMargins(0, 0, 0, 0)
        self.onlinelistLayout.setObjectName("onlinelistLayout")
        self.onlineList = QtWidgets.QListView(self.verticalLayoutWidget)
        self.onlineList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.onlineList.setTabKeyNavigation(True)
        self.onlineList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.onlineList.setObjectName("onlineList")
        self.onlinelistLayout.addWidget(self.onlineList)
        self.addressLabel = QtWidgets.QLabel(self.centralwidget)
        self.addressLabel.setGeometry(QtCore.QRect(30, 470, 221, 16))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.addressLabel.setFont(font)
        self.addressLabel.setObjectName("addressLabel")
        self.txtClearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.txtClearBtn.setGeometry(QtCore.QRect(690, 480, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI Light")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txtClearBtn.setFont(font)
        self.txtClearBtn.setStyleSheet("QPushButton{background:#3AF674;border-radius:5px;}QPushButton:hover{background:#50E022;}")
        self.txtClearBtn.setObjectName("txtClearBtn")
        self.emj_bBtn_1 = QtWidgets.QPushButton(self.centralwidget)
        self.emj_bBtn_1.setEnabled(True)
        self.emj_bBtn_1.setGeometry(QtCore.QRect(280, 330, 71, 71))
        self.emj_bBtn_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/Resources/emoji_pics/concerned.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.emj_bBtn_1.setIcon(icon)
        self.emj_bBtn_1.setIconSize(QtCore.QSize(60, 60))
        self.emj_bBtn_1.setObjectName("emj_bBtn_1")
        self.emj_bBtn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.emj_bBtn_2.setEnabled(True)
        self.emj_bBtn_2.setGeometry(QtCore.QRect(350, 330, 71, 71))
        self.emj_bBtn_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/Resources/emoji_pics/facepalm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.emj_bBtn_2.setIcon(icon1)
        self.emj_bBtn_2.setIconSize(QtCore.QSize(60, 60))
        self.emj_bBtn_2.setObjectName("emj_bBtn_2")
        self.emj_bBtn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.emj_bBtn_3.setEnabled(True)
        self.emj_bBtn_3.setGeometry(QtCore.QRect(420, 330, 71, 71))
        self.emj_bBtn_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/Resources/emoji_pics/smart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.emj_bBtn_3.setIcon(icon2)
        self.emj_bBtn_3.setIconSize(QtCore.QSize(60, 60))
        self.emj_bBtn_3.setObjectName("emj_bBtn_3")
        self.emj_bBtn_4 = QtWidgets.QPushButton(self.centralwidget)
        self.emj_bBtn_4.setEnabled(True)
        self.emj_bBtn_4.setGeometry(QtCore.QRect(490, 330, 71, 71))
        self.emj_bBtn_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pic/Resources/emoji_pics/smirk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.emj_bBtn_4.setIcon(icon3)
        self.emj_bBtn_4.setIconSize(QtCore.QSize(60, 60))
        self.emj_bBtn_4.setObjectName("emj_bBtn_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 140, 219, 32))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.searchBox = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBox.setGeometry(QtCore.QRect(30, 440, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.searchBox.setFont(font)
        self.searchBox.setObjectName("searchBox")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 410, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.fileButton = QtWidgets.QPushButton(self.centralwidget)
        self.fileButton.setGeometry(QtCore.QRect(320, 410, 31, 24))
        self.fileButton.setObjectName("fileButton")
        self.tttButton = QtWidgets.QPushButton(self.centralwidget)
        self.tttButton.setGeometry(QtCore.QRect(160, 50, 75, 71))
        self.tttButton.setStyleSheet("QPushButton{background:#A8D4F2;border-radius:5px;}QPushButton:hover{background:#00D2FF;}")
        self.tttButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pic/Resources/ttt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tttButton.setIcon(icon4)
        self.tttButton.setIconSize(QtCore.QSize(72, 72))
        self.tttButton.setObjectName("tttButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 20, 91, 16))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.chatHistory = QtWidgets.QTextBrowser(self.centralwidget)
        self.chatHistory.setGeometry(QtCore.QRect(280, 30, 481, 371))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.chatHistory.setFont(font)
        self.chatHistory.setObjectName("chatHistory")
        self.picButton = QtWidgets.QPushButton(self.centralwidget)
        self.picButton.setGeometry(QtCore.QRect(360, 410, 31, 24))
        self.picButton.setObjectName("picButton")
        self.chatHistory.raise_()
        self.txtSubmitBtn.raise_()
        self.userInput.raise_()
        self.exitButton.raise_()
        self.emojiBtn.raise_()
        self.searchBtn.raise_()
        self.verticalLayoutWidget.raise_()
        self.addressLabel.raise_()
        self.txtClearBtn.raise_()
        self.emj_bBtn_1.raise_()
        self.emj_bBtn_2.raise_()
        self.emj_bBtn_3.raise_()
        self.emj_bBtn_4.raise_()
        self.label.raise_()
        self.searchBox.raise_()
        self.label_2.raise_()
        self.fileButton.raise_()
        self.tttButton.raise_()
        self.label_3.raise_()
        self.picButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 781, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chatingroom"))
        self.txtSubmitBtn.setText(_translate("MainWindow", "Send"))
        self.exitButton.setText(_translate("MainWindow", "Exit room"))
        self.emojiBtn.setText(_translate("MainWindow", "😁"))
        self.searchBtn.setText(_translate("MainWindow", "🍳"))
        self.addressLabel.setText(_translate("MainWindow", "Your address:"))
        self.txtClearBtn.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "Select someone to send message!\n"
"(default: all)"))
        self.label_2.setText(_translate("MainWindow", "Search history..."))
        self.fileButton.setText(_translate("MainWindow", "📑"))
        self.label_3.setText(_translate("MainWindow", "Tic tac toc"))
        self.picButton.setText(_translate("MainWindow", "🖼"))
import client_res_rc
