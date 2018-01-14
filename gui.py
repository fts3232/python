# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStackedWidget, QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QMainWindow, QAction, QTextEdit, QGridLayout, QLabel, QLineEdit, QSlider, QLCDNumber
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QObject, QThread, QRect, QFile
from JavBus import JavBus
import sys
from Visitor import Visitor
from Mysql import ConnectionPool
import threading
import math
import subprocess


# 子线程不能直接append，所以在子线程发送信号给主线程的信号槽，让主线程执行append
def send_signal(message):
    signal.signal.emit(message)


def my_print(message):
    print(message)
    # text.append(message)


def run():
    count = pages.count()
    currentIndex = pages.currentIndex()
    if(currentIndex + 1 < count):
        pages.setCurrentIndex(currentIndex + 1)
    else:
        pages.setCurrentIndex(0)
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


class MySignal(QObject):
    print_signal = pyqtSignal(str)
    show_single_page = pyqtSignal(str)


class Gui:
    __app = None
    __mainWindow = None
    __pages = None
    __signal = None
    __back_page = None

    def __init__(self):
        # 应用
        self.__app = QApplication(sys.argv)
        # 主窗口
        self.__mainWindow = QMainWindow()
        # 样式表
        file = QFile('style.qss')
        file.open(QFile.ReadOnly)
        styleSheet = file.readAll()
        styleSheet = str(styleSheet, encoding='utf8')
        self.__mainWindow.setStyleSheet(styleSheet)
        # 主窗口大小
        self.__mainWindow.setGeometry(300, 300, 940, 610)
        # 主窗口标题
        self.__mainWindow.setWindowTitle('Title')
        # 主窗口icon
        self.__mainWindow.setWindowIcon(QIcon('../favicon.ico'))
        # 菜单栏
        menubar = self.__mainWindow.menuBar()
        menubar.addMenu('menu')
        menubar.addMenu('menu2')
        # 状态栏
        self.__mainWindow.statusBar().showMessage('这里是状态栏...')
        # 信号
        self.__signal = MySignal()
        self.__signal.show_single_page.connect(my_print)
        # signal.signal.connect(my_print)
        pass

    def setUI(self):
        widget = QWidget()
        self.__mainWindow.setCentralWidget(widget)
        # 布局 网格间隔为10
        grid = QGridLayout()
        grid.setSpacing(10)
        widget.setLayout(grid)
        # 页面
        self.__pages = QStackedWidget()
        self.create_console_page(self.__pages)
        self.create_single_page(self.__pages)
        self.create_list_page(self.__pages)
        self.__pages.setCurrentIndex(2)
        grid.addWidget(self.__pages, 1, 1)
        # play_btn = QPushButton('播放')
        # grid.addWidget(play_btn, 2, 2)
        # download_btn = QPushButton('下载')
        # grid.addWidget(download_btn, 2, 3)

    def show(self):
        # 显示主窗口
        self.__mainWindow.show()
        # 主循环
        sys.exit(self.__app.exec_())

    def create_single_page(self, widget):
        page = QWidget()
        # 图片
        label = QLabel(parent=page)
        label.setObjectName('big_image')
        label.setGeometry(QRect(0, 30, 680, 450))
        label.setAlignment(Qt.AlignCenter)
        # 标题
        label = QLabel('片名:', parent=page)
        label.adjustSize()
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)
        label.setGeometry(QRect(710, 40, 210, 20))
        label = QLabel('', parent=page)
        label.setObjectName('title')
        label.adjustSize()
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)
        label.setGeometry(QRect(710, 60, 210, 50))
        # tag
        label = QLabel('Tag:', parent=page)
        label.adjustSize()
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)
        label.setGeometry(QRect(710, 110, 210, 20))
        label = QLabel('', parent=page)
        label.setObjectName('tag')
        label.adjustSize()
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft)
        label.setGeometry(QRect(710, 130, 210, 50))
        # pic
        offset_x = 0
        bottom_widget = QWidget(parent=page)
        bottom_widget.setObjectName('bottom_widget')
        bottom_widget.setGeometry(QRect(0, 490, 680, 50))
        for x in list(range(20)):
            if(x % 2 == 0):
                pic = './asdasdno_wm.jpg'
            else:
                pic = './camera.png'
            label = QLabel(parent=bottom_widget)
            label.setObjectName('pic-box')
            img = QPixmap(pic)
            img = img.scaled(50, 50, Qt.KeepAspectRatio)
            label.setPixmap(img)
            label.setGeometry(QRect(offset_x, 0, 50, 50))
            label.setAlignment(Qt.AlignCenter)
            label.mousePressEvent = self.thumbnail_click(pic)
            offset_x += 60
        # 按钮
        back_btn = QPushButton('后退', parent=page)
        back_btn.setGeometry(QRect(0, 0, 50, 20))
        back_btn.clicked.connect(self.back_page)
        download_btn = QPushButton('下载', parent=page)
        download_btn.setGeometry(QRect(710, 190, 50, 20))
        download_btn.clicked.connect(self.download)
        play_btn = QPushButton('播放', parent=page)
        play_btn.setGeometry(QRect(770, 190, 50, 20))
        play_btn.clicked.connect(self.play)
        widget.addWidget(page)

    def thumbnail_click(self, pic):
        return lambda x: self.change_big_image(pic)

    def change_big_image(self, pic):
        label = self.__pages.findChild((QLabel, ), 'big_image')
        img = QPixmap(pic)
        img = img.scaled(680, 450, Qt.KeepAspectRatio)
        label.setPixmap(img)

    def create_console_page(self, widget):
        page = QWidget()
        widget.addWidget(page)

    def create_list_page(self, widget):
        db = pool.conn()
        size = 6
        ret = db.select('select * from MOVIE')
        count = len(ret)
        offset = math.ceil(count / size)
        start = 0
        for x in list(range(offset)):
            end = start + size
            page = QWidget()
            self.create_list_page_item(page, ret[start:end])
            start = end
            widget.addWidget(page)

    def list_item_click(self, data):
        return lambda x: self.show_single_page(data)

    def show_single_page(self, data):
        self.__back_page = self.__pages.currentIndex()
        self.__pages.setCurrentIndex(1)

        big_image = self.__pages.findChild((QLabel, ), 'big_image')
        img = QPixmap('./JavBus/{identifier}/cover.jpg'.format(identifier=data['IDENTIFIER']))
        img = img.scaled(680, 450, Qt.KeepAspectRatio)
        big_image.setPixmap(img)

        title = self.__pages.findChild((QLabel, ), 'title')
        title.setText(data['TITLE'])

        tag = self.__pages.findChild((QLabel, ), 'tag')
        tag.setText(data['TAG'])
        pass

    def create_list_page_item(self, widget, data):
        offset_x = 0
        offset_y = 0
        space = 10
        for x in data:
            label = QLabel(parent=widget)
            # img = QPixmap('./JavBus/2017-12-27\ANY-002/cover.jpg')
            img = QPixmap('./JavBus/{identifier}/cover.jpg'.format(identifier=x['IDENTIFIER']))
            label.setPixmap(img)
            label.setGeometry(QRect(offset_x, offset_y, 300, 200))
            label.setScaledContents(True)
            label.setAlignment(Qt.AlignCenter)
            label.mousePressEvent = self.list_item_click(x)
            offset_y += 200 + space

            label = QLabel(x['TITLE'], parent=widget)
            label.adjustSize()
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignCenter)
            label.setGeometry(QRect(offset_x, offset_y, 300, 50))

            offset_x += 300 + space
            offset_y -= 200 + space
            if(offset_x == 930):
                offset_x = 0
                offset_y += 250 + space
        # 按钮
        prev_btn = QPushButton('上一页', parent=widget)
        prev_btn.setGeometry(QRect(0, 520, 50, 20))
        prev_btn.clicked.connect(self.prev_page)
        next_btn = QPushButton('下一页', parent=widget)
        next_btn.setGeometry(QRect(870, 520, 50, 20))
        next_btn.clicked.connect(self.next_page)

    def back_page(self):
        self.__pages.setCurrentIndex(self.__back_page)

    def next_page(self):
        count = self.__pages.count()
        currentIndex = self.__pages.currentIndex()
        if(currentIndex + 1 < count):
            self.__pages.setCurrentIndex(currentIndex + 1)

    def prev_page(self):
        currentIndex = self.__pages.currentIndex()
        if(currentIndex - 1 >= 2):
            self.__pages.setCurrentIndex(currentIndex - 1)

    def download(self):
        pass

    def play(self):
        # ret = subprocess.Popen(["ping.exe", host], shell=True, stdout=subprocess.PIPE, cwd=)
        pass


config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'JavBus',
    'charset': 'utf8',
    'max_connection': 10,
    'min_connection': 2,
}
pool = ConnectionPool(config)
JavBus(Visitor(), pool).run()
# task = threading.Thread(target=splider)
# task.setDaemon(True)
# g = Gui()
# g.setUI()
# g.show()
