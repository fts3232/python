import os
import difflib
import math


def diff(str1, str2):
    match = 0
    match_str = []
    if(len(str1) != len(str2)):
        length = max(len(str1), len(str2))
        min_str = str2 if(len(str1) > len(str2)) else str1
        max_str = str1 if(len(str1) > len(str2)) else str2
        first_index = 0
        match_index =0
        for i, v1 in enumerate(min_str):
            for j, v2 in enumerate(max_str[first_index:]):
                if((match_index ==0 and v2==v1) or (match_index + 1 == i and v2==v1)):
                    first_index = j+1
                    match += 1
                    match_index = i
                    break;
                elif(v2==v1):
                    first_index = j+1
                    match += 0.5
                    match_index = i
                    break;
    else:
        length = len(str1)
        for i, v in enumerate(str1):
            if(v == str2[i]):
                match += 1
    return match / length * 100


def find(roots, filename, suffix=None):
    if(type(roots) == str):
        roots = [roots]
    ratio = 0
    data = None
    for root in roots:
        for path in os.listdir(root):
            # path_ratio = diff(path,filename)
            path_ratio = math.ceil(difflib.SequenceMatcher(None, path, filename).quick_ratio() * 100)
            if(((suffix != None and os.path.isfile(os.path.join(root,path)) and os.path.splitext(path)[1] in suffix) or suffix == None or os.path.isdir(os.path.join(root,path))) and path_ratio > ratio):
                ratio = path_ratio
                data = os.path.join(root,path)
    if(data is not None and os.path.isdir(data)):
        return find(data, filename, suffix)
    else:
        return data

print(find(['D:\wamp\www', 'E:\wamp64\www'], 'est', ['.html']))
