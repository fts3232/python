from django.http import HttpResponse
from django.shortcuts import render
import json
import sys
sys.path.append("../")
from Mysql import ConnectionPool

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'JavBus',
    'charset': 'utf8',
    'max_connection': 10,
    'min_connection': 2,
}
pool = ConnectionPool(config)


def list(request):
    return render(request, 'index.html', content_type='text/html')


def single(request):
    return render(request, 'index.html', content_type='text/html')


def getData(request):
    p = int(request.GET['p'])
    size = int(request.GET['size'])
    db = pool.conn()
    offset = (p - 1) * size
    ret = db.select('select MOVIE_ID,TITLE,IDENTIFIER,TAG from MOVIE LIMIT {offset},{size}'.format(offset=offset, size=size))
    for x in ret:
        x['IMAGE'] = 'http://localhost:8000/static/{identifier}/cover.jpg'.format(identifier=x['IDENTIFIER'])
    db.release()
    return HttpResponse(json.dumps(ret), content_type="application/json")
