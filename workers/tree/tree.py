from __future__ import absolute_import

import sys
import os
sys.path.append("../../lib")
sys.path.append("../lib")

import tempfile
from database import Database, Result
from tree.celery import app
from subprocess import call


# API is outside directory so the import statement there will result in the
# below app name
@app.task(name="tree.tree.build")
def build(opts):
    # Only for mk_time, connections pooled so not a total disaster
    db = Database()
    start_time = db.mk_time()
    fn = setup(opts)
    run(fn)
    save(fn, opts["job_id"], start_time)
    #FIXME
    #cleanup(fn)

@app.task(name="tree.tree.pipeline")
def pipeline(opts):
    build(opts)

def run(fn):
    '''Execute MrBayes script
    '''
    processors = 8

    cwd = os.getcwd()
    os.chdir(os.path.dirname(fn))
    with open("{0}.stdout".format(fn), "w") as out:
        retval = call("mpirun -np {0} {1}/tree/bin/mb {2}".format(processors, cwd, fn),
                      shell=True, stdout=out)
    
    os.chdir(cwd)
    return retval == 0

def save(fn, job_id, start_time):
    '''Save the resulting tree in .nex format to the MySQL database
    '''
    with open("{0}.con.tre".format(fn), "r") as tree_file:
        file_text = tree_file.read()
    db = Database()
    result = Result(job_id = job_id,
                    prog = "mrbayes",
                             result = file_text,
                             timestamp = db.mk_time(),
                             starttime = start_time
                            )
    db.sess.add(result)
    db.sess.commit()

def setup(opts):
    # Template .nex file that contains the run instructions
    run_file_template = """BEGIN mrbayes;
        log start filename=run.log;                [log output for analysis to a text file]
        set autoclose=yes nowarn=yes;                   [this is needed to run in batch mode]

[Primates example from manual]
        execute data.nex;
        lset nst=6 rates=invgamma;
        mcmc ngen=20000
                samplefreq=100
                printfreq=100
                diagnfreq=1000
                filename=run.nex;
        sump filename=run.nex;
        sumt filename=run.nex;
END;
"""

    data_file_template = """#NEXUS
BEGIN data;
    dimensions ntax={seq_count} nchar={seq_length};
    format datatype={seq_type} interleave=no gap=-;
    matrix
    {seq_lines}
;
END;
"""

    temp_dir = tempfile.mkdtemp(prefix="idigphylo.")
    run_fn = "{0}/{1}".format(temp_dir, "run.nex")
    data_fn = "{0}/{1}".format(temp_dir, "data.nex")

    # Job control file
    with open(run_fn, "w") as run_file:
        run_file.write(run_file_template.format(**opts))   

    # Sequence data file 
    opts["seq_lines"] = ""
    for k, v in opts["aligned_seqs"].iteritems():
        opts["seq_lines"] += "{0}	{1}\n".format(k, v)
        # Could use a check here to make sure everything is the same length
        # Otherwise this is a wasteful reassignment
        opts["seq_length"] = len(v)
    opts["seq_count"] = len(opts["aligned_seqs"])
    with open(data_fn, "w") as data_file:
        data_file.write(data_file_template.format(**opts))   
    
    # Consider returning dir name instead of file name?
    # That means we'll hard code the "run.nex" in a lot of places though
    return run_fn


if __name__ == "__main__":

    # This is now broken due to the celery relative import path tree.celery
    # Now need to run this file with celery
    try:
        fn = sys.argv[1] 
    except IndexError:
        fn = "test/run.nex"

    print("Running test with test data {0}, this may take a minute...".format(fn))
    print run(fn)
    save(fn)
