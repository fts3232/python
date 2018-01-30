# -*- coding: utf-8 -*-
import dlib
import cv2
from PIL import Image
from pylab import *
# dlib
#
# 安装：pip install dlib
# 需要安装cmake和boost
img = cv2.imread('t.jpg')
open_img = Image.open('t.jpg')
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
dets = detector(img)
figure()
print("人脸数：", len(dets))
# 输出人脸矩形的四个坐标点
for i, d in enumerate(dets):
    print("第", i, "个人脸d的坐标：",
          "left:", d.left(),
          "right:", d.right(),
          "top:", d.top(),
          "bottom:", d.bottom())
    shape = predictor(img, d)
    for i in range(68):
        pt = shape.part(i)
        # plot(pt.x, pt.y, 'r.')
    cropped_img = open_img.crop((d.left(), d.top(), d.right(), d.bottom()))
    cropped_img = cropped_img.resize((96, 96)).save('./t-thumb.jpg', 'JPEG', quality=100, optimize=True)
    # cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), (55, 255, 155), 2)

# ...省略所有的冒号来用省略号,-1代表最后一个维度 ::-1 翻转
# imshow(img[..., -1::-1])
imshow(cropped_img)
show()
