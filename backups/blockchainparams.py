import json
import functions
from PyQt5 import QtCore, QtGui, QtWidgets


class ParameterWindow(QtWidgets.QWidget):

    def __init__(self, chain):
        super(ParameterWindow, self).__init__()
        self.chain = chain
        self.setupUi()
        self.fetch_parameters()

    def fetch_parameters(self):
        arr = ['multichain-cli', self.chain, 'getblockchainparams']
        data = functions.execute(self, arr)
        if data:
            data = json.loads(data.decode('utf-8'))
            self.param_table.setRowCount(len(data))
            i = 0
            for key, value in data.items():
                self.param_table.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
                self.param_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value)))
                i = i + 1
        else:
            return False

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.param_table = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.param_table.sizePolicy().hasHeightForWidth())
        self.param_table.setSizePolicy(sizePolicy)
        self.param_table.setMinimumSize(QtCore.QSize(315, 30))
        self.param_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.param_table.setLineWidth(1)
        self.param_table.setShowGrid(True)
        self.param_table.setGridStyle(QtCore.Qt.DotLine)
        self.param_table.setRowCount(1)
        self.param_table.setObjectName("param_table")
        self.param_table.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.param_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.param_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.param_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.param_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.param_table.setItem(0, 1, item)
        self.param_table.horizontalHeader().setVisible(True)
        self.param_table.horizontalHeader().setCascadingSectionResizes(True)
        self.param_table.horizontalHeader().setDefaultSectionSize(100)
        self.param_table.horizontalHeader().setMinimumSectionSize(100)
        self.param_table.horizontalHeader().setStretchLastSection(False)
        self.param_table.verticalHeader().setCascadingSectionResizes(True)
        self.param_table.verticalHeader().setMinimumSectionSize(30)
        self.param_table.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout.addWidget(self.param_table)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.param_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.param_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<h2>Chain Parameters<h2>"))
        self.param_table.setSortingEnabled(True)
        item = self.param_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.param_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Parameter"))
        item = self.param_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Value"))
        __sortingEnabled = self.param_table.isSortingEnabled()
        self.param_table.setSortingEnabled(False)
        item = self.param_table.item(0, 0)
        item.setText(_translate("Form", "open"))
        item = self.param_table.item(0, 1)
        item.setText(_translate("Form", "true"))
        self.param_table.setSortingEnabled(__sortingEnabled)

