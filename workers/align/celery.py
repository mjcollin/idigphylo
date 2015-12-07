from __future__ import absolute_import

from celery import Celery

app = Celery('align',
             broker='amqp://idigphylo:idppass9@elk.acis.ufl.edu//',
             include=['align.align'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ROUTES = {"align.align.pipeline": {"queue": "align"}}
)

if __name__ == '__main__':
    app.start()
