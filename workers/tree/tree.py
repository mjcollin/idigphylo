from __future__ import absolute_import

import sys
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
    fn = setup(opts)
    #run(fn)
    #save(fn)
    #cleanup(fn)

def run(fn):
    '''Execute MrBayes script
    '''
    processors = 8

    with open("{0}.stdout".format(fn), "w") as out:
        retval = call("mpirun -np {0} bin/mb {1}".format(processors, fn),
                      shell=True, stdout=out)
    
    return retval == 0

def save(fn):
    '''Save the resulting tree in .nex format to the MySQL database
    '''
    with open("{0}.con.tre".format(fn), "r") as tree_file:
        file_text = tree_file.read()
    db = Database()
    result = Result(job_id = "asdf",
                             result = file_text,
                             timestamp = db.mk_time()
                            )
    db.sess.add(result)
    db.sess.commit()

def setup(opts):
    # Template .nex file that contains the run instructions
    nex_file_template = """BEGIN mrbayes;
        log start filename=run.log;                [log output for analysis to a text file]
        set autoclose=yes nowarn=yes;                   [this is needed to run in batch mode]

[Primates example from manual]
        execute {data_file};
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

    temp_dir = tempfile.mkdtemp(prefix="idigphylo.")
    fn = "{0}/{1}".format(temp_dir, "run.nex")

    with open(fn, "w") as run_file:
        run_file.write(nex_file_template.format(**opts))   

    return fn


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
