import random
import os

def read_label():
    labels = {}
    with open('./trec06c-utf8/label/index') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('\n')[0]
            label = line.split(' ')[0]
            path = [ line.split(' ')[1].split('/')[2], line.split(' ')[1].split('/')[3] ]
            path = '/'.join(path)
            labels[path] = label
    return labels


def divide_set():
    labels = read_label()
    root_dir = './trec06c-utf8/data_cut/'
    filedirs = os.listdir(root_dir)
    trainset = []
    testset = []
    for filedir in filedirs:
        files = os.listdir(root_dir + filedir)
        for filename in files:
            if random.random() < 0.9:
                path = root_dir + filedir + '/' + filename
                trainset.append(path + ' ' + labels[filedir + '/' + filename] + '\n')
            else:
                path = root_dir + filedir + '/' + filename
                testset.append(path + ' ' + labels[filedir + '/' + filename] + '\n')
    with open('dataset/trainset', 'w') as f:
        f.writelines(trainset)
    with open('dataset/testset', 'w') as f:
        f.writelines(testset)


def read_set(set_dir):
    with open(set_dir) as f:
        lines = f.readlines()
        data = [ (line.split('\n')[0].split(' ')[0], line.split('\n')[0].split(' ')[1]) for line in lines]
    return data

divide_set()