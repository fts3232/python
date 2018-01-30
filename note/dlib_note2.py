# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from PIL import Image
import dlib
import cv2


# 读取训练数据
images = []
labels = []

detector = dlib.get_frontal_face_detector()


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
                        cropped_img = cropped_img.resize((96, 96)).save('../faces/{name}.jpg'.format(name=filename[0]), 'JPEG', quality=100, optimize=True)

                    images.append(np.array(open_img))
                    labels.append(filename[0])
    return images, labels


# 从指定路径读取训练数据
def load_dataset(path_name):
    images, labels = read_path(path_name)

    # 将输入的所有图片转成四维数组，尺寸为(图片数量*IMAGE_SIZE*IMAGE_SIZE*3)
    # 我和闺女两个人共1200张图片，IMAGE_SIZE为64，故对我来说尺寸为1200 * 64 * 64 * 3
    # 图片为64 * 64像素,一个像素3个颜色值(RGB)
    images = np.array(images)
    # print(images.shape)

    # # 标注数据，'me'文件夹下都是我的脸部图像，全部指定为0，另外一个文件夹下是闺女的，全部指定为1
    labels = np.array(labels)

    return images, labels


# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         print("Usage:%s path_name\r\n" % (sys.argv[0]))
#     else:
#         images, labels = load_dataset(sys.argv[1])
images, labels = load_dataset('../Star')
print(images.shape,labels.shape)
