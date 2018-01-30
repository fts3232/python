# -*- coding: utf-8 -*-
import os
import math
import random
import glob
import numpy as np
from scipy import misc
from PIL import Image
import cv2
from pylab import *


def data_augmentation(image_files, data_num):
    return image_files


def whitening(img):
    img = img.astype(np.float32)
    w, h, d = img.shape
    num_pixels = d * w * h
    mean = img.mean()
    variance = np.mean(np.square(img)) - np.square(mean)
    stddev = np.sqrt(variance)
    min_stddev = 1.0 / np.sqrt(num_pixels)
    scale = stddev if stddev > min_stddev else min_stddev
    img -= mean
    img /= scale
    return img


# 左右翻转
def flip_left_right(image):
    return image[:, -1::-1]
    pass


# 亮度改变
def random_brightness(image, max_delta=63, seed=None):
    img = np.array(image)
    delta = np.random.uniform(-max_delta, max_delta)
    image = Image.fromarray(np.uint8(img + delta))
    return image


# 对比度改变
def random_contrast(image, lower, upper, seed=None):
    factor = np.random.uniform(-lower, upper)
    mean = (image[0] + image[1] + image[2]).astype(np.float32) / 3
    img = np.zeros(image.shape, np.float32)
    for i in range(0, 3):
        img[i] = (img[i] - mean) * factor + mean
    return img


# 画像切り抜き
def crop(image, name, crop_size, padding_size):
    (width, height, color) = image.shape
    cropped_images = []
    for i in range(0, width, padding_size):
        for j in range(0, height, padding_size):
            # left, upper, right, lower
            # box = (i, j, i + crop_size, j + crop_size)
            # cropped_name = name + '_' + str(i) + '_' + str(j) + '.jpg'
            cropped_image = image[i:i + crop_size, j:j + crop_size]
            resized_image = cv2.resize(cropped_image, (IMAGE_SIZE, IMAGE_SIZE))
            cropped_images.append(resized_image)

    return cropped_images

# image_files = ['./t-thumb.jpg']
# image_files[0] = np.asarray(Image.open('./t-thumb.jpg')).transpose(2, 0, 1)
# image_list = data_augmentation(image_files, 1000)


# # for i, image in enumerate(image_list):
# #     image = whitening(image)
# #     misc.imsave(os.path.join('./', str(i) + '.jpg'), image)
# img = array(Image.open('./t-thumb.jpg'))
# figure()
# IMAGE_SIZE = 96
# cropped_size = int(IMAGE_SIZE * 0.75)
# padding_size = IMAGE_SIZE - cropped_size
# a = crop(img, 'a.jpg', cropped_size, padding_size)
# for i, image in enumerate(a):
#     img = Image.fromarray(uint8(image))
#     img.save('./image/a-' + str(i) + '.jpg')
# image = whitening(a[0])
# img = Image.fromarray(uint8(image))
# img.save('./a.jpg')
# show()
# def load_data_from_dir(input_dir_name):
#     input_dir_list = os.listdir(input_dir_name)
#     train_list = []
#     train_count = 0
#     for dir_index, dir_name in enumerate(input_dir_list):
#         image_files = glob.glob(os.path.join(input_dir_name, dir_name, "*.jpg"))
#         print('directory:{} index:{}'.format(dir_name, dir_index))
#         for file_index, file_name in enumerate(image_files):
#             image = misc.imread(file_name)
#             label = np.int32(file_index)
#             train_list.append((dir_name, image, label))
#             train_count += 1

#         print("directory:{} total:{} train:{}".format(dir_name, train_count, train_count))
#     return train_list


# def save_dataset_numpy(data_list, image_path, label_path):
#     image_list = []
#     label_list = []
#     for _, image, label in data_list:
#         image_list.append(image)
#         label_list.append(label)

#     image_data = np.array(image_list, dtype=np.float32)
#     label_data = np.array(label_list, dtype=np.int32)

#     np.save(image_path, image_data)
#     np.save(label_path, label_data)


# data = load_data_from_dir('./image')
# save_dataset_numpy(data, './train_image.npy', './train_label.npy')

