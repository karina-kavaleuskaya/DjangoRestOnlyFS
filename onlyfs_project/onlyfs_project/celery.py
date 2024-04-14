import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlyfs_project.settings')

app = Celery('onlyfs_project')
app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule ={
    'client_orders': {
        'task': 'only_app.task.check_order_and_send_mails',
        'schedule': crontab(minute="*/1")
    },
    'generate_sales_report': {
        'task': 'only_app.task.generate_sales_report',
        'schedule': crontab(day_of_month='1', hour='0', minute='0')
    },
}
