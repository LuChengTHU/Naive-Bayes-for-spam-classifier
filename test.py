import os
import json
import re
import math
from dataset import read_set


testset = read_set('dataset/testset')


with open('train_result/y') as f:
    y_prob = json.load(f)

with open('train_result/x_cond_y') as f:
    x_cond_y_prob = json.load(f)

total_y_num = 0
for y in y_prob.keys():
    total_y_num += y_prob[y]


def test(laplace_lambda=1, little_prob=1e-100, is_laplace=True):
    true_num = 0
    total_num = 0
    for line in testset:
        path = line[0]
        true_label = line[1]
        max_prob = -math.inf
        label = ''
        for y in y_prob.keys():
            prob = math.log(float(y_prob[y]) / float(total_y_num))
            with open(path, encoding='utf-8') as f:
                text = f.read()
                regex = u'[\u4E00-\u9FA5]+'
                pattern = re.compile(regex)
                words = re.findall(pattern, text)
                regex = u'http'
                pattern = re.compile(regex)
                http_words = re.findall(pattern, text)
                for i in range(50):
                    words += http_words
                regex = u'From.*@.*'
                pattern = re.compile(regex, re.I)
                from_text = re.findall(pattern, text)
                if len(from_text) != 0:
                    mails = from_text[0].split('@')[-1].split('>')[0].split(' ')[0]
                    for i in range(50):
                        words.append(mails)
                for word in words:
                    if not word in x_cond_y_prob[y].keys():
                        if is_laplace:
                            prob += math.log(1.0 * laplace_lambda / (y_prob[y] + laplace_lambda * len(words)))
                        else:
                            prob += math.log(little_prob)
                    else:
                        prob += math.log(float(x_cond_y_prob[y][word]) / float(y_prob[y]))

            if prob > max_prob:
                max_prob = prob
                label = y
        total_num += 1
        if label == true_label:
            true_num += 1
    acc = float(true_num) / float(total_num)
    print('acc: ', acc)
    return acc



def draw_laplace():
    lap_prob = {}
    little = {}

    for i in range(-50, 51):
        prob = float('1e%d' % i)
        lap_acc = test(laplace_lambda=prob, little_prob=prob, is_laplace=True)
        little_acc = test(laplace_lambda=prob, little_prob=prob, is_laplace=False)
        lap_prob[i] = lap_acc
        little[i] = little_acc
        print(i)

    with open('lap', 'w') as f:
        json.dump(lap_prob, f, indent=2)

    with open('little', 'w') as f:
        json.dump(little, f, indent=2)


test(is_laplace=False)

