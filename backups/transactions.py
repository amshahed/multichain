import json
import functions
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets


class TransactionWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(TransactionWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.toggle_combo_box)
        self.wallet_cbox.activated.connect(self.set_wallet)

    def toggle_combo_box(self):
        if self.yes_rbtn.isChecked():
            self.addr_lbl.show()
            self.wallet_cbox.show()
        else:
            self.addr_lbl.hide()
            self.wallet_cbox.hide()

    def fetch_wallets(self):
        self.wallet_cbox.clear()
        self.wallet_cbox.addItem(functions.blank)

        for k, v in self.wallets.items():
            self.wallet_cbox.addItem(v)

    def set_wallet(self):
        addr = self.wallet_cbox.currentText()
        if addr == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Wallet!', 'Choose a valid wallet')
            return
        else:
            for k, v in self.wallets.items():
                if v == addr:
                    addr = k
                    break
            self.fetch_transactions(addr)

    def fetch_transactions(self, addr=False):
        if addr:
            arr = ['multichain-cli', self.chain, 'listaddresstransactions', addr]
        else:
            arr = ['multichain-cli', self.chain, 'listwallettransactions']

        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            transactions = []
            for item in data:
                for key, val in item.items():
                    if key == 'balance' and val['assets']:
                        transactions.append(item)

            self.action_table.setRowCount(len(transactions))
            for i in range(len(transactions)):
                time = datetime.utcfromtimestamp(transactions[i]['blocktime']).strftime('%Y-%m-%d %H:%M:%S')
                self.action_table.setItem(i, 4, QtWidgets.QTableWidgetItem(time))
                if 'issue' in transactions[i]:
                    self.action_table.setItem(i, 0, QtWidgets.QTableWidgetItem('Issue'))
                    self.action_table.setItem(i, 1, QtWidgets.QTableWidgetItem('- - -'))
                    self.action_table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.wallets[transactions[i]['issue']['addresses'][0]]))
                    self.action_table.setItem(i, 3, QtWidgets.QTableWidgetItem(transactions[i]['issue']['name']+': '+str(transactions[i]['issue']['qty'])))
                else:
                    self.action_table.setItem(i, 0, QtWidgets.QTableWidgetItem('Transaction'))
                    if transactions[i]['balance']['assets'][0]['qty'] > 0:
                        self.action_table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.wallets[transactions[i]['addresses'][0]]))
                        self.action_table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.wallets[transactions[i]['myaddresses'][0]]))
                        self.action_table.setItem(i, 3, QtWidgets.QTableWidgetItem(
                            transactions[i]['balance']['assets'][0]['name'] + ': ' + str(
                                transactions[i]['balance']['assets'][0]['qty'])))
                    else:
                        self.action_table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.wallets[transactions[i]['myaddresses'][0]]))
                        self.action_table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.wallets[transactions[i]['addresses'][0]]))
                        self.action_table.setItem(i, 3, QtWidgets.QTableWidgetItem(
                            transactions[i]['balance']['assets'][0]['name'] + ': ' + str(
                                -transactions[i]['balance']['assets'][0]['qty'])))

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(440, 425)
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
        self.addr_lbl = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl.setFont(font)
        self.addr_lbl.setObjectName("addr_lbl")
        self.verticalLayout.addWidget(self.addr_lbl)
        self.wallet_cbox = QtWidgets.QComboBox(self.frame)
        self.wallet_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.wallet_cbox.setObjectName("wallet_cbox")
        self.wallet_cbox.addItem("")
        self.verticalLayout.addWidget(self.wallet_cbox)
        self.action_table = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.action_table.sizePolicy().hasHeightForWidth())
        self.action_table.setSizePolicy(sizePolicy)
        self.action_table.setMinimumSize(QtCore.QSize(315, 30))
        self.action_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.action_table.setLineWidth(1)
        self.action_table.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.action_table.setShowGrid(True)
        self.action_table.setGridStyle(QtCore.Qt.DotLine)
        self.action_table.setRowCount(1)
        self.action_table.setObjectName("action_table")
        self.action_table.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.action_table.setItem(0, 4, item)
        self.action_table.horizontalHeader().setVisible(True)
        self.action_table.horizontalHeader().setCascadingSectionResizes(True)
        self.action_table.horizontalHeader().setDefaultSectionSize(100)
        self.action_table.horizontalHeader().setMinimumSectionSize(100)
        self.action_table.horizontalHeader().setStretchLastSection(False)
        self.action_table.verticalHeader().setCascadingSectionResizes(True)
        self.action_table.verticalHeader().setMinimumSectionSize(30)
        self.action_table.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.action_table)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.action_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.action_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.addr_lbl.hide()
        self.wallet_cbox.hide()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Transactions</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "Do you want to see the transactions of a specific wallet?"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.addr_lbl.setText(_translate("Form", "Choose Wallet"))
        self.wallet_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.action_table.setSortingEnabled(True)
        item = self.action_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.action_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Action"))
        item = self.action_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "From"))
        item = self.action_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Reciver"))
        item = self.action_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Asset"))
        item = self.action_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Time"))
        __sortingEnabled = self.action_table.isSortingEnabled()
        self.action_table.setSortingEnabled(False)
        item = self.action_table.item(0, 0)
        item.setText(_translate("Form", "Transaction"))
        item = self.action_table.item(0, 1)
        item.setText(_translate("Form", "Shahed"))
        item = self.action_table.item(0, 2)
        item.setText(_translate("Form", "Shahed_emergency"))
        item = self.action_table.item(0, 3)
        item.setText(_translate("Form", "Asset1: 200"))
        item = self.action_table.item(0, 4)
        item.setText(_translate("Form", "2018"))
        self.action_table.setSortingEnabled(__sortingEnabled)

