# -*- coding: utf-8 -*-
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.models import load_model
from load_face_dataset import load_dataset
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# 导入皮马印第安人糖尿病数据集. 它描述了病人医疗记录和他们是否在五年内发病。
images, labels = load_dataset('../faces')
# 8个输入变量 1个输出变量，最后一列为输出 1为出现糖尿病，0为未出现
X = images  # 输入
Y = labels  # 输出
# model = Sequential()
# model.add(Conv2D(64, (3, 3), padding='same', input_shape=(64, 64, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))

# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Conv2D(32, (3, 3), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.25))

# model.add(Flatten())  # 13 Flatten层
# model.add(Dense(128, activation='relu'))  # 14 Dense层,又被称作全连接层

# model.add(Dropout(0.5))  # 16 Dropout层
# model.add(Dense(2, activation='softmax'))  # 17 Dense层
# sgd = SGD(lr=0.005, decay=1e-6, momentum=0.9, nesterov=True)  # 采用SGD+momentum的优化器进行训练，首先生成一个优化器对象
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
# model.fit(X, Y, epochs=60, batch_size=10)
# model.save('./image.h5')
model = load_model('./image.h5')
# model.fit(X, Y, epochs=60, batch_size=10)
# model.save('./image.h5')
# # evaluate the model
# scores = model.evaluate(X, Y)
# print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
# exit()
# calculate predictions
images, labels = load_dataset('../faces2')
X = images
predictions = model.predict_classes(X)
proba = model.predict_proba(X)
# round predictions
for i, x in enumerate(predictions):
    print(int(proba[i][x] * 100))
