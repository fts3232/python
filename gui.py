# # -*- coding: utf-8 -*-
# from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QMainWindow, QAction, QTextEdit, QGridLayout, QLabel, QLineEdit, QSlider, QLCDNumber
# from PyQt5.QtGui import QIcon, QFont
# from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QObject,  QThread
# from PyQt5 import *
# from JavBus import JavBus
# import sys
# from Visitor import Visitor
# from Mysql import ConnectionPool

# config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'db': 'JavBus',
#     'charset': 'utf8',
#     'max_connection': 10,
#     'min_connection': 2,
# }


# def my_print(message):
#     text.append(message)


# class MyThread(QThread):
#     signal = pyqtSignal()

#     def run():
#         mainWindow.statusBar().showMessage('爬取中...')
#         obj = JavBus(Visitor(), ConnectionPool(config), my_print)
#         obj.run()
#         mainWindow.statusBar().showMessage('爬取结束...')


# # 应用
# app = QApplication(sys.argv)
# # 主窗口
# mainWindow = QMainWindow()
# widget = QWidget()
# # 主窗口大小
# mainWindow.setGeometry(300, 300, 800, 400)
# # 主窗口标题
# mainWindow.setWindowTitle('Title')
# # 主窗口icon
# mainWindow.setWindowIcon(QIcon('../favicon.ico'))
# # 菜单栏
# menubar = mainWindow.menuBar()
# menu = menubar.addMenu('menu')
# menu2 = menubar.addMenu('menu2')
# # 状态栏
# mainWindow.statusBar().showMessage('这里是状态栏...')
# # 信号
# thread = MyThread()
# thread.signal.connect(splider)
# thread.signal.start()
# # 布局 网格间隔为10
# grid = QGridLayout()
# grid.setSpacing(10)
# widget.setLayout(grid)
# mainWindow.setCentralWidget(widget)
# # 文本框
# text = QTextEdit()
# grid.addWidget(text, 1, 1)
# # 按钮
# run_btn = QPushButton('启动')
# run_btn.clicked.connect(start)
# grid.addWidget(run_btn, 2, 1)
# play_btn = QPushButton('播放')
# grid.addWidget(play_btn, 2, 2)
# download_btn = QPushButton('下载')
# grid.addWidget(download_btn, 2, 3)
# # 显示主窗口
# mainWindow.show()
# # 主循环
# sys.exit(app.exec_())



from PyQt5.QtCore import QThread ,  pyqtSignal,  QDateTime 
from PyQt5.QtWidgets import QApplication,  QDialog,  QLineEdit
import time
import sys

class BackendThread(QThread):
     # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

     # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit( str(currTime) )
            time.sleep(1)

class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('PyQt 5界面实时更新例子')
        self.resize(400, 100)
        self.input = QLineEdit(self)
        self.input.resize(400, 100)
        self.initUI()

    def initUI(self):
          # 创建线程
        self.backend = BackendThread()
          # 连接信号
        self.backend.update_date.connect(self.handleDisplay)
          # 开始线程
        self.backend.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        self.input.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show() 
    sys.exit(app.exec_())