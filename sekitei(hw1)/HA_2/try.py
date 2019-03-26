# coding: utf-8


import sys
import os
import re
import random
import time
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
import urlparse
import urllib
import numpy as np


def plus_one(features, str):
    try:
        features[str] += 1
    except:
        features[str] = 1

def add_feature(features, line):
    line = line.strip('\n')
    line = urlparse.urlparse(line)
    index = 0
    for segment in urllib.unquote(line.path).split('/'):
        if segment == '':
            continue

        plus_one(features, 'segment_name_{0}:{1}'.format(index, segment))
        plus_one(features, 'segment_len_{0}:{1}'.format(index, len(segment)))

        if segment.isdigit():
            plus_one(features, 'segment_[0-9]_{0}:1'.format(index))
        if re.match(r'[^\d]+\d+[^\d]', segment):
            plus_one(features, 'segment_substr[0-9]_{0}:1'.format(index))
        if re.match(r'.+[.]\w+', segment):
            ext = re.findall(r'.+[.](\w+)', segment)[0]
            plus_one(features, 'segment_ext_{0}:{1}'.format(index, ext))
        if re.match(r'[^\d]+\d+[^\d]', segment) and re.match(r'.+[.]\w+', segment):
            ext = re.findall(r'.+[.](\w+)', segment)[0]
            plus_one(features, 'segment_ext_substr[0-9]_{0}:{1}'.format(index, ext))

        index += 1

    plus_one(features, 'segments:{0}'.format(index))

    parameters = urllib.unquote(line.params).split('&')
    if parameters[0] != '':
        for param in parameters:
            plus_one(features, 'param:{0}'.format(param))
            plus_one(features, 'param_name:{0}'.format(param.split('=')[0]))

def extract_features(all_features, url_features, urls):
    for url in urls:
        features = Counter()
        add_feature(features, url)
        all_features += features
        url_features.append(features)
    return all_features

def extract_useful_features(all_features, N, alpha=0.03):
    for key, value in list(all_features.items()):
        if value <= N*alpha:
            del all_features[key]
    return all_features

def make_features_matrix(all_features, url_features):
    X = np.zeros((len(url_features), len(all_features)))
    for i, _ in enumerate(url_features):
        for j, key in enumerate(all_features.keys()):
            X[i][j] += url_features[i][key]
    return X

def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    url_features = []
    all_features = Counter()
    num = len(QLINK_URLS) + len(UNKNOWN_URLS)

    all_features = extract_features(all_features, url_features, QLINK_URLS)
    all_features = extract_features(all_features, url_features, UNKNOWN_URLS)

    all_features = extract_useful_features(all_features, num)

    X = np.zeros((len(url_features), len(all_features)))
    X = make_features_matrix(all_features, url_features)

    clust = KMeans(10, init='k-means++', max_iter=300, n_jobs=-1)
    clust.fit(X)
    label = clust.predict(X)

    # clf = LogisticRegression(solver='lbfgs', multi_class='multinomial').fit(X, label)

    unique, counts = np.unique(label[:len(QLINK_URLS)], return_counts=True)
    x_qlinks = dict(zip(unique, counts))
    # for i in x_qlinks:
    #     print(str(i)+'\t'+str(x_qlinks[i]))

    # print("////")
    # unique, counts = np.unique(label[len(QLINK_URLS):], return_counts=True)
    # x_unklinks = dict(zip(unique, counts))
    # for i in x_qlinks:
    #     print(str(i)+'\t'+str(x_unkinks[i]))

    quota_cluster = np.zeros(10).astype(int)
    for i in x_qlinks:
        quota_cluster[i] = int(float(x_qlinks[i]) / len(QLINK_URLS) * QUOTA)
        # print(quota_cluster[i], " ", x_qlinks[i])


    # for i in all_features:
        # print(str(i)+'\t'+str(all_features[i]))
    # print "define_segments is not implemented";


#
# returns True if need to fetch url
#
def fetch_url(url):
    #global sekitei
    #return sekitei.fetch_url(url);
    return True;

f1 = './data/urls.zr.examined'
f2 = './data/urls.zr.general'

def get_random_url(file_path, N):
    urls = []
    with open(file_path) as file:
        for line in file:
            urls.append(line)
    random.shuffle(urls)
    return urls[:N]

define_segments(get_random_url(f1, 500), get_random_url(f2, 500), 1000)
