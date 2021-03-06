# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.line_lat = QtWidgets.QLineEdit(self.centralwidget)
        self.line_lat.setEnabled(True)
        self.line_lat.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.line_lat.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.line_lat.setObjectName("line_lat")
        self.gridLayout.addWidget(self.line_lat, 1, 3, 1, 1)
        self.label_lat = QtWidgets.QLabel(self.centralwidget)
        self.label_lat.setObjectName("label_lat")
        self.gridLayout.addWidget(self.label_lat, 1, 2, 1, 1)
        self.spin_zoom = QtWidgets.QSpinBox(self.centralwidget)
        self.spin_zoom.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.spin_zoom.setMinimum(1)
        self.spin_zoom.setMaximum(19)
        self.spin_zoom.setProperty("value", 13)
        self.spin_zoom.setObjectName("spin_zoom")
        self.gridLayout.addWidget(self.spin_zoom, 2, 1, 1, 1)
        self.line_lon = QtWidgets.QLineEdit(self.centralwidget)
        self.line_lon.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.line_lon.setObjectName("line_lon")
        self.gridLayout.addWidget(self.line_lon, 1, 1, 1, 1)
        self.label_error_msg = QtWidgets.QLabel(self.centralwidget)
        self.label_error_msg.setText("")
        self.label_error_msg.setObjectName("label_error_msg")
        self.gridLayout.addWidget(self.label_error_msg, 2, 3, 1, 1)
        self.label_zoom = QtWidgets.QLabel(self.centralwidget)
        self.label_zoom.setObjectName("label_zoom")
        self.gridLayout.addWidget(self.label_zoom, 2, 0, 1, 1)
        self.label_lon = QtWidgets.QLabel(self.centralwidget)
        self.label_lon.setObjectName("label_lon")
        self.gridLayout.addWidget(self.label_lon, 1, 0, 1, 1)
        self.line_search = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_search.sizePolicy().hasHeightForWidth())
        self.line_search.setSizePolicy(sizePolicy)
        self.line_search.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.line_search.setObjectName("line_search")
        self.gridLayout.addWidget(self.line_search, 0, 0, 1, 4)
        self.btn_search = QtWidgets.QPushButton(self.centralwidget)
        self.btn_search.setObjectName("btn_search")
        self.gridLayout.addWidget(self.btn_search, 0, 4, 1, 1)
        self.btn_reset = QtWidgets.QPushButton(self.centralwidget)
        self.btn_reset.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btn_reset.setObjectName("btn_reset")
        self.gridLayout.addWidget(self.btn_reset, 0, 5, 1, 1)
        self.btn_run = QtWidgets.QPushButton(self.centralwidget)
        self.btn_run.setObjectName("btn_run")
        self.gridLayout.addWidget(self.btn_run, 1, 4, 1, 2)
        self.btn_change_map = QtWidgets.QPushButton(self.centralwidget)
        self.btn_change_map.setObjectName("btn_change_map")
        self.gridLayout.addWidget(self.btn_change_map, 2, 4, 1, 2)
        self.label_map = QtWidgets.QLabel(self.centralwidget)
        self.label_map.setText("")
        self.label_map.setObjectName("label_map")
        self.gridLayout.addWidget(self.label_map, 3, 0, 1, 6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.line_lat.setText(_translate("MainWindow", "55.753630"))
        self.label_lat.setText(_translate("MainWindow", "Широта:"))
        self.line_lon.setText(_translate("MainWindow", "37.620070"))
        self.label_zoom.setText(_translate("MainWindow", "Масштаб:"))
        self.label_lon.setText(_translate("MainWindow", "Долгота:"))
        self.line_search.setText(_translate("MainWindow", "Элиста экг"))
        self.btn_search.setText(_translate("MainWindow", "Поиск"))
        self.btn_reset.setText(_translate("MainWindow", "Сброс"))
        self.btn_run.setText(_translate("MainWindow", "Выполнить"))
        self.btn_change_map.setText(_translate("MainWindow", "Тип карты"))
