import json
import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class IssueMoreWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(IssueMoreWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.toggle_combo_box)
        self.asset_cbox.activated.connect(self.set_current_quantity)
        self.issue_btn.clicked.connect(self.issue_more_asset)

    def toggle_combo_box(self):
        if self.yes_rbtn.isChecked():
            self.label_5.show()
            self.addr_cbox.show()
        else:
            self.label_5.hide()
            self.addr_cbox.hide()

    def fill_addresses(self):
        self.addr_cbox.clear()
        self.to_addr_cbox.clear()
        self.addr_cbox.addItem(functions.blank)
        self.to_addr_cbox.addItem(functions.blank)

        for key, val in self.addr.items():
            self.addr_cbox.addItem(val)

        for key, val in self.to_addr.items():
            self.to_addr_cbox.addItem(val)

        self.fill_assets()

    def fill_assets(self):
        self.asset_cbox.clear()
        self.asset_cbox.addItem(functions.blank)

        arr = ['multichain-cli', self.chain, 'listassets']
        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            for asset in data:
                self.asset_cbox.addItem(asset['name']+',current quantity: '+str(asset['issueqty'])+',smallest unit: '+str(asset['units']))

    def set_current_quantity(self):
        asset = self.asset_cbox.currentText()
        if not asset == functions.blank:
            qty = asset.split(',')[1].split(':')[1]
            asset = asset.split(',')[0]
            self.qty_ledit.setPlaceholderText('Current quantity of "'+asset+'":'+qty)

    def issue_more_asset(self):
        to_addr = self.to_addr_cbox.currentText()
        if to_addr == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Wallet!', 'Choose a valid receiving wallet')
            return
        else:
            for key, val in self.to_addr.items():
                if val == to_addr:
                    to_addr = key
                    break

        if self.yes_rbtn.isChecked():
            addr = self.addr_cbox.currentText()
            if addr == functions.blank:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Wallet!', 'Choose a valid issuing Wallet')
                return
            else:
                for key, val in self.addr.items():
                    if val == addr:
                        addr = key
                        break

        asset = self.asset_cbox.currentText().split(',')[0]
        if asset == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Asset!', 'Choose a valid asset')
            return

        qty = self.qty_ledit.text()

        if qty == '':
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Quantity!', 'Enter valid quantity')
            return

        msg = QtWidgets.QMessageBox.question(self, 'Confirm', 'Do you want to issue '+qty+' amount more of "'+asset+'" to this wallet?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            if self.yes_rbtn.isChecked():
                arr = ['multichain-cli', self.chain, 'issuemorefrom', addr, to_addr, asset, qty]
            else:
                arr = ['multichain-cli', self.chain, 'issuemore', to_addr, asset, qty]

            data = functions.execute(self, arr)
            if data:
                msg = QtWidgets.QMessageBox.information(self, 'Successful!', 'Issuing successful')
                self.fill_addresses()
                self.fill_assets()
                self.qty_ledit.clear()
        else:
            return

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(365, 489)
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
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_6 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
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
        self.label_5 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_5.hide()
        self.verticalLayout.addWidget(self.label_5)
        self.addr_cbox = QtWidgets.QComboBox(self.frame)
        self.addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.addr_cbox.setObjectName("addr_cbox")
        self.addr_cbox.hide()
        self.verticalLayout.addWidget(self.addr_cbox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.label_7 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.to_addr_cbox = QtWidgets.QComboBox(self.frame)
        self.to_addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.to_addr_cbox.setObjectName("to_addr_cbox")
        self.verticalLayout.addWidget(self.to_addr_cbox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
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
        self.qty_ledit.setMinimumSize(QtCore.QSize(200, 30))
        self.qty_ledit.setPlaceholderText("")
        self.qty_ledit.setObjectName("qty_ledit")
        self.horizontalLayout_2.addWidget(self.qty_ledit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.issue_btn = QtWidgets.QPushButton(self.frame)
        self.issue_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.issue_btn.setFont(font)
        self.issue_btn.setObjectName("issue_btn")
        self.verticalLayout.addWidget(self.issue_btn, 0, QtCore.Qt.AlignHCenter)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Issue More of an Existing Asset</span></p></body></html>"))
        self.label_6.setText(_translate("Form", "Do you want to issue with a specific wallet?"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.label_5.setText(_translate("Form", "Issuing Address"))
        self.label_7.setText(_translate("Form", "Receiving Address"))
        self.label_2.setText(_translate("Form", "Choose Asset"))
        self.label_3.setText(_translate("Form", "Quantity"))
        self.issue_btn.setText(_translate("Form", "Issue"))

