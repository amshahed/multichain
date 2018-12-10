import json
import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class BalanceWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(BalanceWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.toggle_combo_box)
        self.no_rbtn.toggled.connect(lambda: self.show_balance())
        self.addr_cbox.activated.connect(self.show_address_balance)

    def toggle_combo_box(self):
        if self.yes_rbtn.isChecked():
            self.addr_lbl.show()
            self.addr_cbox.show()
        else:
            self.addr_lbl.hide()
            self.addr_cbox.hide()

    def fill_addresses(self):
        self.addr_cbox.clear()
        self.addr_cbox.addItem(functions.blank)

        for k, v in self.addr.items():
            self.addr_cbox.addItem(v)

    def show_address_balance(self):
        if self.yes_rbtn.isChecked():
            addr = self.addr_cbox.currentText()
            if addr == functions.blank:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Address!', 'Choose a valid address')
                return
            else:
                for k, v in self.addr.items():
                    if v == addr:
                        addr = k
                        break
                self.show_balance(addr)

    def show_balance(self, addr=False):
        if addr:
            arr = ['multichain-cli', self.chain, 'getaddressbalances', addr]
        else:
            arr = ['multichain-cli', self.chain, 'gettotalbalances']

        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            self.addr_table.setRowCount(len(data))
            for i in range(len(data)):
                self.addr_table.setItem(i, 0, QtWidgets.QTableWidgetItem(data[i]['name']))
                self.addr_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(data[i]['qty'])))
        else:
            return False

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(406, 404)
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
        self.addr_cbox = QtWidgets.QComboBox(self.frame)
        self.addr_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.addr_cbox.setObjectName("addr_cbox")
        self.addr_cbox.addItem("")
        self.verticalLayout.addWidget(self.addr_cbox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.addr_table = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addr_table.sizePolicy().hasHeightForWidth())
        self.addr_table.setSizePolicy(sizePolicy)
        self.addr_table.setMinimumSize(QtCore.QSize(315, 30))
        self.addr_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.addr_table.setLineWidth(1)
        self.addr_table.setShowGrid(True)
        self.addr_table.setGridStyle(QtCore.Qt.DotLine)
        self.addr_table.setRowCount(1)
        self.addr_table.setObjectName("addr_table")
        self.addr_table.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.addr_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.addr_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.addr_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.addr_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.addr_table.setItem(0, 1, item)
        self.addr_table.horizontalHeader().setVisible(True)
        self.addr_table.horizontalHeader().setCascadingSectionResizes(True)
        self.addr_table.horizontalHeader().setDefaultSectionSize(100)
        self.addr_table.horizontalHeader().setMinimumSectionSize(100)
        self.addr_table.horizontalHeader().setStretchLastSection(True)
        self.addr_table.verticalHeader().setCascadingSectionResizes(True)
        self.addr_table.verticalHeader().setMinimumSectionSize(30)
        self.addr_table.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.addr_table)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.addr_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.addr_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.addr_lbl.hide()
        self.addr_cbox.hide()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Asset Balance</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "Do you want to see the balance of a specific wallet?"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.addr_lbl.setText(_translate("Form", "Choose Wallet"))
        self.addr_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.addr_table.setSortingEnabled(True)
        item = self.addr_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.addr_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Asset"))
        item = self.addr_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Balance"))
        __sortingEnabled = self.addr_table.isSortingEnabled()
        self.addr_table.setSortingEnabled(False)
        item = self.addr_table.item(0, 0)
        item.setText(_translate("Form", "asset1"))
        item = self.addr_table.item(0, 1)
        item.setText(_translate("Form", "700"))
        self.addr_table.setSortingEnabled(__sortingEnabled)

