# coding: utf-8

import sys
import re
import random
from urllib.parse import urlparse
import urllib
# you may add imports if needed (and if they are installed)


def plus_one(features, name):
    try:
        features[name] += 1
    except:
        features[name] = 1

def get_random_url(file_path, N):
    urls = []
    with open(file_path) as f:
        for line in f:
            urls.append(line)
    random.shuffle(urls)
    return urls[:N]

def add_features(features, urls):
    for line in urls:
        line = line.strip('\n')
        line = urlparse(line)
        index = 0
        for segment in urllib.parse.unquote(line.path).split('/'):
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

            index += 1

        plus_one(features, 'segments:{0}'.format(index))

def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):
    N = 1000
    alpha = 0.1
    min_count = N * alpha

    features = dict()

    file1 = open(INPUT_FILE_1)
    file2 = open(INPUT_FILE_2)

    add_features(features, get_random_url(INPUT_FILE_1, N))
    add_features(features, get_random_url(INPUT_FILE_2, N))

    features = dict(sorted(features.items(), key=lambda x:-x[1]))

    with open(OUTPUT_FILE, 'w') as out:
        for i in features:
            if features[i] > min_count:
                out.write(str(i)+'\t'+str(features[i])+'\n')
    # print >> sys.stderr, "Not implemented"
