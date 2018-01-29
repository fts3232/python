# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from chainer import Variable, optimizers, serializers
import chainer.functions as F
import chainer.links as L
# Chainer
# 
# 安装：pip install Chainer
# 
a = Variable(np.array([3], dtype=np.float32))
b = Variable(np.array([4], dtype=np.float32))
c = a**2 + b**2
print("a.data: {0}, b.data: {1}, c.data: {2}".format(a.data, b.data, c.data))
c.backward()
print("dc/da = {0}, dc/db = {1}, dc/dc = {2}".format(a.grad, b.grad, c.grad))

linear_function = L.Linear(1,1)