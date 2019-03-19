import sys
import os
import re
import time
from urllib.parse import urlparse
import urllib
import random
from collections import OrderedDict
from operator import itemgetter
# import extract_features


def extract_names(f):
    m = re.search(r'urls\.(\w+)\.(\w+)', f)
    if m is not None:
        return m.group(1), m.group(2), f

INPUT_PATH = './data/'
CHECK_PATH = './check/'


if not os.path.exists(INPUT_PATH):
    print >> sys.stderr, "Missing input path " + INPUT_PATH
    sys.exit(1)


if not os.path.exists(CHECK_PATH):
    print >> sys.stderr, "Missing check path " + CHECK_PATH
    sys.exit(1)


files = os.listdir(INPUT_PATH)
files = sorted(files)
names = map(extract_names, files)

# print (list(names))
f1 = './data/urls.wikipedia.examined'
f2 = './data/urls.wikipedia.general'

def get_random_url(file_path, N):
    urls = []
    with open(file_path) as file:
        for line in file:
            urls.append(line)
    random.shuffle(urls)
    return urls[:N]

def plus_one_feature(features, str):
    try:
        features[str] += 1
    except:
        features[str] = 1

def extract_features(INPUT_FILE_1, INPUT_FILE_2):
    features = dict()

    file1 = open(INPUT_FILE_1)
    file2 = open(INPUT_FILE_2)
    i = 0

    for line in file2:
        # i += 1
        # if i == 12:
        #     break
        line = line.strip('\n')
        line = urlparse(line)
        count = 0
        for segment in urllib.parse.unquote(line.path).split('/'): # urllib.parse.unquote
            if segment == '':
                continue
            if segment.isdigit():
                plus_one_feature(features, 'segment_[0-9]_{0}:1'.format(count))
            plus_one_feature(features, 'segment_len_{0}:{1}'.format(count, len(segment)))

            # if re.match(r'.+[.]\w+', segment):
            #     # print(re.findall(r'\w+[.](\w+)', segment))
            #     plus_one_feature(features, 'segment_ext_{0}:{1}'.format(count, re.findall(r'\w+[.](\w+)', segment)[0]))
            # print (segment, end=',')
            count += 1
        # try:
        #     features['segments:{0}'.format(count)] += 1
        # except:
        #     features['segments:{0}'.format(count)] = 1
        plus_one_feature(features, 'segments:{0}'.format(count))
        # print('')


    features = dict(sorted(features.items(), key=lambda x:-x[1]))
    for i in features:
        print (i, '\t', features[i], end='\n')


extract_features(f1, f2)

# string = "photo.jpg"
#
# if re.match(r'\w+[.]\w+', string):
#     print(re.findall(r'\w+[.](\w+)', string)[0])

# print(get_random_url(f1, 20))
