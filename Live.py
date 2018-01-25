import time
import os
import re
import pickle
from Visitor import Visitor


class Live():
    'live'
    __hosts = [
        'http://www.huya.com/zhaoxiaochou',
        'http://www.huya.com/2183499048',
        'http://www.huya.com/a16789',
        # 'https://www.douyu.com/aleng1106',
        'https://www.douyu.com/196',
        'https://www.douyu.com/asmr',
        'https://www.douyu.com/tao15',
        'https://www.douyu.com/xiaojiujiu',
        'https://www.douyu.com/109064',
        'https://www.douyu.com/220149',
        'https://www.douyu.com/3107374',
        'https://www.douyu.com/2168715',
        'https://www.douyu.com/feimagine',
        'https://www.douyu.com/xiaoleilei',
        'https://www.douyu.com/32892',
        'https://www.douyu.com/78561',
        'https://www.douyu.com/67373',
        'https://www.douyu.com/292081',
        'https://www.douyu.com/3507497',
        'https://www.douyu.com/306774',
        'https://www.douyu.com/213841',
    ]
    # vistor类
    __visitor = None

    def __init__(self):
        self.__visitor = Visitor()

    def run(self):
        #while 1:
        print('开始爬取数据...')
        if(os.path.exists('./host.pkl') is not True):
            live_list = {}
        else:
            fo = open('./host.pkl', 'rb+')
            ret = fo.read()
            live_list = pickle.loads(ret)
        for host in self.__hosts:
            body = self.__visitor.send_request(host).visit()
            if('huya' in host):
                # 房间信息
                room_data = re.findall(r' var TT_ROOM_DATA = (.+?);', body)
                room_data = room_data[0].replace('true', 'True')
                room_data = room_data.replace('false', 'False')
                room_data = room_data.replace('null', 'None')
                room_data = eval(room_data)
                # 主播信息
                profile_info = re.findall(r'var TT_PROFILE_INFO = (.+?);', body)
                profile_info = eval(profile_info[0])
                if(room_data['state'] == 'ON'):
                    state = '正在直播'
                elif(room_data['state'] == 'REPLAY'):
                    state = '回播'
                else:
                    state = '未在直播'
                nickname = profile_info['nick']
                title = room_data['introduction']
                category = room_data['gameFullName']
                screenshot = room_data['screenshot']
            elif('douyu' in host):
                room_data = re.findall(r'var \$ROOM = ({.+?});', body)
                room_data = room_data[0].replace('true', 'True')
                room_data = room_data.replace('false', 'False')
                room_data = room_data.replace('null', 'None')
                room_data = eval(room_data)
                title = room_data['room_name']
                screenshot = room_data['room_pic']
                nickname = room_data['owner_name']
                category = room_data['second_lvl_name']
                state = '正在直播'if room_data['show_status'] == 1 else '未在直播'
            elif('panda' in host):
                # room_data = re.findall(r'window._config_roominfo = ({[\s\S]+?});', body)
                # print(room_data)
                # exit()
                pass
            elif('longzhu' in host):
                # soup = BeautifulSoup(body, "html.parser")
                # room_data = re.findall(r'var roomInfo = (.+?);', body)
                # room_data = room_data[0].replace('true', 'True')
                # room_data = room_data.replace('false', 'False')
                # room_data = room_data.replace('null', 'None')
                # room_data = eval(room_data)
                # title = ''
                # screenshot = ''
                # nickname = room_data['Name']
                # exit()
                pass
            live_list[host] = {'nickname': nickname, 'state': state, 'title': title, 'category': category, 'screenshot': screenshot}
            print("{nickname} {state} 分类：{category} 标题：{title} 封面：{screenshot}".format(nickname=nickname, state=state, title=title, category=category, screenshot=screenshot))
        fo = open('./host.pkl', 'wb+')
        fo.write(pickle.dumps(live_list))
        print('结束...')
        #time.sleep(60)


Live().run()
