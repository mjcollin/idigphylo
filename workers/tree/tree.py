import sys
sys.path.append("../../lib")

import database
from celery import Celery
from subprocess import call

app = Celery('tasks', broker='amqp://idigphylo:idppass9@elk.acis.ufl.edu//')

@app.task
def add(x, y):
    return x + y


def save(fn):
    '''Save the resulting tree in .nex format to the MySQL database
    '''
    with open("{0}.con.tre".format(fn), "r") as tree_file:
        file_text = tree_file.read()
    db = database.Database()
    result = database.Result(job_id = "asdf",
                             result = file_text,
                             timestamp = db.mk_time()
                            )
    db.sess.add(result)
    db.sess.commit()

def run(fn):
    '''Execute MrBayes script
    '''
    processors = 8

    with open("{0}.stdout".format(fn), "w") as out:
        retval = call("mpirun -np {0} bin/mb {1}".format(processors, fn),
                      shell=True, stdout=out)
    
    return retval == 0


if __name__ == "__main__":

    try:
        fn = sys.argv[1] 
    except IndexError:
        fn = "test/run.nex"

    print("Running test with test data {0}, this may take a minute...".format(fn))
    print run(fn)
    save(fn)
