# -*- coding: utf-8 -*-
from PIL import Image
from pylab import *
# 添加中文字体支持
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=14)

im = array(Image.open('./data/empire.jpg').convert('L'))
print(int(im.min()), int(im.max()))
im2 = 255 - im  # invert image
print(int(im2.min()), int(im2.max()))

im3 = (100.0/255) * im + 100  # clamp to interval 100...200
print(int(im3.min()), int(im3.max()))

im4 = 255.0 * (im/255.0)**2  # squared
print(int(im4.min()), int(im4.max()))

figure()
gray()
subplot(2, 2, 1)
imshow(im)
axis('off')
title(r'$f(x)=x$')

subplot(2, 2, 2)
imshow(im2)
axis('off')
title(r'$f(x)=255-x$')

subplot(2, 2, 3)
imshow(im3)
axis('off')
title(r'$f(x)=\frac{100}{255}x+100$')

subplot(2, 2, 4)
imshow(im4)
axis('off')
title(r'$f(x)=255(\frac{x}{255})^2$')
show()
# 