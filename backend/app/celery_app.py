from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    # Celery Beat schedule
    celery.conf.beat_schedule = {
        'schedule-notifications': {
            'task': 'tasks.schedule_notifications',
            'schedule': crontab(minute='*'),  # Run every minute
        },
    }
    celery.conf.timezone = 'UTC'
    return celery