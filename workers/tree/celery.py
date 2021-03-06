from __future__ import absolute_import

from celery import Celery

app = Celery('tree',
             broker='amqp://idigphylo:idppass9@elk.acis.ufl.edu//',
             include=['tree.tree'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ROUTES = {"tree.tree.pipeline": {"queue": "tree"}}
)

if __name__ == '__main__':
    app.start()
