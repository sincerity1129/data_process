#!/bin/bash
# Gunicorn을 백그라운드에서 실행합니다
gunicorn --config gunicorn/config.py django_data_process.wsgi &

# Gunicorn의 프로세스 ID를 기록합니다
echo $! > gunicorn/gunicorn.pid
echo "Gunicorn started with PID $(cat gunicorn/gunicorn.pid)"