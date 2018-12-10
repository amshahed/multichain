import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class CreateWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(CreateWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.yes_rbtn.toggled.connect(self.toggle_combo_box)
        self.create_btn.clicked.connect(self.create_stream)

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

    def create_stream(self):
        name = self.stream_ledit.text()
        if len(name) < 3:
            msg = QtWidgets.QMessageBox.information(self, 'Invalid Name!', 'Name length should be at least 3')
            return

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
                arr = ['multichain-cli', self.chain, 'createfrom', addr, 'stream', name, 'true']
        else:
            arr = ['multichain-cli', self.chain, 'create', 'stream', name, 'true']

        msg = QtWidgets.QMessageBox.question(self, 'Confirm', 'Do you want to create the stream "'+name+'"?',
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if msg == QtWidgets.QMessageBox.Yes:
            data = functions.execute(self, arr)
            if data:
                msg = QtWidgets.QMessageBox.information(self, 'Success!', 'Create successful!')
        return

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(383, 394)
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
        self.stream_ledit = QtWidgets.QLineEdit(self.frame)
        self.stream_ledit.setMinimumSize(QtCore.QSize(300, 30))
        self.stream_ledit.setObjectName("stream_ledit")
        self.verticalLayout.addWidget(self.stream_ledit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.create_btn = QtWidgets.QPushButton(self.frame)
        self.create_btn.setMinimumSize(QtCore.QSize(120, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.create_btn.setFont(font)
        self.create_btn.setObjectName("create_btn")
        self.verticalLayout.addWidget(self.create_btn, 0, QtCore.Qt.AlignHCenter)
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
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Create Stream</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "Do you want to use a specific wallet?"))
        self.yes_rbtn.setText(_translate("Form", "Yes"))
        self.no_rbtn.setText(_translate("Form", "No"))
        self.addr_lbl.setText(_translate("Form", "Choose Wallet"))
        self.addr_cbox.setItemText(0, _translate("Form", "- - - - - - - - - -"))
        self.stream_ledit.setPlaceholderText(_translate("Form", "Enter Name of Stream"))
        self.create_btn.setText(_translate("Form", "Create"))

