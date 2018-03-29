# -*- coding:utf-8 -*-
import os
import re
import json
import random
from dataset import read_set

trainset = read_set('dataset/trainset')


def train(sample_rate=1):
    labels = {}
    y_prob = {}
    for line in trainset:
        if random.random() > sample_rate:
            continue
        path = line[0]
        label = line[1]
        if not label in labels.keys():
            labels[label] = {}
        with open(path, encoding='utf-8') as f:
            text = f.read()
            regex = u'[\u4E00-\u9FA5]+'
            pattern = re.compile(regex)
            words = re.findall(pattern, text)
            regex = u'http'
            pattern = re.compile(regex)
            http_words = re.findall(pattern, text)
            words += http_words
            regex = u'From.*@.*'
            pattern = re.compile(regex, re.I)
            from_text = re.findall(pattern, text)
            if len(from_text) != 0:
                mails = from_text[0].split('@')[-1].split('>')[0].split(' ')[0]
                words.append(mails)
            for word in words:
                if not word in labels[label].keys():
                    labels[label][word] = 1
                else:
                    labels[label][word] += 1
    for label, word_dict in labels.items():
        totalNum = 0
        for num in word_dict.values():
            totalNum += num
        y_prob[label] = totalNum

    with open('train_result/y', 'w') as f:
        json.dump(y_prob, f, ensure_ascii=False, indent=2)

    with open('train_result/x_cond_y', 'w') as f:
        json.dump(labels, f, ensure_ascii=False, indent=2)


train(sample_rate=1)