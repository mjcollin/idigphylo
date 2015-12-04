from __future__ import absolute_import

import sys
import os
sys.path.append("../../lib")
sys.path.append("../lib")

import tempfile
from database import Database, Result
from align.celery import app
from subprocess import call
from textwrap import fill

from tree.tree import pipeline as next_pipeline


# API is outside directory so the import statement there will result in the
# below app name
@app.task(name="align.align.msa")
def msa(opts):
    fn = setup(opts)
    run(fn)
    save(fn)
    opts["aligned_seqs"] = load(fn)

    #FIXME
    #cleanup(fn)

    return opts

def load(fn):
    """Load the resulting FASTA file into a dict
    """
    out_fn = "{0}.out".format(fn)
    seqs = {}
    with open(out_fn, "r") as out:
        k = ""
        v = ""
        for l in out:
            if l[0] == ">":
                if len(v) > 0:
                    seqs[k] = v
                    k = ""
                    v = ""
                k = l[1:].strip()
            else:
                v += l.strip()
        seqs[k] = v
    return seqs

@app.task(name="align.align.pipeline")
def pipeline(opts):
    opts = msa(opts)
    next_pipeline.delay(opts)

def run(fn):
    '''Execute ClustalOmega alignment
    '''
    cwd = os.getcwd()
    os.chdir(os.path.dirname(fn))
    out_fn = "{0}.out".format(fn)
    with open("{0}.stdout".format(fn), "w") as out:
        retval = call("{0}/align/bin/clustalo -i {1} -o {2} --force".format(cwd, fn, out_fn),
                      shell=True, stdout=out)
    
    os.chdir(cwd)
    return retval == 0

def save(fn):
    '''Save the resulting alignment in fasta to the MySQL database
    '''
    with open("{0}.out".format(fn), "r") as fasta_file:
        file_text = fasta_file.read()
    db = Database()
    result = Result(job_id = "asdf",
                    prog = "clustalo",
                    result = file_text,
                    timestamp = db.mk_time()
                    )
    db.sess.add(result)
    db.sess.commit()

def setup(opts):
    temp_dir = tempfile.mkdtemp(prefix="idigphylo.clustalo.")
    seq_fn = "{0}/{1}".format(temp_dir, "seqs.fasta")

    # Write sequence data file in FASTA format
    with open(seq_fn, "w") as seq_file:
        for k, v in opts["raw_seqs"].iteritems():
            wrapped = fill(v, 60)
            seq_file.write(">{0}\n{1}\n".format(k, wrapped))
    
    return seq_fn


if __name__ == "__main__":

    # This is now broken due to the celery relative import path align.celery
    # Now need to run this file with celery
    cwd = os.getcwd()
    try:
        fn = sys.argv[1] 
    except IndexError:
        fn = "{0}/test/primates.fasta".format(cwd)

    print("Running test with test data {0}, this may take a minute...".format(fn))
    print run(fn)
    save(fn)
