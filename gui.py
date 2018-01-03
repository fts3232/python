# -*- coding: utf-8 -*-
from appJar import gui
from JavBus import JavBus
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

i = 1


def my_print(message):
    app.setTextArea('message', '{message}\n'.format(message=message)).config(bottom=0)


def press(button):
    global i
    i+=1
    my_print(i)
    # obj = JavBus(Visitor(), ConnectionPool(config), my_print)
    # task = threading.Thread(target=obj.run)
    # task.setDaemon(True)
    # task.start()


app = gui('title', '400x400')
app.setIcon('./favicon.ico')
app.setSticky("ews")
app.setExpand("both")
app.setPadding([20, 20])  # 20 pixels padding outside the widget [X, Y]
# app.setInPadding([0, 0]) # 20 pixels padding inside the widget [X, Y]
app.addScrolledTextArea('message', row=1, column=1, rowspan=2)
app.addButton("启动", press, row=2, column=2)
help(gui)
# app.setLabelBg("l1", "red")
# app.setLabelBg("l2", "blue")
# app.setLabelBg("l4", "green")
# app.setLabelBg("l6", "orange")
# app.setLabelBg("l7", "yellow")
# app.setBg("orange")
# app.setFont(18)
# app.addLabel("title", "Welcome to appJar")
# app.setLabelBg("title", "red")
# app.addLabelEntry("Username")
# app.setFocus("Username")
# app.addLabelSecretEntry("Password")
# app.addButtons(["Submit", "Cancel"], press)
# app.addButtons(["启动", "暂停"], press)
# app.addButtons(["←", "→"], press)
app.go()
