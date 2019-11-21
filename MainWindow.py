# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'magicPlot.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1071, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout3.setObjectName("horizontalLayout3")
        self.tableView3 = QtWidgets.QTableView(self.centralwidget)
        self.tableView3.setObjectName("tableView3")
        self.horizontalLayout3.addWidget(self.tableView3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout3)
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.tableView2 = QtWidgets.QTableView(self.centralwidget)
        self.tableView2.setObjectName("tableView2")
        self.horizontalLayout2.addWidget(self.tableView2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout2)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1071, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menuGraph = QtWidgets.QMenu(self.menubar)
        self.menuGraph.setObjectName("menuGraph")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionConfig = QtWidgets.QAction(MainWindow)
        self.actionConfig.setObjectName("actionConfig")
        self.actionPlot = QtWidgets.QAction(MainWindow)
        self.actionPlot.setObjectName("actionPlot")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionConfig)
        self.menuGraph.addAction(self.actionPlot)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuGraph.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menuGraph.setTitle(_translate("MainWindow", "Graph"))
        self.actionOpen.setText(_translate("MainWindow", "Open "))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionConfig.setText(_translate("MainWindow", "Config"))
        self.actionConfig.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.actionPlot.setText(_translate("MainWindow", "Plot"))
        self.actionPlot.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
    
    
