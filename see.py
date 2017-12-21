# -*- coding: utf-8 -*-
from PIL import Image
from pylab import *
import os
import pickle
from scipy.ndimage import filters
import sift
# 添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)


def get_imlist(path):
    filelist = os.listdir(path)
    result = []
    for f in filelist:
        if(f.endswith('.jpg')):
            result.append(os.path.join(path, f))
    return result


def pca(X):
    """    Principal Component Analysis
        input: X, matrix with training data stored as flattened arrays in rows
        return: projection matrix (with important dimensions first), variance and mean.
    """

    # get dimensions
    num_data, dim = X.shape

    # center data
    mean_X = X.mean(axis=0)
    X = X - mean_X

    if dim > num_data:
        # PCA - compact trick used
        M = dot(X, X.T)  # covariance matrix
        e, EV = linalg.eigh(M)  # eigenvalues and eigenvectors
        tmp = dot(X.T, EV).T  # this is the compact trick
        V = tmp[::-1]  # reverse since last eigenvectors are the ones we want
        S = sqrt(e)[::-1]  # reverse since eigenvalues are in increasing order
        for i in range(V.shape[1]):
            V[:, i] /= S
    else:
        # PCA - SVD used
        U, S, V = linalg.svd(X)
        V = V[:num_data]  # only makes sense to return the first num_data

    # return the projection matrix, the variance and the mean
    return V, S, mean_X


# imlist = get_imlist('./data/a_thumbs')
# im = array(Image.open(imlist[0]))  # open one image to get the size
# m, n = im.shape[:2]  # get the size of the images
# imnbr = len(imlist)  # get the number of images
# print("The number of images is %d" % imnbr)
# immatrix = []
# for imname in imlist:
#     immatrix.append(array(Image.open(imname)).flatten())
# immatrix = array(immatrix, 'f')
# V, S, immean = pca(immatrix)
# figure()
# gray()
# subplot(2, 4, 1)
# axis('off')
# imshow(immean.reshape(m, n))
# for i in range(7):
#     subplot(2, 4, i+2)
#     imshow(V[i].reshape(m, n))
#     axis('off')
# f = open('./data/font_pca_modes.pkl', 'wb+')
# pickle.dump(immean,f)
# pickle.dump(V,f)
# f.close()

def gaussian_filter(im, blur):
    im2 = zeros(im.shape)
    if(len(im.shape) == 2):
        im2 = filters.gaussian_filter(im, blur)
    else:
        for i in range(len(im.shape)):
            im2[:, :, i] = filters.gaussian_filter(im[:, :, i], blur)
    im2 = np.uint8(im2)
    return im2

imname = './data/empire.jpg'
im = array(Image.open(imname).convert('L'))
sift.process_image(imname, 'empire.sift')
l1, d1 = sift.read_features_from_file('empire.sift')

figure()
gray()
subplot(131)
sift.plot_features(im, l1, circle=False)
title(u'SIFT特征',fontproperties=font)
subplot(132)
sift.plot_features(im, l1, circle=True)
title(u'用圆圈表示SIFT特征尺度',fontproperties=font)


# for bi, blur in enumerate([2, 5, 10]):
#   im2 = zeros(im.shape)
#   im2 = filters.gaussian_filter(im, blur)
#   im2 = np.uint8(im2)
#   imNum=str(blur)
#   subplot(1, 4, 2 + bi)
#   axis('off')
#   title(u'标准差为'+imNum, fontproperties=font)
#   imshow(im2)
show()
