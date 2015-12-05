from __future__ import absolute_import
import sys
sys.path.append("../lib")
sys.path.append("../workers")

from flask import Flask, jsonify
from database import Database, Sequence, Result
from align.align import pipeline

import idigbio


app = Flask(__name__)

@app.route('/tree/build', methods=["GET", "POST"])
def tree_build():
    opts = {}
    # Hardcoded options, potentially expose
    opts["data_file"] = "data.nex"
    opts["seq_type"] = "dna"
    opts["fields"] = ["uuid"]
    opts["sort"] = ["uuid"]

    opts["rq"] = {"genus": "acer"}
    opts["limit"] = 10

    idb = idigbio.json()
    results = idb.search_records(rq=opts["rq"], limit=opts["limit"], 
                                 fields=opts["fields"], sort=opts["sort"])

    idb_uuids = []
    for rec in results["items"]:
        idb_uuids.append(rec["indexTerms"]["uuid"])

    db = Database()
    opts["raw_seqs"] = {}
    for seq in db.sess.query(Sequence).filter(Sequence.idb_uuid.in_(idb_uuids)):
        # The "-" char messes up MrBayes even in the taxon name string field.
        # Change that here and it will percolate through the output without
        # affecting the data sources on the front end.
        opts["raw_seqs"][seq.idb_uuid.replace("-", "_")] = seq.seq

    pipeline.delay(opts)
    return jsonify({"return": True})

@app.route('/tree/view/<string:job_id>')
def tree_view(job_id, methods=["GET", "POST"]):
    return jsonify({"job_id": job_id})

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)


