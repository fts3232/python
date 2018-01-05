# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStackedWidget, QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QMainWindow, QAction, QTextEdit, QGridLayout, QLabel, QLineEdit, QSlider, QLCDNumber
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QObject
import sys
# pyqt5
#
# 安装：pip install PyQt5
#
# QApplication 基础对象
#   exec_() 主循环.事件处理
#
# QCoreApplication 核心对象
#   quit 退出方法
#
# QWidget 界面的基类
#   resize(width，height) resize窗口大小
#   move(x, y) 窗口移动到xy坐标
#   setGeometry(w x, y, idth, height) 设置窗口大小和位置
#   setWidnowTitle() 设置标题
#   setWindowIcon(icon) 设置窗口icon
#   setToolTip(text) 设置悬浮提示
#   setLayout(layout) 设置布局
#   clicked.connect() 链接信号槽
#   show() 显示
#   hide() 隐藏
#   closeEvent 关闭事件,会传递一个event参数
#       event.accept() 接受事件
#       event.ignore() 忽略事件
#   keyPressEvent 键盘按下事件,会传递一个event参数
#       event.key() 获取键值
#       Qt.Key_xxx ：xxx键
#   sender() 获取发送信号者
#   close() 关闭
#   deleteLater() 删除widget
#   setAlignment() 设置对齐方式
#       Qt.AlignCenter ：居中
#       Qt.AlignTop ：顶部对齐
#       Qt.AlignLeft ： 左对齐
#       Qt.AlignRight ： 右对齐
#   setWordWrap(True) 自动换行
#
# QIcon(path) icon基类
#
# QFont(path，size) 字体基类
#
# QToolTip 悬浮提示基类
#   setFont(font) 设置字体
#
# QPushButton 按钮基类
#   QPushButton(str,parent) 文字按钮
#   QPushButton(qicon,str,parent) icon按钮
#
# QMessageBox 对话框基类
#   question(parent,title,msg,buttons,defaultButton)
#   warning(parent,title,msg,buttons,defaultButton)
#   critical(parent,title,msg,buttons,defaultButton)
#   information(parent,title,msg,buttons,defaultButton)
#   about(parent,title,msg)
#   QMessageBox.Yes yes按钮
#   QMessageBox.No  no按钮
#   QMessageBox.Cancel cancel按钮
#   QMessageBox.Ok
#   QMessageBox.Open
#   QMessageBox.Save
#   QMessageBox.Close
#   QMessageBox.Discard
#   QMessageBox.Apply
#   QMessageBox.Reset
#   QMessageBox.RestoreDefaults
#   QMessageBox.Help
#   QMessageBox.SaveAll
#   QMessageBox.YesToAll
#   QMessageBox.NoToAl
#   QMessageBox.Abort
#   QMessageBox.Retry
#   QMessageBox.Ignor
#   QMessageBox.NoButton
#
# QMainWindow 主窗口基类
#   statusBar() 状态栏
#       showMessage() 显示信息
#
#   menBar() 菜单栏
#       addMenu(str) 添加菜单
#           addAction(QAction) 为菜单添加动作
#
#   addToolBar(str) 添加工具栏
#       addAction(QAction) 为工具栏添加动作
#
#   setCentralWidget(widget) 把widget放在中心，并占据剩余的其他位置
#
# QAction(icon,str) 动作基类
#   setShortcut() 设置快捷键
#   setStatusTip(text) 设置状态栏提示
#   triggered.connect() 执行动作时会发送triggered信号
#
# QTextEdit 多行文本框基类
#
# QLineEdit 单行文本框基类
#
# QLabel 标签基类
#   setPixmap(QPixmap) 设置图片
#
# QGridLayout() 网格布局
#   addWidget(widget,row,column) 添加widget
#   removeWidget(widget) 删除widget
#   setSpacing(space) 设置网格距离
#
# QSlider(Qt.Horizontal) slider基类
#   valueChanged.connect() 发送数值变化信号
#
# QLCDNumber() LCD数字面板基类
#   display(val) 显示数字
#
# pyqtSignal() 信号源
#    emit() 发送信号
#
# QPixmap(path) 一个用于处理图像的部件
#
# QStackedWidget 分页布局
#   addWidget(widget)
#   currentIndex() 当前页面索引
#   setCurrentIndex(index) 切换页面
#   count() 总页数
#

app = QApplication(sys.argv)

mainWindow = QMainWindow()
widget = QWidget()

# 主窗口大小
mainWindow.setGeometry(300, 300, 800, 400)
# 主窗口标题
mainWindow.setWindowTitle('Title')
# 主窗口icon
mainWindow.setWindowIcon(QIcon('../favicon.ico'))
# 菜单栏
menubar = mainWindow.menuBar()
menu = menubar.addMenu('menu')
menu2 = menubar.addMenu('menu2')
# 状态栏
mainWindow.statusBar().showMessage('这里是状态栏...')
# 布局 网格间隔为10
grid = QGridLayout()
grid.setSpacing(10)
widget.setLayout(grid)
mainWindow.setCentralWidget(widget)
# 文本框
text = QTextEdit()
grid.addWidget(text, 1, 1)
# 按钮
run_btn = QPushButton('启动')
run_btn.clicked.connect(splider)
grid.addWidget(run_btn, 2, 1)
play_btn = QPushButton('播放')
grid.addWidget(play_btn, 2, 2)
download_btn = QPushButton('下载')
grid.addWidget(download_btn, 2, 3)
# 显示主窗口
mainWindow.show()
# 主循环
sys.exit(app.exec_())
