import os
import math
import difflib


def findMovie(roots, filename, suffix=None):
    if(type(roots) == str):
        roots = [roots]
    ratio = 0
    data = None
    for root in roots:
        for path in os.listdir(root):
            if((filename.lower() in path.lower() or filename.lower().replace('-', '') in path.lower()) or filename.lower() in root.lower()):
                temp = os.path.join(root, path)
                if(os.path.isfile(temp) and os.path.splitext(temp)[1].lower() in suffix):
                    path_ratio = math.ceil(difflib.SequenceMatcher(None, path, filename).quick_ratio() * 100)
                    if(path_ratio > ratio):
                        ratio = path_ratio
                        data = temp
                elif(os.path.isdir(temp)):
                    return findMovie(temp, filename, suffix)
    return data
