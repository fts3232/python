# -*- coding: utf-8 -*-
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# 导入皮马印第安人糖尿病数据集. 它描述了病人医疗记录和他们是否在五年内发病。
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# 8个输入变量 1个输出变量，最后一列为输出 1为出现糖尿病，0为未出现
X = dataset[:, 0:8]  # 输入
Y = dataset[:, 8]  # 输出
# model = Sequential()
# # 全连接层使用 Dense 定义
# # 第一个参数为神经元数量，input_dim为输出神经元的数量，kernel_initializer 定义权重的初始化方法, activation 参数定义激活函数
# # 权重初始化方法
# #   一个服从均匀分布的小随机数（init='uniform'）,在0到0.05直接（这是 Keras 标准均匀分布权重初始值）。
# #   另一种传统的选择是‘normal’,会从高斯分布（正态分布）中产生一个小的随机数。
# # 激活函数
# #   输出层使用 Sigmoid 函数来确保网络输出在 0 和 1 之间,
# model.add(Dense(12, input_dim=8, kernel_initializer='uniform', activation='relu'))
# model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
# model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
# # Compile model
# #   loss 损失函数
# #   optimizer 优化器 adam：一种高效地默认方法
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# # Fit the model
# # 填充数据
# # epochs 迭代的次数
# # batch_size 批处理大小，每个batch包含的样本数
# model.fit(X, Y, epochs=150, batch_size=10)
# model.save('./pima-indians-diabetes.h5')
model = load_model('./pima-indians-diabetes.h5')
# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
# calculate predictions
predictions = model.predict(X)
# round predictions
# for i, x in enumerate(predictions):
#     print(round(x[0]))
