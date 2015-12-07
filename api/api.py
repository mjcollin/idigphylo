from __future__ import absolute_import

import sys
from subprocess import call, check_output
sys.path.append("../lib")
sys.path.append("../workers")

from flask import Flask, request, jsonify, send_file
import idigbio
import uuid
from database import Database, Sequence, Result
from align.align import pipeline


app = Flask(__name__)

@app.route('/tree/build', methods=["GET", "POST"])
def tree_build():
    opts = {}
    # Hardcoded options, potentially expose
    opts["data_file"] = "data.nex"
    opts["seq_type"] = "dna"
    opts["fields"] = ["uuid"]
    opts["sort"] = ["uuid"]

    opts["rq"] = request.args.get("rq")
    opts["limit"] = request.args.get("limit", 10)

    # Generate a uuid job id
    opts["job_id"] = str(uuid.uuid4())

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
    return jsonify({"job_id": opts["job_id"]})

@app.route('/tree/view/<string:job_id>')
def tree_view(job_id, methods=["GET", "POST"]):
    db = Database()
    trees = db.sess.query(Result).\
            filter(Result.job_id==job_id).\
            filter(Result.prog=="mrbayes").first()

    if trees is not None:
        return jsonify({"job_id": job_id, "tree": trees.result, "status":"done"})
    else:
        return jsonify({"job_id": job_id, "tree": "", "status": "pending"})

@app.route('/tree/render/<string:job_id>')
def tree_render(job_id, methods=["GET", "POST"]):
    out_fn = "/tmp/image.svg"

    db = Database()
    trees = db.sess.query(Result).\
            filter(Result.job_id==job_id).\
            filter(Result.prog=="mrbayes").first()
    aligned = db.sess.query(Result).\
              filter(Result.job_id==job_id).\
              filter(Result.prog=="clustalo").first()

    if trees is not None:  
        # Convert NEXUS tree to Newick format with BioPerl script, was the only 
        # thing I could find that would parse a MrBayes tree file.
        t = check_output("echo '{0}' | /usr/bin/bp_nexus2nh".format(trees.result), shell=True)
        s = aligned.result

        # Create tree, have to use a process call to run PhyloTree.render()
        # inside an X framebuffer since it uses Qt4 to render.
        # https://github.com/jhcepas/ete/issues/101
        call("/usr/bin/xvfb-run bin/ete_render.py '{0}' '{1}' '{2}'".format(t, s, out_fn), shell=True)
                
        return send_file(out_fn)

    else:
        return jsonify({"status":False})

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)


