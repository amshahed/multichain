import functions
from PyQt5 import QtCore, QtWidgets
import grant, revoke, issue, send, issuemore, listpermissions, balance, blockchainparams, newaddress
import transactions, create, publish, listitems


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

    def setup(self):
        self.setupUi()
        self.stack.setCurrentIndex(7)
        self.page_8.addr = functions.fetch_my_wallets(self.page_8,  self.page_8.chain)
        self.page_8.fill_addresses()
        self.page_8.show_balance()
        self.sidebar.itemClicked.connect(self.change_index)

    def change_index(self, item, col):
        str = item.text(col).lower()

        if str == 'grant':
            self.stack.setCurrentIndex(1)
            self.page_2.wallets = functions.fetch_from_stream(self.page_2, self.page_2.chain, 'root')
            self.page_2.fill_addresses()

        elif str == 'revoke':
            self.stack.setCurrentIndex(2)
            self.page_3.wallets = functions.fetch_from_stream(self.page_3, self.page_3.chain, 'root')
            self.page_3.fill_addresses()

        elif str == 'issue':
            self.stack.setCurrentIndex(3)
            self.page_4.addr = functions.fetch_wallets_with_single_permission(self.page_4, self.page_4.chain, 'issue', True)
            self.page_4.to_addr = functions.fetch_wallets_with_single_permission(self.page_4, self.page_4.chain, 'receive')
            self.page_4.fill_addresses()

        elif str == 'issue more':
            self.stack.setCurrentIndex(4)
            self.page_5.addr = functions.fetch_wallets_with_single_permission(self.page_5, self.page_5.chain, 'issue', True)
            self.page_5.to_addr = functions.fetch_wallets_with_single_permission(self.page_5, self.page_5.chain, 'receive')
            self.page_5.fill_addresses()

        elif str == 'send':
            self.stack.setCurrentIndex(5)
            self.page_6.addr = functions.fetch_wallets_with_single_permission(self.page_6, self.page_6.chain, 'receive')
            self.page_6.from_addr = functions.fetch_wallets_with_single_permission(self.page_6, self.page_6.chain, 'send', True)
            self.page_6.fill_addresses()

        elif str == 'list permissions':
            self.page_7.fetch_permissions()
            self.stack.setCurrentIndex(6)

        elif str == 'balance':
            self.stack.setCurrentIndex(7)
            self.page_8.addr = functions.fetch_my_wallets(self.page_8,  self.page_8.chain)
            self.page_8.fill_addresses()
            self.page_8.show_balance()

        elif str == 'list parameters':
            self.stack.setCurrentIndex(8)

        elif str == 'new wallet':
            self.stack.setCurrentIndex(9)

        elif str == 'list transactions':
            self.stack.setCurrentIndex(10)
            self.page_11.wallets = functions.fetch_my_wallets(self.page_11,  self.page_11.chain)
            self.page_11.fetch_wallets()
            self.page_11.fetch_transactions()

        elif str == 'create':
            self.stack.setCurrentIndex(11)
            self.page_12.wallets = functions.fetch_wallets_with_single_permission(self.page_12, self.page_12.chain, 'create', True)
            self.page_12.fill_wallets()

        elif str == 'publish':
            self.stack.setCurrentIndex(12)
            self.page_13.wallets = functions.fetch_wallets_with_single_permission(self.page_13, self.page_13.chain, 'send', True)
            self.page_13.fill_wallets()
            self.page_13.fill_streams()

        elif str == 'list stream items':
            self.stack.setCurrentIndex(13)
            self.page_14.wallets = functions.fetch_from_stream(self.page_14, self.page_14.chain, 'root')
            self.page_14.fill_streams()
            self.page_14.fill_wallets()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(554, 422)
        self.centralwidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.sidebar = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar.sizePolicy().hasHeightForWidth())
        self.sidebar.setSizePolicy(sizePolicy)
        self.sidebar.setMinimumSize(QtCore.QSize(200, 360))
        self.sidebar.setMaximumSize(QtCore.QSize(200, 10000000))
        self.sidebar.setStyleSheet("")
        self.sidebar.setAnimated(True)
        self.sidebar.setObjectName("sidebar")
        item_0 = QtWidgets.QTreeWidgetItem(self.sidebar)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.sidebar)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.sidebar)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.sidebar)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.sidebar)
        item_0.setExpanded(True)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.gridLayout.addWidget(self.sidebar, 0, 0, 1, 1)
        self.stack = QtWidgets.QStackedWidget(self.centralwidget)
        self.stack.setMinimumSize(QtCore.QSize(330, 360))
        self.stack.setObjectName("stack")

        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stack.addWidget(self.page)

        self.page_2 = grant.GrantWindow(self.chain)
        self.page_2.setObjectName("page_2")
        self.stack.addWidget(self.page_2)

        self.page_3 = revoke.RevokeWindow(self.chain)
        self.page_3.setObjectName("page_3")
        self.stack.addWidget(self.page_3)

        self.page_4 = issue.IssueWindow(self.chain)
        self.page_4.setObjectName("page_4")
        self.stack.addWidget(self.page_4)

        self.page_5 = issuemore.IssueMoreWindow(self.chain)
        self.page_5.setObjectName("page_5")
        self.stack.addWidget(self.page_5)

        self.page_6 = send.SendWindow(self.chain)
        self.page_6.setObjectName("page_6")
        self.stack.addWidget(self.page_6)

        self.page_7 = listpermissions.ListPermissionsWindow(self.chain)
        self.page_7.setObjectName("page_7")
        self.stack.addWidget(self.page_7)

        self.page_8 = balance.BalanceWindow(self.chain)
        self.page_8.setObjectName("page_8")
        self.stack.addWidget(self.page_8)

        self.page_9 = blockchainparams.ParameterWindow(self.chain)
        self.page_9.setObjectName("page_9")
        self.stack.addWidget(self.page_9)

        self.page_10 = newaddress.NewWalletWindow(self.chain)
        self.page_10.setObjectName("page_10")
        self.stack.addWidget(self.page_10)

        self.page_11 = transactions.TransactionWindow(self.chain)
        self.page_11.setObjectName("page_11")
        self.stack.addWidget(self.page_11)

        self.page_12 = create.CreateWindow(self.chain)
        self.page_12.setObjectName("page_12")
        self.stack.addWidget(self.page_12)

        self.page_13 = publish.PublishWindow(self.chain)
        self.page_13.setObjectName("page_13")
        self.stack.addWidget(self.page_13)

        self.page_14 = listitems.StreamItemsWindow(self.chain)
        self.page_14.setObjectName("page_14")
        self.stack.addWidget(self.page_14)

        self.gridLayout.addWidget(self.stack, 0, 1, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 554, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.retranslateUi()
        self.stack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Multichain"))
        self.sidebar.headerItem().setText(0, _translate("MainWindow", "Menu"))
        __sortingEnabled = self.sidebar.isSortingEnabled()
        self.sidebar.setSortingEnabled(False)
        self.sidebar.topLevelItem(0).setText(0, _translate("MainWindow", "Chain"))
        self.sidebar.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "List Parameters"))
        self.sidebar.topLevelItem(1).setText(0, _translate("MainWindow", "Wallet"))
        self.sidebar.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "New Wallet"))
        self.sidebar.topLevelItem(2).setText(0, _translate("MainWindow", "Permissions"))
        self.sidebar.topLevelItem(2).child(0).setText(0, _translate("MainWindow", "Grant"))
        self.sidebar.topLevelItem(2).child(1).setText(0, _translate("MainWindow", "Revoke"))
        self.sidebar.topLevelItem(2).child(2).setText(0, _translate("MainWindow", "List Permissions"))
        self.sidebar.topLevelItem(3).setText(0, _translate("MainWindow", "Asset"))
        self.sidebar.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "Issue"))
        self.sidebar.topLevelItem(3).child(1).setText(0, _translate("MainWindow", "Issue More"))
        self.sidebar.topLevelItem(3).child(2).setText(0, _translate("MainWindow", "Send"))
        self.sidebar.topLevelItem(3).child(3).setText(0, _translate("MainWindow", "Balance"))
        self.sidebar.topLevelItem(3).child(4).setText(0, _translate("MainWindow", "List Transactions"))
        self.sidebar.topLevelItem(4).setText(0, _translate("MainWindow", "Stream"))
        self.sidebar.topLevelItem(4).child(0).setText(0, _translate("MainWindow", "Create"))
        self.sidebar.topLevelItem(4).child(1).setText(0, _translate("MainWindow", "Publish"))
        self.sidebar.topLevelItem(4).child(2).setText(0, _translate("MainWindow", "List Stream Items"))
        self.sidebar.setSortingEnabled(__sortingEnabled)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

