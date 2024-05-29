#!/bin/bash

# gunicorn.pid 파일이 있는지 확인합니다
if [ -f gunicorn//gunicorn.pid ]; then
    # PID를 읽고 프로세스를 종료합니다
    PID=$(cat gunicorn/gunicorn.pid)
    echo "Stopping Gunicorn with PID $PID"
    kill $PID
    
    # 프로세스가 종료될 때까지 잠시 대기합니다
    sleep 1
    
    # PID 파일을 삭제합니다
    rm gunicorn/gunicorn.pid
    echo "Gunicorn stopped"
else
    echo "No gunicorn.pid file found. Gunicorn may not be running."
fi