import json
import functions
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
import multichain


class StartWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(StartWindow, self).__init__()
        self.syms = set('!?_@#$%^&*,[]{}<>/\\|\'\"')
        self.tries = 0
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.switch_create_or_connect)
        self.the_button.clicked.connect(self.create_or_connect)

    def switch_create_or_connect(self):
        if self.yes_rbtn.isChecked():
            self.the_label.setText('Enter Name of a New Chain')
            self.the_button.setText('Create Chain')
            self.name_lbl.show()
            self.name_ledit.show()
        else:
            self.the_label.setText('Enter Name of an Existing Chain')
            self.the_button.setText('Connect to Chain')
            self.name_lbl.hide()
            self.name_ledit.hide()

    def save_wallet(self, chain):
        wallet = self.name_ledit.text()
        name = wallet.encode('utf-8').hex()
        arr = ['multichain-cli', chain, 'getaddresses']
        data = functions.execute(self, arr)
        if data:
            addr = json.loads(data.decode('utf-8'))[0]
        arr = ['multichain-cli', chain, 'publish', 'root', addr, name]
        functions.execute(self, arr)
        msg = QtWidgets.QMessageBox.information(self, 'Success!', 'Wallet saved!')

    def create_or_connect(self):
        name = self.the_ledit.text()
        if len(name) < 3 :
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Name!', 'Length of chain name should be at least 3')
            return

        if self.yes_rbtn.isChecked():
            wallet = self.name_ledit.text()
            if len(wallet) < 3 or self.syms & set(wallet):
                msg = QtWidgets.QMessageBox.information(self, 'Invalid name',
                                                        "Length should be at least 3, only alphanumeric, '.' & '-' are valid")
                return

            arr = ['multichain-util', 'create', name]
            p = subprocess.Popen(arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate(timeout=2)
            if err.decode('utf-8') == '':
                msg = QtWidgets.QMessageBox.information(self, 'Success!', 'Chain created! Connecting to chain. . .')
                self.connect_to_chain(name)
            else:
                msg = QtWidgets.QMessageBox.question(self, 'Already exists!',
                                                     name+' alredy exists! Do you want to connect to the chain?',
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if msg == QtWidgets.QMessageBox.Yes:
                    self.connect_to_chain(name)
                else:
                    return
        else:
            self.connect_to_chain(name)

    def connect_to_chain(self, name):
        p = subprocess.Popen(['multichaind', name, '-daemon'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = p.communicate(timeout=2)
        except:
            if self.tries < 3:
                self.tries = self.tries + 1
                self.connect_to_chain(name)
            else:
                msg = QtWidgets.QMessageBox.information(self, 'Error!', 'An unexpected error occurred')
                return
        else:
            err = err.decode('utf-8').split(':')[1].split(' ')[1].lower()
            if err == "couldn't":
                if self.yes_rbtn.isChecked():
                    msg = QtWidgets.QMessageBox.information(self, 'Success!', 'Connection successful! Saving your wallet. . .')
                    self.save_wallet(name)

                mw2.chain = name
                mw.hide()
                mw2.setup()
                mw2.show()
            elif err == 'parameter':
                self.delete_folder(name)
                msg = QtWidgets.QMessageBox.critical(self, 'Invalid Chain!', 'Enter an already existing chain name')

            else:
                msg = QtWidgets.QMessageBox.critical(self, 'Error!', 'An unexpected error occurred')
                return

    def delete_folder(self, name):
        arr = ['whoami']
        username = functions.execute(False, arr).decode('utf-8').split('\n')[0]
        arr = ['rm', '-r', '/home/'+username+'/.multichain/'+name+'/']
        functions.execute(False, arr)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(449, 376)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_rbtn = QtWidgets.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.yes_rbtn.setFont(font)
        self.yes_rbtn.setObjectName("yes_rbtn")
        self.horizontalLayout.addWidget(self.yes_rbtn)
        self.no_rbtn = QtWidgets.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.no_rbtn.setFont(font)
        self.no_rbtn.setChecked(True)
        self.no_rbtn.setObjectName("no_rbtn")
        self.horizontalLayout.addWidget(self.no_rbtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.the_label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.the_label.setFont(font)
        self.the_label.setObjectName("the_label")
        self.verticalLayout.addWidget(self.the_label)
        self.the_ledit = QtWidgets.QLineEdit(self.frame)
        self.the_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.the_ledit.setPlaceholderText("")
        self.the_ledit.setObjectName("the_ledit")
        self.verticalLayout.addWidget(self.the_ledit)
        self.name_lbl = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.name_lbl.setFont(font)
        self.name_lbl.setObjectName("name_lbl")
        self.verticalLayout.addWidget(self.name_lbl)
        self.name_ledit = QtWidgets.QLineEdit(self.frame)
        self.name_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.name_ledit.setPlaceholderText("")
        self.name_ledit.setObjectName("name_ledit")
        self.verticalLayout.addWidget(self.name_ledit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.the_button = QtWidgets.QPushButton(self.frame)
        self.the_button.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.the_button.setFont(font)
        self.the_button.setFlat(False)
        self.the_button.setObjectName("the_button")
        self.verticalLayout.addWidget(self.the_button, 0, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.name_lbl.hide()
        self.name_ledit.hide()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome to Blockchain"))
        self.label_2.setText(_translate("MainWindow", "Do you want to create a new chain?"))
        self.yes_rbtn.setText(_translate("MainWindow", "Yes"))
        self.no_rbtn.setText(_translate("MainWindow", "No"))
        self.the_label.setText(_translate("MainWindow", "Enter Name of Existing Chain"))
        self.name_lbl.setText(_translate("MainWindow", "Enter your name"))
        self.the_button.setText(_translate("MainWindow", "Connect to Chain"))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mw = StartWindow()
    mw2 = multichain.MainWindow()
    mw.show()
    app.exec_()