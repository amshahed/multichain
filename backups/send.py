import json
import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class SendWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(SendWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.toggle_combo_box)
        self.from_addr_cbox.activated.connect(self.fill_assets)
        self.asset_cbox.activated.connect(self.set_maximum_quantity)
        self.send_btn.clicked.connect(self.send_asset)

    def toggle_combo_box(self):
        if self.yes_rbtn.isChecked():
            self.label_6.show()
            self.from_addr_cbox.show()
        else:
            self.label_6.hide()
            self.from_addr_cbox.hide()
            self.fill_assets()

    def fill_addresses(self):
        self.addr_cbox.clear()
        self.from_addr_cbox.clear()
        self.addr_cbox.addItem(functions.blank)
        self.from_addr_cbox.addItem(functions.blank)

        for key, value in self.addr.items():
            self.addr_cbox.addItem(value)

        for key, val in self.from_addr.items():
            self.from_addr_cbox.addItem(val)

    def fill_assets(self):
        self.asset_cbox.clear()
        self.asset_cbox.addItem(functions.blank)

        if self.yes_rbtn.isChecked():
            from_addr = self.from_addr_cbox.currentText()
            if from_addr == functions.blank:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Choose a valid sending address')
                return
            else:
                for k, v in self.from_addr.items():
                    if v == from_addr:
                        from_addr = k
                        break
                arr = ['multichain-cli', self.chain, 'getaddressbalances', from_addr]
        else:
            arr = ['multichain-cli', self.chain, 'gettotalbalances']

        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            for asset in data:
                self.asset_cbox.addItem(asset['name']+', quantity:'+str(asset['qty']))

    def set_maximum_quantity(self):
        asset = self.asset_cbox.currentText()
        if not asset == functions.blank:
            qty = asset.split(':')[1]
            self.qty_ledit.setPlaceholderText('You can send upto '+qty)

    def send_asset(self):
        addr = self.addr_cbox.currentText()
        if addr == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Choose a valid receiving address')
            return
        else:
            for k, v in self.addr.items():
                if v == addr:
                    addr = k
                    break

        if self.yes_rbtn.isChecked():
            from_addr = self.from_addr_cbox.currentText()
            if from_addr == functions.blank:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Choose a valid sending address')
                return
            else:
                for k, v in self.from_addr.items():
                    if v == from_addr:
                        from_addr = k
                        break

        asset = self.asset_cbox.currentText()
        if asset == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Asset!', 'Choose a valid asset')
            return
        asset = asset.split(',')[0]

        qty = self.qty_ledit.text()
        if qty == '':
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Quantity!', 'Enter quantity')
            return

        if self.yes_rbtn.isChecked():
            arr = ['multichain-cli', self.chain, 'sendassetfrom', from_addr, addr, asset, qty]
        else:
            arr = ['multichain-cli', self.chain, 'sendasset', addr, asset, qty]

        msg = QtWidgets.QMessageBox.question(self, 'Confirm', 'Do you want to send '+qty+' amount of "'+asset+'" to this wallet?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            data = functions.execute(self, arr)
            if data:
                msg = QtWidgets.QMessageBox.information(self, 'Successful!', 'Transaction successful!')
                self.fill_addresses()
                self.fill_assets()
                self.qty_ledit.clear()
            else:
                return
        else:
            return

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(459, 487)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_rbtn = QtWidgets.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.yes_rbtn.setFont(font)
        self.yes_rbtn.setChecked(True)
        self.yes_rbtn.setObjectName("yes_rbtn")
        self.horizontalLayout.addWidget(self.yes_rbtn)
        self.no_rbtn = QtWidgets.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.no_rbtn.setFont(font)
        self.no_rbtn.setChecked(False)
        self.no_rbtn.setObjectName("no_rbtn")
        self.horizontalLayout.addWidget(self.no_rbtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_6 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.from_addr_cbox = QtWidgets.QComboBox(self.frame)
        self.from_addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.from_addr_cbox.setObjectName("from_addr_cbox")
        self.verticalLayout.addWidget(self.from_addr_cbox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.addr_cbox = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addr_cbox.sizePolicy().hasHeightForWidth())
        self.addr_cbox.setSizePolicy(sizePolicy)
        self.addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.addr_cbox.setObjectName("addr_cbox")
        self.verticalLayout.addWidget(self.addr_cbox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.label_7 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.asset_cbox = QtWidgets.QComboBox(self.frame)
        self.asset_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.asset_cbox.setObjectName("asset_cbox")
        self.verticalLayout.addWidget(self.asset_cbox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.qty_ledit = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qty_ledit.sizePolicy().hasHeightForWidth())
        self.qty_ledit.setSizePolicy(sizePolicy)
        self.qty_ledit.setMinimumSize(QtCore.QSize(200, 30))
        self.qty_ledit.setObjectName("qty_ledit")
        self.horizontalLayout_2.addWidget(self.qty_ledit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.send_btn = QtWidgets.QPushButton(self.frame)
        self.send_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.send_btn.setFont(font)
        self.send_btn.setObjectName("send_btn")
        self.verticalLayout.addWidget(self.send_btn, 0, QtCore.Qt.AlignHCenter)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Send Asset</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Do you want to use a specific wallet?</span></p></body></html>"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.label_6.setText(_translate("Form", "Choose Sending Address"))
        self.label_5.setText(_translate("Form", "Choose Receiving Address"))
        self.label_7.setText(_translate("Form", "Choose Asset to Send"))
        self.label_3.setText(_translate("Form", "Quantity"))
        self.send_btn.setText(_translate("Form", "Send"))

