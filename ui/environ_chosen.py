# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'environ_chosen.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_environ_chosen(object):
    def setupUi(self, environ_chosen):
        environ_chosen.setObjectName("environ_chosen")
        environ_chosen.setWindowModality(QtCore.Qt.ApplicationModal)
        environ_chosen.resize(380, 200)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        environ_chosen.setFont(font)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(environ_chosen)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lw_env_list = QtWidgets.QListWidget(environ_chosen)
        self.lw_env_list.setObjectName("lw_env_list")
        self.verticalLayout.addWidget(self.lw_env_list)
        self.label = QtWidgets.QLabel(environ_chosen)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(environ_chosen)
        QtCore.QMetaObject.connectSlotsByName(environ_chosen)

    def retranslateUi(self, environ_chosen):
        _translate = QtCore.QCoreApplication.translate
        environ_chosen.setWindowTitle(_translate("environ_chosen", "选择 Python 环境"))
        self.label.setText(_translate("environ_chosen", "如果此处没有可选择的 Python 环境则需先到<包管理器>中添加。"))
