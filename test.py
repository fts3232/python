# import base64
import urllib
help(urllib.parse)
# '''
# 人脸查找——识别
# '''

# request_url = "https://aip.baidubce.com/rest/2.0/face/v2/identify"

# f = open('../faces2/范冰冰/未标题-2.jpg', 'rb')
# # 参数images：图像base64编码
# img1 = base64.b64encode(f.read())
# # 二进制方式打开图文件
# f = open('../faces2/范冰冰/u=1025625741,3359753935&fm=27&gp=0.jpg', 'rb')
# # 参数images：图像base64编码
# img2 = base64.b64encode(f.read())

# params = {"face_top_num": "1", "group_id": "test_group_2", "images": str(img1) + ',' + str(img2), "user_top_num": "1"}
# params = bytes(urllib.parse.urlencode(params), encoding='utf8')

# access_token = '[调用鉴权接口获取的token]'
# request_url = request_url + "?access_token=" + access_token
# request = urllib.request(url=request_url, data=params)
# request.add_header('Content-Type', 'application/x-www-form-urlencoded')
# response = request.urlopen(request)
# content = response.read()
# if content:
#     print(content)