import matplotlib.pyplot as plt
from chainer.datasets import mnist
from chainer import iterators
from chainer import optimizers
from chainer.dataset import concat_examples
from chainer.cuda import to_cpu
from chainer import Chain
import chainer.functions as F
import chainer.links as L
from chainer import serializers


train, test = mnist.get_mnist(withlabel=True, ndim=1)

# # Display an example from the MNIST dataset.
# # `x` contains the inpu t image array and `t` contains that target class
# # label as an integer.
# x, t = train[0]
# plt.imshow(x.reshape(28, 28), cmap='gray')
# plt.savefig('5.png')
# print('label:', t)

# batchsize = 128

# train_iter = iterators.SerialIterator(train, batchsize)
# test_iter = iterators.SerialIterator(test, batchsize, repeat=False, shuffle=False)


class MyNetwork(Chain):

    def __init__(self, n_mid_units=100, n_out=10):
        super(MyNetwork, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, n_mid_units)
            self.l2 = L.Linear(n_mid_units, n_mid_units)
            self.l3 = L.Linear(n_mid_units, n_out)

    def __call__(self, x):
        h = F.relu(self.l1(x))
        h = F.relu(self.l2(h))
        return self.l3(h)


# model = MyNetwork()

# # Choose an optimizer algorithm
# optimizer = optimizers.MomentumSGD(lr=0.01, momentum=0.9)

# # Give the optimizer a reference to the model so that it
# # can locate the model's parameters.
# optimizer.setup(model)
# gpu_id = -1
# max_epoch = 10

# while train_iter.epoch < max_epoch:

#     # ---------- One iteration of the training loop ----------
#     train_batch = train_iter.next()
#     image_train, target_train = concat_examples(train_batch, gpu_id)

#     # Calculate the prediction of the network
#     prediction_train = model(image_train)

#     # Calculate the loss with softmax_cross_entropy
#     loss = F.softmax_cross_entropy(prediction_train, target_train)

#     # Calculate the gradients in the network
#     model.cleargrads()
#     loss.backward()

#     # Update all the trainable paremters
#     optimizer.update()
#     # --------------------- until here ---------------------

#     # Check the validation accuracy of prediction after every epoch
#     if train_iter.is_new_epoch:  # If this iteration is the final iteration of the current epoch

#         # Display the training loss
#         print('epoch:{:02d} train_loss:{:.04f} '.format(
#             train_iter.epoch, float(to_cpu(loss.data))), end='')

#         test_losses = []
#         test_accuracies = []
#         while True:
#             test_batch = test_iter.next()
#             image_test, target_test = concat_examples(test_batch, gpu_id)

#             # Forward the test data
#             prediction_test = model(image_test)

#             # Calculate the loss
#             loss_test = F.softmax_cross_entropy(prediction_test, target_test)
#             test_losses.append(to_cpu(loss_test.data))

#             # Calculate the accuracy
#             accuracy = F.accuracy(prediction_test, target_test)
#             accuracy.to_cpu()
#             test_accuracies.append(accuracy.data)

#             if test_iter.is_new_epoch:
#                 test_iter.epoch = 0
#                 test_iter.current_position = 0
#                 test_iter.is_new_epoch = False
#                 test_iter._pushed_position = None
#                 break

#         print('val_loss:{:.04f} val_accuracy:{:.04f}'.format(
#             np.mean(test_losses), np.mean(test_accuracies)))

# serializers.save_npz('my_mnist.model', model)

model = MyNetwork()

# Load the saved paremeters into the instance
serializers.load_npz('my_mnist.model', model)

# Get a test image and label
x, t = test[1]
plt.imshow(x.reshape(28, 28), cmap='gray')
plt.savefig('7.png')
print('label:', t)

print(x.shape, end=' -> ')
x = x[None, ...]
print(x.shape)

# forward calculation of the model by sending X
y = model(x)

# The result is given as Variable, then we can take a look at the contents by the attribute, .data.
y = y.data

# Look up the most probable digit number using argmax
pred_label = y.argmax(axis=1)

print('predicted label:', pred_label[0])
