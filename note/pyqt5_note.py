# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets  # 导入模块
import sys
# PyQt5
#
# 安装：pip install PyQt5
#


class Ui_Form(object):  # 创建窗口类，继承object
    _signal = QtCore.pyqtSignal(str)
    def setupUi(self, Form):
        Form.setObjectName("Form")  # 设置窗口名
        Form.resize(400, 300)  # 设置窗口大小
        self.quitButton = QtWidgets.QPushButton(Form)  # 创建一个按钮，并将按钮加入到窗口Form中
        self.quitButton.setGeometry(QtCore.QRect(280, 240, 75, 23))  # 设置按钮大小与位置
        self.quitButton.setObjectName("quitButton")  # 设置按钮名
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)  # 关联信号槽
        self.quitButton.clicked.connect(self.myPrint)
        self._signal.connect(self.mySignal)               #将信号连接到函数mySignal  

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Test"))  # 设置窗口标题
        self.quitButton.setText(_translate("Form", "Quit"))  # 设置按钮显示文字

    def myPrint(self):
        print('close')

    def mySignal(self, string):
        self._signal.emit("你妹，打印结束了吗，快回答！")


app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(widget)
widget.show()
sys.exit(app.exec_())
