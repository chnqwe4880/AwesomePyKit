# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'check_imports.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_check_imports(object):
    def setupUi(self, check_imports):
        check_imports.setObjectName("check_imports")
        check_imports.setWindowModality(QtCore.Qt.ApplicationModal)
        check_imports.resize(900, 566)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        check_imports.setFont(font)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(check_imports)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(check_imports)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_cip_cur_env = QtWidgets.QLineEdit(check_imports)
        self.le_cip_cur_env.setFrame(False)
        self.le_cip_cur_env.setReadOnly(True)
        self.le_cip_cur_env.setObjectName("le_cip_cur_env")
        self.horizontalLayout_2.addWidget(self.le_cip_cur_env)
        self.horizontalLayout_2.setStretch(1, 9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tw_missing_imports = QtWidgets.QTableWidget(check_imports)
        self.tw_missing_imports.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_missing_imports.setObjectName("tw_missing_imports")
        self.tw_missing_imports.setColumnCount(3)
        self.tw_missing_imports.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tw_missing_imports.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_missing_imports.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_missing_imports.setHorizontalHeaderItem(2, item)
        self.tw_missing_imports.horizontalHeader().setHighlightSections(False)
        self.tw_missing_imports.verticalHeader().setHighlightSections(False)
        self.verticalLayout.addWidget(self.tw_missing_imports)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_install_all_missing = QtWidgets.QPushButton(check_imports)
        self.pb_install_all_missing.setObjectName("pb_install_all_missing")
        self.horizontalLayout.addWidget(self.pb_install_all_missing)
        self.pb_confirm = QtWidgets.QPushButton(check_imports)
        self.pb_confirm.setObjectName("pb_confirm")
        self.horizontalLayout.addWidget(self.pb_confirm)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(check_imports)
        QtCore.QMetaObject.connectSlotsByName(check_imports)

    def retranslateUi(self, check_imports):
        _translate = QtCore.QCoreApplication.translate
        check_imports.setWindowTitle(_translate("check_imports", "导入项检查(测试)"))
        self.label.setText(_translate("check_imports", "当前环境:"))
        item = self.tw_missing_imports.horizontalHeaderItem(0)
        item.setText(_translate("check_imports", "项目文件"))
        item = self.tw_missing_imports.horizontalHeaderItem(1)
        item.setText(_translate("check_imports", "文件导入项"))
        item = self.tw_missing_imports.horizontalHeaderItem(2)
        item.setText(_translate("check_imports", "环境缺失项"))
        self.pb_install_all_missing.setText(_translate("check_imports", "一键安装"))
        self.pb_confirm.setText(_translate("check_imports", "确定"))