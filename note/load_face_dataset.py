# -*- coding: utf-8 -*-

import os
import numpy as np
from PIL import Image
import dlib
import cv2
import glob
import time
from keras.utils import np_utils


IMAGE_SIZE = 64
# 读取训练数据
images = []
labels = []

detector = dlib.get_frontal_face_detector()


# 按照指定图像大小调整尺寸
def resize_image(image, height=IMAGE_SIZE, width=IMAGE_SIZE):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w, _ = image.shape

    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    # RGB颜色
    BLACK = [0, 0, 0]

    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))


def read_path(path_name):
    for dir_item in os.listdir(path_name):
        # 从初始路径开始叠加，合并成可识别的操作路径
        full_path = os.path.abspath(os.path.join(path_name, dir_item))

        if os.path.isdir(full_path):  # 如果是文件夹，继续递归调用
            read_path(full_path)
        else:  # 文件
            if dir_item.endswith('.jpg'):
                open_img = Image.open(full_path)
                if(open_img.mode == 'RGB'):
                    dets = detector(np.array(open_img))
                    filename = os.path.splitext(dir_item)
                    for i, d in enumerate(dets):
                        cropped_img = open_img.crop((d.left(), d.top(), d.right(), d.bottom()))
                        cropped_img.thumbnail((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
                        w, h = cropped_img.size
                        p = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), (0, 0, 0))
                        offset_x = int((IMAGE_SIZE - w) / 2)
                        offset_y = int((IMAGE_SIZE - h) / 2)
                        p.paste(cropped_img, (offset_x, offset_y, w + offset_x, h + offset_y))
                        if(os.path.exists(os.path.join('../faces', os.path.basename(path_name))) is False):
                            os.mkdir(os.path.join('../faces', os.path.basename(path_name)))
                        p.save('../faces/{dirname}/{name}.jpg'.format(name=filename[0], dirname=os.path.basename(path_name)), 'JPEG', quality=100, optimize=True)

                    images.append(np.array(open_img))
                    labels.append(os.path.basename(path_name))
    return images, labels


# 从指定路径读取训练数据
def prepare_dataset(path_name):
    images, labels = read_path(path_name)

    # 将输入的所有图片转成四维数组，尺寸为(图片数量*IMAGE_SIZE*IMAGE_SIZE*3)
    # 我和闺女两个人共1200张图片，IMAGE_SIZE为64，故对我来说尺寸为1200 * 64 * 64 * 3
    # 图片为64 * 64像素,一个像素3个颜色值(RGB)
    # images = np.array(images)
    # print(images.shape)

    # # 标注数据，'me'文件夹下都是我的脸部图像，全部指定为0，另外一个文件夹下是闺女的，全部指定为1
    # labels = np.array(labels)

    return images, labels


def load_dataset(path_name):
    image_list = []
    label_list = []
    dir_list = os.listdir(path_name)
    for dir_index, dir_name in enumerate(dir_list):
        image_files = glob.glob(os.path.join(path_name, dir_name, "*.jpg"))
        image_list_count = 0
        for file_index, file_name in enumerate(image_files):
            image = np.array(Image.open(file_name))
            label = dir_index
            image_list.append(image)
            if(dir_name == '松井玲奈'):
                label = 0
            elif(dir_name == '松井珠理奈'):
                label = 1
            else:
                continue
            label_list.append(label)
            image_list_count += 1
        print("directory:{} total:{}".format(dir_name, image_list_count))

    image = np.array(image_list)
    # image = image.reshape(image.shape[0], 3, 64, 64)
    image = image.astype('float32')
    image /= 255
    label = np.array(label_list)
    label = np_utils.to_categorical(label, 2)
    return image, label


def save_dataset_numpy(data_list, image_path, label_path):
    image_list = []
    label_list = []
    for image, label in data_list:
        image_list.append(image)
        label_list.append(label)
    image_data = np.array(image_list, dtype=np.float32)
    label_data = np.array(label_list, dtype=np.int32)
    np.save(image_path, image_data)
    np.save(label_path, label_data)


# prepare_dataset('../Star')
# image, label = load_dataset('../faces')
# save_dataset_numpy(train_list, './train/data.npy', './train/label.npy')
# save_dataset_numpy(test_list, './test/data.npy', './test/label.npy')
