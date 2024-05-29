from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django의 기본 settings 모듈을 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_data_process.settings')

# Celery 애플리케이션을 생성합니다.
app = Celery('django_data_process')

# Django settings 파일에서 Celery 관련 설정을 불러옵니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery가 Django 앱 설정을 자동으로 발견하게 합니다.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')