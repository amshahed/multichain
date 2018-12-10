import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class GrantWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(GrantWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.switch_old_new)
        self.no_rbtn.toggled.connect(self.switch_old_new)
        self.grant_btn.clicked.connect(self.grant_permission)

    def switch_old_new(self):
        if self.yes_rbtn.isChecked():
            self.addr_cbox.hide()
            self.addr_lbl.hide()
            self.addr_ledit.show()
            self.name_ledit.show()
        else:
            self.addr_cbox.show()
            self.addr_lbl.show()
            self.addr_ledit.hide()
            self.name_ledit.hide()

    def fill_addresses(self):
        self.addr_cbox.clear()
        self.addr_cbox.addItem(functions.blank)

        for key, value in self.wallets.items():
            self.addr_cbox.addItem(value)

    def save_wallet(self, name, addr):
        name = name.encode('utf-8').hex()
        arr = ['multichain-cli', self.chain, 'publish', 'root', addr, name]
        data = functions.execute(self, arr)

    def grant_permission(self):
        permissions = []
        if self.connect_ch.isChecked():
            permissions.append('connect')
        if self.send_ch.isChecked():
            permissions.append('send')
        if self.receive_ch.isChecked():
            permissions.append('receive')
        if self.issue_ch.isChecked():
            permissions.append('issue')
        if self.create_ch.isChecked():
            permissions.append('create')
        permissions = ','.join(permissions)
        if permissions == '':
            msg = QtWidgets.QMessageBox.critical(self, 'Invalid Permission!', 'Choose permission(s) to grant')
            return

        if self.yes_rbtn.isChecked():
            name = self.name_ledit.text()
            if not functions.check_name(self, self.chain, name, False):
                return
            addr = self.addr_ledit.text()
            if len(addr) < 38:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Enter a valid address')
                return
            permissions = permissions + ',send'
        else:
            addr = self.addr_cbox.currentText()
            if addr == functions.blank:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Choose a valid address')
                return

            for key, val in self.wallets.items():
                if val == addr:
                    addr = key
                    break

        msg = QtWidgets.QMessageBox.question(self, 'Confirm',
                                             'Are you sure you want to grant "' + permissions + '" permission(s) to this wallet?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            arr = ['multichain-cli', self.chain, 'grant', addr, permissions]
            data = functions.execute(self, arr)
            if data:
                if self.yes_rbtn.isChecked():
                    self.save_wallet(name, addr)
                    self.addr_ledit.clear()
                msg = QtWidgets.QMessageBox.information(self, 'Successful!', 'Permissions successfully granted!')
                self.wallets = functions.fetch_from_stream(self, self.chain, 'root')
                self.fill_addresses()
        else:
            return


    def setupUi(self):
        self.setObjectName("Form")
        self.setMinimumSize(QtCore.QSize(330, 360))
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self)
        font = QtGui.QFont()
        font.setKerning(True)
        self.frame.setFont(font)
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
        self.addr_ledit = QtWidgets.QLineEdit(self.frame)
        self.addr_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.addr_ledit.setObjectName("addr_ledit")
        self.verticalLayout.addWidget(self.addr_ledit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.name_ledit = QtWidgets.QLineEdit(self.frame)
        self.name_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.name_ledit.setObjectName("name_ledit")
        self.verticalLayout.addWidget(self.name_ledit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.addr_lbl = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl.setFont(font)
        self.addr_lbl.setObjectName("addr_lbl")
        self.verticalLayout.addWidget(self.addr_lbl)
        self.addr_cbox = QtWidgets.QComboBox(self.frame)
        self.addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.addr_cbox.setObjectName("addr_cbox")
        self.addr_cbox.addItem("")
        self.verticalLayout.addWidget(self.addr_cbox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.connect_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.connect_ch.setFont(font)
        self.connect_ch.setObjectName("connect_ch")
        self.verticalLayout.addWidget(self.connect_ch)
        self.issue_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.issue_ch.setFont(font)
        self.issue_ch.setObjectName("issue_ch")
        self.verticalLayout.addWidget(self.issue_ch)
        self.send_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.send_ch.setFont(font)
        self.send_ch.setObjectName("send_ch")
        self.verticalLayout.addWidget(self.send_ch)
        self.receive_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.receive_ch.setFont(font)
        self.receive_ch.setObjectName("receive_ch")
        self.verticalLayout.addWidget(self.receive_ch)
        self.create_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.create_ch.setFont(font)
        self.create_ch.setObjectName("create_ch")
        self.verticalLayout.addWidget(self.create_ch)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.grant_btn = QtWidgets.QPushButton(self.frame)
        self.grant_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.grant_btn.setFont(font)
        self.grant_btn.setObjectName("grant_btn")
        self.verticalLayout.addWidget(self.grant_btn, 0, QtCore.Qt.AlignHCenter)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.addr_ledit.hide()
        self.name_ledit.hide()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Grant Permission</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "Do you want to give a new wallet address?"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.addr_ledit.setPlaceholderText(_translate("Form", "  Enter New Address"))
        self.name_ledit.setPlaceholderText(_translate("Form", "  Enter Name of the New Member"))
        self.addr_lbl.setText(_translate("Form", "Choose Wallet"))
        self.addr_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.connect_ch.setText(_translate("Form", "Connect"))
        self.issue_ch.setText(_translate("Form", "Issue"))
        self.send_ch.setText(_translate("Form", "Send"))
        self.receive_ch.setText(_translate("Form", "Receive"))
        self.create_ch.setText(_translate("Form", "Create"))
        self.grant_btn.setText(_translate("Form", "Grant"))

