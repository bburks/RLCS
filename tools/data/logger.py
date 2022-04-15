from . import csv_handler as csv
from ..helper import transpose, mkdir
import os



def log(object, path):
    if isinstance(object, dict):
        mkdir(f'{path}/')
        keys = object.keys()
        for key in object:
            value = object[key]
            log(value, f'{path}/{key}')
    elif isinstance(object, list):
        mkdir(f'{path}/')
        log(len(object), f'{path}/count')
        for i, elem in enumerate(object):
            log(elem, f'{path}/{i}')
    else:
        csv.export_one(object, path)

def unlog(path):
    res = dict()
    paths = os.listdir(path = path)

    for next_path in paths:
        if next_path.endswith('.csv'):
            file = next_path[:-4]
            data = csv.extract_one(f'{path}/{file}')
            if file == 'count':
                count = int(data)
                data = []
                for i in range(count):
                    next = unlog(f'{path}/{i}')
                    data.append(next)
                res = data
            else:
                try:
                    data = int(data)
                except:
                    pass
                res[file] = data
        else:
            try:
                int(next_path)
            except:
                data = unlog(f'{path}/{next_path}')
                try:
                    data = int(data)
                except:
                    pass
                res[next_path] = data
    return res

def log_summary(obj, path):
    assert isinstance(obj, list)
    dataList = []
    for i, info in enumerate(obj):
        assert isinstance(info, dict)
        if i == 0:
            keys = list(info.keys())
            labels = keys
        data = []
        for key in keys:
            data.append(info[key])
        dataList.append(data)

    #dataList = transpose(dataList)
    print(dataList)
    csv.export(labels, dataList, path)
