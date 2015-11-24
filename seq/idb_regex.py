from __future__ import print_function
import os
import sys
import re
import unicodecsv
from pyspark import SparkContext
from operator import add
import csv
import StringIO

def parse(str, headers=None):
    if headers is not None:
        retval = {}
    else:
        retval = []

    try:

        b = StringIO.StringIO(str)
        r = csv.reader(b)

        for line in r:
            i = 0
            for value in line:
                if headers:
                    retval[ headers[i] ] = value
                else:
                    retval.append(value)
                i += 1
    except Exception as e:
        with open("/tmp/rejects", "a") as f:
            f.write("PROBLEM WITH: {0}\n".format(str))

        # assume we're parsing a line and not the headers
        for h in headers:
            retval[h] = ""

        raise e

    return retval


def triplify(parsed):
    id_field = "first:field"

    retval = []
    for k, v in parsed.iteritems():
        if k != id_field:
            retval.append((k, parsed[id_field], v))

    return retval



if __name__ == "__main__":
    sc = SparkContext(appName="idb_regex")

    #sc.setLogLevel(INFO)
    fn = sys.argv[1]
    records = sc.textFile(fn)

    first_line = records.take(1)[0]
    headers = parse(first_line)    

    # filter removes header line which is going to be unique
    records = records.filter(lambda line: line != first_line)
    parsed = records.flatMap(lambda x: triplify(parse(x.encode("utf8"), headers)) )

    filtered = parsed.filter(lambda triple: triple[0] == "second")

    print(filtered.collect())
