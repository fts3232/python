# -*- coding: utf-8 -*-
from numpy import *
# numpy
# 
# 安装：pip install numpy
# 
# img = array(Image.open(xxx))
# x,y,color = img.shape()
# 一维系x，二维系y，三维是颜色通过
# 左右翻转
#   img[:,-1::-1] 二维y轴翻转
#
# 上下翻转
#   img[-1::-1] 一维y轴翻转
#
# 颜色翻转
#   img[...,-1::-1] 三维颜色通过翻转
#   ...代表省略前面的：冒号，1个冒号代表1个维度
