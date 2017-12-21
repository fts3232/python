# -*- coding: utf-8 -*-
from scipy.ndimage import filters
# scipy.ndimage
# 
# 安装：pip install scipy
# 
# fgaussian_filter() 高斯模糊
# 
# def gaussian_filter(im, blur):
#     im2 = zeros(im.shape)
#     if(len(im.shape) == 2):
#         im2 = filters.gaussian_filter(im, blur)
#     else:
#         for i in range(len(im.shape)):
#             im2[:, :, i] = filters.gaussian_filter(im[:, :, i], blur)
#     im2 = np.uint8(im2)
#     return im2