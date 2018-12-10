import codecs
import functions, multichain
from PyQt5 import QtCore, QtGui, QtWidgets


class NewWalletWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(NewWalletWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.get_btn.clicked.connect(self.get_new_wallet)

    def save_wallet(self, wallet, addr):
        name = functions.get_name(self, self.chain)
        wallet = name + '_' + wallet
        wallet = wallet.encode('utf-8').hex()
        arr = ['multichain-cli', self.chain, 'publish', 'root', addr, wallet]
        out = functions.execute(self, arr)
        if out:
            msg = QtWidgets.QMessageBox.information(self, 'Success!', 'You have a new Wallet!')

    def get_new_wallet(self):
        name = self.wallet_ledit.text()
        if not functions.check_name(self, self.chain, name):
            return

        msg = QtWidgets.QMessageBox.information(self, 'Confirm', 'Are you sure you want to create a new wallet with this name?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            arr = ['multichain-cli', self.chain, 'getnewaddress']
            data = functions.execute(self, arr)
            if data:
                addr = data.decode('utf-8').split('\n')[0]
                self.save_wallet(name, addr)
        else:
            return

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(338, 337)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.addr_lbl = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl.setFont(font)
        self.addr_lbl.setObjectName("addr_lbl")
        self.verticalLayout.addWidget(self.addr_lbl)
        self.wallet_ledit = QtWidgets.QLineEdit(self.frame)
        self.wallet_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.wallet_ledit.setObjectName("wallet_ledit")
        self.verticalLayout.addWidget(self.wallet_ledit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.get_btn = QtWidgets.QPushButton(self.frame)
        self.get_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.get_btn.setFont(font)
        self.get_btn.setObjectName("get_btn")
        self.verticalLayout.addWidget(self.get_btn, 0, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Create New Wallet</span></p></body></html>"))
        self.addr_lbl.setText(_translate("Form", "Name of the Wallet"))
        self.wallet_ledit.setPlaceholderText(_translate("Form", "i.e: emergency, savings"))
        self.get_btn.setText(_translate("Form", "Create Wallet"))

