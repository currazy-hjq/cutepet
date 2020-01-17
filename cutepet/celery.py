from celery import Celery
from django.conf import settings
import os


#为了celery设置环境变量
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'cutepet.settings'
)

#创建应用  初始化celery
app = Celery('cutepet')
app.conf.update(
    broker_url = 'redis://@127.0.0.1:6379/1',
)
# app.conf.update(
#     broker_url = 'redis://:123456@111.229.46.201:6379/1',
# )


app.autodiscover_tasks(settings.INSTALLED_APPS)