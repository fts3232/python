# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget
import sys
# pyqt5
#
# 安装：pip install PyQt5
#
# QApplication
# 
# 
# QWidget
#   resize()
#   move()

app = QApplication(sys.argv)

w = QWidget()
w.resize(250, 150)
# w.move(300, 300)
w.setWindowTitle('First PyQt5')
w.show()

sys.exit(app.exec_())