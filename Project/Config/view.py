from django.http import HttpResponse
from django.shortcuts import render
import json
import sys
import os
import re
import subprocess
sys.path.append("../")
from Mysql import ConnectionPool
from JavBus import JavBus
from Visitor import Visitor

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'JavBus',
    'charset': 'utf8',
    'max_connection': 20,
    'min_connection': 2,
}
pool = ConnectionPool(config)


def list(request):
    return render(request, 'index.html', content_type='text/html')


def findMovie(root, filename):
    returnData = False
    for path in os.listdir(root):
        if(filename.lower() in path.lower() or filename.lower().replace('-', '') in path.lower()):
            temp = "{root}/{path}".format(root=root, path=path)
            ret = os.path.splitext(temp)
            if(os.path.isfile(temp) and ret[1].lower() in ['.avi', '.mp4']):
                path = path.replace('(', '^(')
                path = path.replace(')', '^)')
                subprocess.Popen([path], shell=True, stdout=subprocess.PIPE, cwd=root)
                returnData = True
                break
            elif(os.path.isdir(temp)):
                returnData = findMovie(temp, filename)
    return returnData


def play(request):
    identifier = str(request.GET['identifier'])
    ret = findMovie('E:/迅雷下载', identifier)
    msg = '播放成功' if(ret is True) else '播放失败'
    ret = {'msg': msg, 'status': ret}
    return HttpResponse(json.dumps(ret), content_type="application/json")


def search(request):
    pass


def scan(request):
    root = 'E:/迅雷下载'
    identifiers = []
    for path in os.listdir(root):
        temp = "{root}/{path}".format(root=root, path=path)
        ret = os.path.splitext(temp)
        if((os.path.isfile(temp) and ret[1].lower() in ['.avi', '.mp4']) or os.path.isdir(temp)):
            ret = re.search('([A-Za-z]{2,})-?(\d{2,})', path)
            if(ret is not None):
                num = ret.group(2)
                if(len(num) >= 5):
                    num = num.replace('00', '')
                identifiers.append("{series}-{num}".format(series=ret.group(1), num=num))
    # JavBus(Visitor(), pool).search(identifiers)
    ret = {'msg': '1', 'status': False, 'list':identifiers}
    return HttpResponse(json.dumps(ret), content_type="application/json")


def getData(request):
    p = int(request.GET['p'])
    size = int(request.GET['size'])
    db = pool.conn()
    offset = (p - 1) * size
    ret = db.select('select MOVIE_ID,TITLE,IDENTIFIER,TAG from MOVIE LIMIT {offset},{size}'.format(offset=offset, size=size))
    for x in ret:
        path = '../JavBus/{identifier}'.format(identifier=x['IDENTIFIER'])
        sample = []
        x['LINK'] = []
        x['IMAGE'] = ''
        links = db.select('select LINK,PUBLISH_TIME from DOWNLOAD_LINK where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': x['MOVIE_ID']})
        for link in links:
            link['PUBLISH_TIME'] = str(link['PUBLISH_TIME'])
            x['LINK'].append(link)
        if(os.path.isdir(path)):
            for file in os.listdir(path):
                if(file != 'cover.jpg'):
                    sample.append("http://localhost:8000/static/{dir}/{file}".format(file=file, dir=x['IDENTIFIER']))
            x['IMAGE'] = 'http://localhost:8000/static/{identifier}/cover.jpg'.format(identifier=x['IDENTIFIER'])
        x["SAMPLE"] = sample
    db.release()
    return HttpResponse(json.dumps(ret), content_type="application/json")
