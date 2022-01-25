from PyQt5.QtCore import Qt
from pastebin import PastebinAPI
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import sys

class Ui_LoadstringR(object):
    def setupUi(self, LoadstringR):
        self.user_dev_key = ""
        self.username = ""
        self.password = ""
        self.api_dev_key = ""
        self.login_url = ""
        x = requests.post(self.login_url, data= {'api_dev_key': self.api_dev_key,'api_user_name': self.username,'api_user_password': self.password})
        self.user_dev_key = str(x.text)

        LoadstringR.setObjectName("LoadstringR")
        LoadstringR.resize(381, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoadstringR.sizePolicy().hasHeightForWidth())
        LoadstringR.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("blob:https://imgur.com/c2e41af1-1d5a-4fe6-b7eb-4f1f68ca3d98"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoadstringR.setWindowIcon(icon)
        self.statusLabel = QtWidgets.QLabel(LoadstringR)
        self.statusLabel.setText("Status : Idle")
        self.statusLabel.move(10,70)
        self.statusLabel.setGeometry(QtCore.QRect(10, 70, 201, 20))
        self.openFile = QtWidgets.QPushButton(LoadstringR)
        self.openFile.setGeometry(QtCore.QRect(10, 270, 91, 21))
        self.openFile.setObjectName("openFile")
        self.scriptBox = QtWidgets.QTextEdit(LoadstringR)
        self.scriptBox.setGeometry(QtCore.QRect(10, 120, 361, 141))
        self.scriptBox.setObjectName("scriptBox")
        self.loadstringBox = QtWidgets.QTextEdit(LoadstringR)
        self.loadstringBox.setGeometry(QtCore.QRect(10, 90, 361, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadstringBox.sizePolicy().hasHeightForWidth())
        self.loadstringBox.setSizePolicy(sizePolicy)
        self.loadstringBox.setAcceptDrops(False)
        self.loadstringBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.loadstringBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.loadstringBox.setTabChangesFocus(False)
        self.loadstringBox.setReadOnly(True)
        self.loadstringBox.setObjectName("loadstringBox")
        self.title = QtWidgets.QLabel(LoadstringR)
        self.title.setGeometry(QtCore.QRect(10, 10, 361, 71))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.clearFile = QtWidgets.QPushButton(LoadstringR)
        self.clearFile.setGeometry(QtCore.QRect(280, 270, 91, 21))
        self.clearFile.setObjectName("clearFile")
        self.convertFile = QtWidgets.QPushButton(LoadstringR)
        self.convertFile.setGeometry(QtCore.QRect(110, 270, 161, 21))
        self.convertFile.setObjectName("convertFile")
        self.openFile.clicked.connect(self.open_file)
        self.clearFile.clicked.connect(self.clearAll)
        self.convertFile.clicked.connect(self.convertToLoadstring)
        self.retranslateUi(LoadstringR)
        QtCore.QMetaObject.connectSlotsByName(LoadstringR)

    def retranslateUi(self, LoadstringR):
        _translate = QtCore.QCoreApplication.translate
        LoadstringR.setWindowTitle(_translate("LoadstringR", "LoadstringR"))
        self.openFile.setText(_translate("LoadstringR", "Open"))
        self.title.setText(_translate("LoadstringR", "LOADSTRINGR"))
        self.clearFile.setText(_translate("LoadstringR", "Clear"))
        self.convertFile.setText(_translate("LoadstringR", "Convert"))

    def open_file(self):
        self.statusLabel.setText("Status : Waiting")
        self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", ".lua files (*.lua)")
        if self.file_name[0] != '':
            with open(self.file_name[0], mode='r') as f:
                contents = f.read()
                print(contents)
                self.scriptBox.setText(contents)
                f.close()
        self.statusLabel.setText("Status : Idle")

    def convertToLoadstring(self):
        self.statusLabel.setText("Status : Converting")
        data = {
        'api_option': 'paste',
        'api_dev_key': self.api_dev_key,
        'api_paste_code':self.scriptBox.toPlainText() + " \n-- Loadstring created using LoadstringR --",
        'api_paste_name':'loadstringr',
        'api_paste_expire_date': '1Y',
        'api_user_key': self.user_dev_key,
        'api_paste_format': 'lua'}

        r = requests.post("https://pastebin.com/api/api_post.php", data=data)

        if r.status_code != 200:
            self.statusLabel.setText("Status : Failed")
        else:
            self.statusLabel.setText("Status : Loadstring Created")
            print("Paste send: ", r.status_code if r.status_code != 200 else "OK/200")
            link = r.text 
            splitLink = link.split("/")
            link = f"https://pastebin.com/raw/{splitLink[3]}"
            self.loadstringBox.setText(f"loadstring(game:HttpGet('{link}'))()")

    def clearAll(self):
        self.scriptBox.setText("")
        self.loadstringBox.setText("")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    LoadstringR = QtWidgets.QWidget()
    ui = Ui_LoadstringR()
    ui.setupUi(LoadstringR)
    LoadstringR.show()
    sys.exit(app.exec_())
