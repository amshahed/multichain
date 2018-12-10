import json
import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class PublishWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(PublishWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.toggle_combo_box)
        self.publish_btn.clicked.connect(self.publish_to_stream)

    def toggle_combo_box(self):
        if self.yes_rbtn.isChecked():
            self.addr_lbl.show()
            self.addr_cbox.show()
        else:
            self.addr_lbl.hide()
            self.addr_cbox.hide()

    def fill_wallets(self):
        self.addr_cbox.clear()
        self.addr_cbox.addItem(functions.blank)

        for k, v in self.wallets.items():
            self.addr_cbox.addItem(v)

    def fill_streams(self):
        self.stream_cbox.clear()
        self.stream_cbox.addItem(functions.blank)

        arr = ['multichain-cli', self.chain, 'liststreams']
        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            for item in data:
                if item['name'] != 'root':
                    self.stream_cbox.addItem(item['name'])

    def publish_to_stream(self):
        name = self.stream_cbox.currentText()
        if name == functions.blank:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Stream!', 'Choose a valid stream')
            return

        key = self.key_ledit.text()
        data = self.data_ledit.text()
        if len(key) < 3 or len(data) < 3:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Key/Data!', 'Length of key and data should be at least 3')
            return
        else:
            data = data.encode('utf-8').hex()

        if self.yes_rbtn.isChecked():
            addr = self.addr_cbox.currentText()
            if addr == functions.blank:
                msg = QtWidgets.QMessageBox.information(self, 'Invalid Wallet!', 'Choose a valid wallet')
                return
            else:
                for k, v in self.wallets.items():
                    if v == addr:
                        addr = k
                        break
            arr = ['multichain-cli', self.chain, 'publishfrom', addr, name, key, data]
        else:
            arr = ['multichain-cli', self.chain, 'publish', name, key, data]

        msg = QtWidgets.QMessageBox.question(self, 'Confirm', 'Do you want to publish to the stream "'+name+'"?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            data = functions.execute(self, arr)
            if data:
                msg = QtWidgets.QMessageBox.information(self, 'Success!', 'Publishing successful')
        return

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(400, 449)
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
        self.addr_lbl_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addr_lbl_2.setFont(font)
        self.addr_lbl_2.setObjectName("addr_lbl_2")
        self.verticalLayout.addWidget(self.addr_lbl_2)
        self.stream_cbox = QtWidgets.QComboBox(self.frame)
        self.stream_cbox.setMinimumSize(QtCore.QSize(300, 30))
        self.stream_cbox.setObjectName("stream_cbox")
        self.stream_cbox.addItem("")
        self.verticalLayout.addWidget(self.stream_cbox)
        self.key_ledit = QtWidgets.QLineEdit(self.frame)
        self.key_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.key_ledit.setObjectName("key_ledit")
        self.verticalLayout.addWidget(self.key_ledit)
        self.data_ledit = QtWidgets.QLineEdit(self.frame)
        self.data_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.data_ledit.setObjectName("data_ledit")
        self.verticalLayout.addWidget(self.data_ledit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.publish_btn = QtWidgets.QPushButton(self.frame)
        self.publish_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.publish_btn.setFont(font)
        self.publish_btn.setObjectName("publish_btn")
        self.verticalLayout.addWidget(self.publish_btn, 0, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.addr_lbl.hide()
        self.addr_cbox.hide()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Publish to Stream</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "Do you want to publish with a specific wallet?"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.addr_lbl.setText(_translate("Form", "Choose Wallet"))
        self.addr_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.addr_lbl_2.setText(_translate("Form", "Choose Stream"))
        self.stream_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.key_ledit.setPlaceholderText(_translate("Form", "Enter Key"))
        self.data_ledit.setPlaceholderText(_translate("Form", "Enter data"))
        self.publish_btn.setText(_translate("Form", "Publish"))

