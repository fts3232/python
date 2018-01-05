# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStackedWidget, QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QMainWindow, QAction, QTextEdit, QGridLayout, QLabel, QLineEdit, QSlider, QLCDNumber
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QObject, QThread, QRect
from JavBus import JavBus
import sys
from Visitor import Visitor
from Mysql import ConnectionPool
import threading

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'JavBus',
    'charset': 'utf8',
    'max_connection': 10,
    'min_connection': 2,
}


# 子线程不能直接append，所以在子线程发送信号给主线程的信号槽，让主线程执行append
def send_signal(message):
    signal.signal.emit(message)


def my_print(message):
    text.append(message)


class MySignal(QObject):
    signal = pyqtSignal(str)


def run():
    count = a.count()
    currentIndex = a.currentIndex()
    if(currentIndex + 1 < count):
        a.setCurrentIndex(currentIndex + 1)
    else:
        a.setCurrentIndex(0)
    # status = run_btn.text()
    # if(status == '启动'):
    #     run_btn.setText('暂停')
    #     task.start()
    # else:
    #     run_btn.setText('启动')


def splider():
    mainWindow.statusBar().showMessage('爬取中...')
    obj = JavBus(Visitor(), pool, send_signal)
    obj.run()
    mainWindow.statusBar().showMessage('爬取结束...')


def create_page():
    db = pool.conn()
    ret = db.select('select * from MOVIE')
    page = QWidget()
    # grid = QGridLayout()
    # grid.setSpacing(10)
    # page.setLayout(grid)
    offset_x = 0
    offset_y = 0
    space = 10
    for x in ret[:15]:
        label = QLabel(parent=page)
        img = QPixmap('./JavBus/2017-12-27\ANY-002/cover.jpg')
        label.setPixmap(img)
        label.setGeometry(QRect(offset_x, offset_y, 150, 100))
        label.setScaledContents(True)
        label.setAlignment(Qt.AlignCenter)
        offset_x += 150 + space
        if(offset_x==800):
            offset_x = 0
            offset_y += 100 + space
        # grid.addWidget(label, row, column)

        # label = QLabel(x['TITLE'],parent=page)
        #label.adjustSize()
        #label.setWordWrap(True)
        #label.setAlignment(Qt.AlignCenter)
        # label.setGeometry(QRect(60, 150, 21, 16))
        # grid.addWidget(label, row + 1, column)
        # column += 1
        # if(column > 4):
        #     row += 2
        #     column = 0
    a.addWidget(page)


pool = ConnectionPool(config)
task = threading.Thread(target=splider)
task.setDaemon(True)

# 应用
app = QApplication(sys.argv)
# 主窗口
mainWindow = QMainWindow()
widget = QWidget()
# 主窗口大小
mainWindow.setGeometry(300, 300, 800, 600)
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
# 信号
signal = MySignal()
signal.signal.connect(my_print)
# 布局 网格间隔为10
grid = QGridLayout()
grid.setSpacing(10)
widget.setLayout(grid)
mainWindow.setCentralWidget(widget)
# 文本框
# text = QTextEdit()
# grid.addWidget(text, 1, 1)
# text.deleteLater()
a = QStackedWidget()
create_page()
# # page1
# page1 = QWidget()
# grid1 = QGridLayout()
# grid1.setSpacing(10)
# page1.setLayout(grid1)
# label1 = QLabel("add a image file")
# grid1.addWidget(label1, 1, 1)
# a.addWidget(page1)
# # page2
# page2 = QWidget()
# grid2 = QGridLayout()
# grid2.setSpacing(10)
# page2.setLayout(grid2)
# label2 = QLabel("add2 a image file")
# grid2.addWidget(label2, 1, 1)
# a.addWidget(page2)
# # page3
# page3 = QWidget()
# grid3 = QGridLayout()
# grid3.setSpacing(10)
# page3.setLayout(grid3)
# label3 = QLabel("add3 a image file")
# grid3.addWidget(label3, 1, 1)
# a.addWidget(page3)
# label = QLabel("add a image file")
# label.setPixmap(QPixmap('./favicon.ico'))
grid.addWidget(a, 1, 1)

# 按钮
run_btn = QPushButton('启动')
run_btn.clicked.connect(run)
grid.addWidget(run_btn, 2, 1)
# play_btn = QPushButton('播放')
# grid.addWidget(play_btn, 2, 2)
# download_btn = QPushButton('下载')
# grid.addWidget(download_btn, 2, 3)

# 显示主窗口
mainWindow.show()
# 主循环
sys.exit(app.exec_())
