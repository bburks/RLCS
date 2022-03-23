import csv

# writes a csv containing row1, dataList at the given path

def export(row1, dataList, path):

    width = len(row1)
    dataListHeight = len(dataList)
    dataListWidth = len(dataList[0])

    assert width == dataListWidth, "wrong number of labels"

    for i, row in enumerate(dataList):
        assert dataListWidth == len(row), f'wrong number of elements in row {i}'

    with open(f'{path}.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(row1)
        for row in dataList:
            writer.writerow(row)

# inputs a CSV and outputs [col1, row1, dataList]

def extract(path):
    dataList = []
    col1 = []
    with open(f'{path}.csv', newline = '') as file:
        reader = csv.reader(file)

        for i, nextRow in enumerate(reader):
            dataList.append([])
            for j, data in enumerate(nextRow):
                if j == 0:
                    col1.append(data)
                else:
                    dataList[i].append(data)


    return [col1, dataList]

# writes a one-line csv

def export_line(row, path):
    with open(path + '.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(row)

# pulls info from a one-line csv

def extract_line(path):
    with open(path +'.csv', newline = '') as file:
        reader = csv.reader(file)
        firstRow = next(reader)
    return firstRow

# writes a two-line csv from a list of pairs

def export_pairs(pairs, path):
    labels = []
    values = []
    with open(f'{path}.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        for pair in pairs:
            labels.append(pair[0])
            values.append(pair[1])
        writer.writerow(labels)
        writer.writerow(values)

# collates a two-line csv into a list of pairs

def extract_pairs(path):
    pairs = []
    with open(f'{path}.csv', newline = '') as file:
        reader = csv.reader(file)
        labels = next(reader)
        values = next(reader)
    for (label, value) in zip(labels, values):
        pairs.append((label, value))
    return pairs

# writes one

def export_one(elem, path):
    with open(f'{path}.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        row = [elem]
        writer.writerow(row)

# returns one

def extract_one(path):
    with open(f'{path}.csv', newline = '') as file:
        reader = csv.reader(file)
        [elem] = next(reader)
    return elem

def transpose(dataList):
    return list(map(list, zip(*dataList)))
