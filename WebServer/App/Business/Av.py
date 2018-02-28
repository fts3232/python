import os
import re
import math
import difflib
from Model.Av import Av as AvModel


class Av():

    __config = {}

    def __init__(self, config):
        self.__config = config
        pass

    def getData(self, options):
        model = AvModel()
        ret = model.getMovie(options)
        for x in ret:
            # 可否播放
            storage_path = self.__config['storage_path']
            path = os.path.join(storage_path, x['IDENTIFIER'])
            x['PLAY'] = True if(self.scanLocalFolder(x['IDENTIFIER']) is not False) else False
            # 发布时间
            x['PUBLISH_TIME'] = x['PUBLISH_TIME'].strftime('%Y-%m-%d')
            # 下载链接
            links = model.getDownloadLink(x['MOVIE_ID'])
            x['LINK'] = []
            for link in links:
                link['PUBLISH_TIME'] = str(link['PUBLISH_TIME'])
                x['LINK'].append(link)
            # 封面图
            x['IMAGE'] = False
            if(os.path.isfile(os.path.join(path, 'cover.jpg'))):
                x['IMAGE'] = True
            # 分类
            if(x['TAG'] != '' and x['TAG'] is not None):
                tags = model.getTag(x['TAG'])
                x['TAG'] = tags
            # 演员
            if(x['STAR'] != '' and x['STAR'] is not None):
                x['STAR'] = model.getStar(x['STAR'])
            # 样本图链接
            samples = model.getSample(x['MOVIE_ID'])
            x["SAMPLE"] = samples
        return ret

    def scanLocalFolder(self, identifier=None, roots=None):
        data = {}
        if(roots is None):
            roots = self.__config['roots']
        elif(isinstance(roots, str)):
            roots = [roots]
        # 遍历指定的目录
        for root in roots:
            # 判断目录是否存在
            if(os.path.exists(root) is False):
                continue
            # 列出目录下所有文件和文件夹，并按创建时间降序排序
            paths = os.listdir(root)
            paths = sorted(paths, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
            # 遍历
            for path in paths:
                # 获取文件名和后缀
                tempPath = os.path.join(root, path)
                # 判断是否文件
                isFile = os.path.isfile(tempPath)
                if(isFile):
                    (filename, suffix) = os.path.splitext(path)
                else:
                    filename = path

                # 忽略不是匹配后缀的文件
                if(isFile and suffix.lower() not in self.__config['suffix']):
                    continue
                # 忽略名字不匹配的项
                if(identifier is not None and identifier.lower().replace('-', '') not in filename.lower().replace('-', '') and identifier.lower().replace('-', '') not in root.lower().replace('-', '')):
                    continue
                # 如果identifier未指定，按正则匹配，获取identifier
                if(identifier is None):
                    ret = re.findall('([A-Za-z]{2,})-?(\d{3,4})(-\d+)?', path)
                    if(len(ret) == 0):
                        continue
                    ret = ret[-1]
                    num = ret[1]
                    if(len(num) >= 4 and num[0] == '0' and ret[0] != 'heyzo'):
                        num = num[1:]
                    if(ret[2] != ''):
                        tempIdentifier = "{series}-{num}-{extra}".format(series=ret[0], num=num, extra=ret[2][1:])
                    else:
                        tempIdentifier = "{series}-{num}".format(series=ret[0], num=num)
                    ret = re.findall('\d{6,}', path)
                    if(len(ret) > 0):
                        tempIdentifier = path
                # identifier
                else:
                    tempIdentifier = identifier
                # 如果是文件，向列表添加内容
                if(isFile):
                    # 获取文件名匹配程度，取最高的那个
                    ratio = math.ceil(difflib.SequenceMatcher(None, tempIdentifier, filename).quick_ratio() * 100)
                    ret = {'path': tempPath, 'filename': filename, 'suffix': suffix, 'identifier': tempIdentifier, 'ratio': ratio}
                    if(tempIdentifier not in data or ratio > data[tempIdentifier]['ratio']):
                        data[tempIdentifier] = ret
                # 如果是文件夹，合拼2个列表
                else:
                    ret = self.scanLocalFolder(tempIdentifier, tempPath)
                    if(ret):
                        for key in ret:
                            if(key not in data or ret[key]['ratio'] > data[key]['ratio']):
                                data[key] = ret[key]
        if(len(data) == 0):
            data = False
        return data

    def getTag(self):
        tag = AvModel().getAllTag()
        return tag
