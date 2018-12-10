import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class RevokeWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(RevokeWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.revoke_btn.clicked.connect(self.revoke_permission)

    def fill_addresses(self):
        self.addr_cbox.clear()
        self.addr_cbox.addItem(functions.blank)

        for key, value in self.wallets.items():
            self.addr_cbox.addItem(value)

    def revoke_permission(self):
        addr = self.addr_cbox.currentText()
        if addr == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Choose a valid address')
            return

        for key, val in self.wallets.items():
            if val == addr:
                addr = key
                break

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
            msg = QtWidgets.QMessageBox.critical(self, 'Invalid Permission!', 'Choose permission(s) to revoke')
            return

        msg = QtWidgets.QMessageBox.question(self, 'Confirm',
                                             'Are you sure you want to revoke "' + permissions + '" permission(s) from this wallet?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            arr = ['multichain-cli', self.chain, 'revoke', addr, permissions]
            data = functions.execute(self, arr)
            if data:
                msg = QtWidgets.QMessageBox.information(self, 'Successful!', 'Permissions successfully revoked!')
                self.fill_addresses()
        else:
            return

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(361, 386)
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
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.addr_cbox = QtWidgets.QComboBox(self.frame)
        self.addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.addr_cbox.setObjectName("addr_cbox")
        self.addr_cbox.addItem("")
        self.gridLayout_2.addWidget(self.addr_cbox, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.issue_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.issue_ch.setFont(font)
        self.issue_ch.setObjectName("issue_ch")
        self.gridLayout_2.addWidget(self.issue_ch, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 13, 0, 1, 1)
        self.create_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.create_ch.setFont(font)
        self.create_ch.setObjectName("create_ch")
        self.gridLayout_2.addWidget(self.create_ch, 9, 0, 1, 1)
        self.receive_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.receive_ch.setFont(font)
        self.receive_ch.setObjectName("receive_ch")
        self.gridLayout_2.addWidget(self.receive_ch, 8, 0, 1, 1)
        self.send_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.send_ch.setFont(font)
        self.send_ch.setObjectName("send_ch")
        self.gridLayout_2.addWidget(self.send_ch, 7, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 11, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        self.revoke_btn = QtWidgets.QPushButton(self.frame)
        self.revoke_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.revoke_btn.setFont(font)
        self.revoke_btn.setObjectName("revoke_btn")
        self.gridLayout_2.addWidget(self.revoke_btn, 12, 0, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 4, 0, 1, 1)
        self.connect_ch = QtWidgets.QCheckBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.connect_ch.setFont(font)
        self.connect_ch.setObjectName("connect_ch")
        self.gridLayout_2.addWidget(self.connect_ch, 5, 0, 1, 1)
        self.addr_lbl = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl.setFont(font)
        self.addr_lbl.setObjectName("addr_lbl")
        self.gridLayout_2.addWidget(self.addr_lbl, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.addr_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Revoke Permission</span></p></body></html>"))
        self.issue_ch.setText(_translate("Form", "Issue"))
        self.create_ch.setText(_translate("Form", "Create"))
        self.receive_ch.setText(_translate("Form", "Receive"))
        self.send_ch.setText(_translate("Form", "Send"))
        self.revoke_btn.setText(_translate("Form", "Revoke"))
        self.connect_ch.setText(_translate("Form", "Connect"))
        self.addr_lbl.setText(_translate("Form", "Choose Wallet"))

