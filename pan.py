from Visitor import Visitor
from bs4 import BeautifulSoup
import execjs
from PIL import Image
from pylab import *
from pytesseract import pytesseract
# import bencode 
v = Visitor()
ret = v.send_request('http://pwpan.com/fs/0c8a5i7xbi78b930/').visit()
ret = execjs.eval('"/view?module=verifyimg&action=getPcv&timestamp=" + new Date().getTime()')
v.send_request('http://pwpan.com'+ ret).download('./','code.jpg')
print(ret)
pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract"
im = Image.open('./code.jpg')
code = pytesseract.image_to_string(im,config="-psm 7 digits")
print(code)
code = code.replace(' ','')
print(code)
url = 'http://pwpan.com/file/down/caixi89/0857b7b3/' + code + '.html'
ret = v.send_request(url).visit()
print(ret)

# torrent = open('./00017122224.torrent', 'rb').read() 