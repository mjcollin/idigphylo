from celery import Celery
from subprocess import call
import sys

app = Celery('tasks', broker='amqp://idigphylo:idppass9@elk.acis.ufl.edu//')

@app.task
def add(x, y):
    return x + y

def run(fn):
    '''Execute MrBayes script
    '''
    call("bin/mb {0}".format(fn), shell=True)
    

if __name__ == "__main__":
    run(sys.argv[1])
