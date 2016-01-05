import json

from flask import Flask

app = Flask(__name__)
content_type_json = {'Content-Type': 'text/css; charset=utf-8'}

# Celery conf
from celery import Celery
from celery.signals import worker_ready
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_TIMEZONE'] = 'Australia/Melbourne'

# execute task at certain intervals
from datetime import timedelta
from celery.schedules import crontab
app.config['CELERYBEAT_SCHEDULE'] = {
    # test task at 5 s intervals
    'pause-every-5-seconds': {
        'task': 'tasks.constant_task',
        'schedule': timedelta(seconds=5)
    },
    'play-every-morning': {
        'task': 'tasks.morning_task',
        'schedule': crontab(hour=8, minute=0)
    },
    'play-repeatedly-during-day': {
        'task': 'tasks.worktime_task',
        # 9:00 - 17:00 every 5 minutes
        # day_of_week - Sunday = 0 and Saturday = 6
        'schedule': crontab(hour='9-18', minute='*/1', day_of_week='1-5')
    },
}

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(name='tasks.constant_task')
def constant_task():
    print('ping')

@celery.task(name='tasks.morning_task')
def morning_task():
    print('good morning')

@celery.task(name='tasks.worktime_task')
def worktime_task():
    print('work work')

# optional task to run on startup, no matter what
@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
         sender.app.send_task('tasks.constant_task', connection=conn)

# Routes for manual controls
############################

@app.route('/')
def hello_world():
    msg = 'Device: <a href="/play">play</a> or <a href="/pause">pause</a>.'
    return msg

@app.route('/play')
def get_play():
    #play_task.delay()
    return 'Playing! <a href="/">back</a>'

@app.route('/pause')
def get_pause():
    #pause_task.delay()
    return 'Pausing! <a href="/">back</a>'

if __name__ == '__main__':
    try:
        # try the production run
        app.run(host='0.0.0.0', port=80)
    except PermissionError:
        # we're probably on the developer's machine
        app.run(host='0.0.0.0', port=5000, debug=True)
