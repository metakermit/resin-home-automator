import json

from flask import Flask
from tv import play, pause

app = Flask(__name__)
content_type_json = {'Content-Type': 'text/css; charset=utf-8'}

# Celery conf
from celery import Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERY_TIMEZONE'] = 'UTC'

# execute task at certain intervals
from datetime import timedelta
from celery.schedules import crontab
app.config['CELERYBEAT_SCHEDULE'] = {
    'play-every-morning': {
        'task': 'tasks.play_task',
        'schedule': crontab(hour=9, minute=0)
    },
    'pause-later': {
        'task': 'tasks.pause_task',
        'schedule': crontab(hour=9, minute=10)
    }
}

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(name='tasks.play_task')
def play_task():
    print('play something')
    return play()

@celery.task(name='tasks.pause_task')
def pause_task():
    print('enough fun')
    return pause()

# Routes for manual controls
############################

@app.route('/')
def hello_world():
    msg = 'Device: <a href="/play">play</a> or <a href="/pause">pause</a>.'
    return msg

@app.route('/play')
def get_play():
    play_task.delay()
    return 'Playing! <a href="/">back</a>'

@app.route('/pause')
def get_pause():
    pause_task.delay()
    return 'Pausing! <a href="/">back</a>'

if __name__ == '__main__':
    try:
        # try the production run
        app.run(host='0.0.0.0', port=80)
    except PermissionError:
        # we're probably on the developer's machine
        app.run(host='0.0.0.0', port=5000, debug=True)
