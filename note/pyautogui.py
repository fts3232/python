# -*- coding: utf-8 -*-
import pyautogui
# pyautogui
# 
# 安装：pip install pyautogui
# 
# pyautogui.FAILSAFE = True 鼠标光标在屏幕左上角，中断PyAutoGUI函数
# pyautogui.PAUSE 延迟时间
# pyautogui.size() 获取屏幕分辨率
# pyautogui.click(x,y,duration,button='left',clicks,interval) 在x,y坐标点击，持续时间为duration,按键为button,点击次数为clicks,2次点击停留时间为interval
# pyautogui.moveTo(x,y,duration) 绝对坐标移动到x,y，持续时间为duration
# pyautogui.moveRel(x,y,duration) 相对当前坐标移动x,y，持续时间为duration
# pyautogui.posistion() 获取鼠标当前位置
# pyautogui.scroll(clicks) 鼠标滚轮滚动clicks， clicks为正往上滚，clicks为负往下滚。
# pyautogui.dragTo(x,y,duration) 绝对坐标拖动到x,y，持续时间为duration
# pyautogui.dragRel(x,y,duration) 相对当前坐标拖动x,y，持续时间为duration
# pyautogui.screenshot(imageFilename,region) 屏幕截图，保存文件的路径为imageFilename，截取的开始坐标为regiosn[0],regiosn[1],宽度为regiosn[2],高度为regiosn[3]
# pyautogui.typewrite(message,interval) 键盘输入message,每个字符的间隔为interval,messsage为[]可输入特殊键['enter', 'a', 'b', 'left', 'left', 'X', 'Y']
# pyautogui.keyDown(key) 按下key
# pyautogui.keyUp(key) 松开key
# pyautogui.press(key) 按下，并松开key
# pyautogui.hotkey() 热键组合
# pyautogui.alert(text) 显示带有一段消息和一个确认按钮的警告框
# pyautogui.confirm(text) 显示带有一段消息以及确认按钮和取消按钮的对话框
# pyautogui.prompt(text) 显示可提示用户输入的对话框
# 