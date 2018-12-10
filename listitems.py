import json
import codecs
import subprocess
import functions
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets


class StreamItemsWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(StreamItemsWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.stream_cbox.activated.connect(self.show_items)
        self.wallet_cbox.activated.connect(self.show_items)
        self.key_ledit.textChanged.connect(self.show_items)

    def fill_streams(self):
        self.stream_cbox.clear()

        arr = ['multichain-cli', self.chain, 'liststreams']
        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            for item in data:
                if item['name'] != 'root':
                    self.stream_cbox.addItem(item['name'])

            self.stream_cbox.setCurrentIndex(0)
            self.show_items()

    def fill_wallets(self):
        self.wallet_cbox.clear()
        self.wallet_cbox.addItem(functions.blank)

        for k, v in self.wallets.items():
            self.wallet_cbox.addItem(v)

    def filter_items(self, items):
        final_items = []
        for item in items:
            publisher = self.wallets[item['publishers'][0]]
            key = item['key']
            data = codecs.decode(item['data'], 'hex').decode('ascii')
            time = datetime.utcfromtimestamp(item['blocktime']).strftime('%Y-%m-%d %H:%M:%S')

            if self.wallet_cbox.currentText() != functions.blank:
                if publisher != self.wallet_cbox.currentText():
                    continue
            if self.key_ledit.text() != '':
                if self.key_ledit.text() not in key:
                    continue

            final_items.append({'publisher':publisher, 'key':key, 'data':data, 'time':time})

        return final_items

    def show_items(self):
        name = self.stream_cbox.currentText()
        arr = ['multichain-cli', self.chain, 'subscribe', name]
        functions.execute(False, arr)

        arr = ['multichain-cli', self.chain, 'liststreamitems', name, 'false', '999999999']
        data = functions.execute(self, arr)
        if data:

            tmp_items = json.loads(data.decode('utf-8'))
            items = self.filter_items(tmp_items)
            self.stream_table.setRowCount(len(items))
            for i in range(len(items)):
                self.stream_table.setItem(i, 0, QtWidgets.QTableWidgetItem(items[i]['publisher']))
                self.stream_table.setItem(i, 1, QtWidgets.QTableWidgetItem(items[i]['key']))
                self.stream_table.setItem(i, 2, QtWidgets.QTableWidgetItem(items[i]['data']))
                self.stream_table.setItem(i, 3, QtWidgets.QTableWidgetItem(items[i]['time']))

            arr = ['multichain-cli', self.chain, 'unsubscribe', name]
            functions.execute(False, arr)

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(472, 488)
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
        self.addr_lbl = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl.setFont(font)
        self.addr_lbl.setObjectName("addr_lbl")
        self.verticalLayout.addWidget(self.addr_lbl)
        self.stream_cbox = QtWidgets.QComboBox(self.frame)
        self.stream_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.stream_cbox.setStyleSheet("")
        self.stream_cbox.setObjectName("stream_cbox")
        self.stream_cbox.addItem("")
        self.verticalLayout.addWidget(self.stream_cbox)
        self.addr_lbl_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl_2.setFont(font)
        self.addr_lbl_2.setObjectName("addr_lbl_2")
        self.verticalLayout.addWidget(self.addr_lbl_2)
        self.wallet_cbox = QtWidgets.QComboBox(self.frame)
        self.wallet_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.wallet_cbox.setObjectName("wallet_cbox")
        self.wallet_cbox.addItem("")
        self.verticalLayout.addWidget(self.wallet_cbox)
        self.addr_lbl_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl_3.setFont(font)
        self.addr_lbl_3.setObjectName("addr_lbl_3")
        self.verticalLayout.addWidget(self.addr_lbl_3)
        self.key_ledit = QtWidgets.QLineEdit(self.frame)
        self.key_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.key_ledit.setObjectName("key_ledit")
        self.verticalLayout.addWidget(self.key_ledit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.stream_table = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stream_table.sizePolicy().hasHeightForWidth())
        self.stream_table.setSizePolicy(sizePolicy)
        self.stream_table.setMinimumSize(QtCore.QSize(315, 30))
        self.stream_table.setStyleSheet("")
        self.stream_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stream_table.setLineWidth(1)
        self.stream_table.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.stream_table.setShowGrid(True)
        self.stream_table.setGridStyle(QtCore.Qt.DotLine)
        self.stream_table.setRowCount(0)
        self.stream_table.setObjectName("stream_table")
        self.stream_table.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.stream_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.stream_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.stream_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.stream_table.setHorizontalHeaderItem(3, item)
        self.stream_table.horizontalHeader().setVisible(True)
        self.stream_table.horizontalHeader().setCascadingSectionResizes(True)
        self.stream_table.horizontalHeader().setDefaultSectionSize(100)
        self.stream_table.horizontalHeader().setMinimumSectionSize(100)
        self.stream_table.horizontalHeader().setStretchLastSection(False)
        self.stream_table.verticalHeader().setCascadingSectionResizes(True)
        self.stream_table.verticalHeader().setMinimumSectionSize(30)
        self.stream_table.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.stream_table)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.stream_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.stream_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Stream Items</span></p></body></html>"))
        self.addr_lbl.setText(_translate("Form", "Choose Stream"))
        self.stream_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.addr_lbl_2.setText(_translate("Form", "Choose Wallet"))
        self.wallet_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.addr_lbl_3.setText(_translate("Form", "Enter key"))
        self.key_ledit.setPlaceholderText(_translate("Form", " "))
        self.stream_table.setSortingEnabled(True)
        item = self.stream_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Publisher"))
        item = self.stream_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Key"))
        item = self.stream_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Data"))
        item = self.stream_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Publish Time"))

