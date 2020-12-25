#!/usr/bin/env python

import os
import bisect
from datetime import datetime

result = []


def log_analyze(location, keyword):
    results = []
    for root, dir, files in os.walk(location):

        for one_file in files:
            filename = os.path.join(root, one_file)
            items = parse_one_file(filename, keyword)
            if not items:
                continue
            for item in items:
                log_time, line = item
                sort_keys = [one[0] for one in results]
                index = bisect.bisect_left(sort_keys, log_time)
                results.insert(index, (log_time, line, one_file, filename))
        # print(os.path.join(root, files[0]))

    for one_item in results:
        print(one_item[3] + ":")
        print(one_item[1])


def parse_one_file(filename, keyword):
    try:
        with open(filename) as f:
            for line in f.readlines():
                if keyword in line:
                    log_time = None
                    if 'ip=' in line:
                        # for access log
                        log_time = (line.split("ip=", 1)[0]).strip()
                    else:
                        log_time = (line.split("|", 1)[0])

                    the_log_time = datetime.strptime(log_time, "%m-%d-%Y %H:%M:%S.%f")

                    if log_time is None:
                        continue
                    yield (the_log_time, line)
    except Exception as r:
        pass
        # print("can't parse file:" + filename)


if __name__ == '__main__':
    import sys

    location = sys.argv[1]
    keyword = sys.argv[2]
    log_analyze(location, keyword)
