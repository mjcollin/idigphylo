import sys
sys.path.append("../../lib")

import db
from celery import Celery
from subprocess import call

app = Celery('tasks', broker='amqp://idigphylo:idppass9@elk.acis.ufl.edu//')

@app.task
def add(x, y):
    return x + y


def save(fn):
    '''Save the resulting tree in .nex format to the MySQL database
    '''
    pass



def run(fn):
    '''Execute MrBayes script
    '''
    with open("{0}.stdout".format(fn), "w") as out:
        retval = call("bin/mb {0}".format(fn), shell=True, stdout=out)
    
    return retval == 0


if __name__ == "__main__":

    try:
        fn = sys.argv[1] 
    except IndexError:
        fn = "test/run.nex"

    print("Running test with test data {0}, this may take a minute...".format(fn))
    print run(fn)
