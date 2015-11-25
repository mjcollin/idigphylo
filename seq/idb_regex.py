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


def triplify(parsed, id_field):
    retval = []
    for k, v in parsed.iteritems():
        if k != id_field:
            retval.append((parsed[id_field], k, v))

    return retval


def read_options(opts):
    retval = {}
    retval["fn"] = opts[1]
    retval["id_field"] = opts[2]
    retval["fields"] = opts[3]
    retval["outfn"] = opts[4]
    retval["regex"] = opts[5]
    return retval

# returns [] for unmatched tuples but flatMap() throws empty lists 
# away so it's all good
def regex_find(p, triple):
    retval = []
    #matches = p.search(triple[2])
    for m in re.finditer(p, triple[2]):
        #for m in matches.groups():
            retval.append((triple[0], triple[1], triple[2], m.group(0)))
        #return triple
    return retval


if __name__ == "__main__":
    sc = SparkContext(appName="idb_regex")
    opts = read_options(sys.argv)

    #sc.setLogLevel(INFO)
    records = sc.textFile(opts["fn"])

    first_line = records.take(1)[0]
    headers = parse(first_line)    

    # filter removes header line which is going to be unique
    records = records.filter(lambda line: line != first_line)
    parsed = records.flatMap(lambda x: triplify(parse(x.encode("utf8"), headers), opts["id_field"]) )

    #p = re.compile("(http.*[ $])")
    p = re.compile(opts["regex"])
    filtered = parsed.filter(lambda triple: triple[1] in opts["fields"])
    matched = filtered.flatMap(lambda triple: regex_find(p, triple))

    #print(matched.collect())
    #matched.saveAsTextFile("hdfs://cloudera0.acis.ufl.edu:8020/user/mcollins/{0}".format(opts["outfn"]))

    # http://apache-spark-user-list.1001560.n3.nabble.com/Iterator-over-RDD-in-PySpark-td11146.$
    iter = matched._jrdd.toLocalIterator()
    output = matched._collect_iterator_through_file(iter)
    with open(opts["outfn"], "wb") as f:
        csvwriter = unicodecsv.writer(f, "excel")
        csvwriter.writerow(["id", "field", "value", "match"])
        for (id, field, value, match) in output:
            csvwriter.writerow([id, field, value, match])
