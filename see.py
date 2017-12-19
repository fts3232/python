# -*- coding: utf-8 -*-
from PIL import Image
from pylab import *
# 添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)



im = array(Image.open('./data/climbing_1_small.jpg').resize((960,1280)),'f')
im2 = array(Image.open('./data/empire.jpg').resize((960,1280)),'f')
im3 = array(Image.open('./data/sunset_tree.jpg').resize((960,1280)),'f')
new_im = array((im + im2 + im3) / 3,'uint8')
imshow(new_im)
show()