import multiprocessing

bind = '0.0.0.0:8000'  # 서버가 바인드할 주소와 포트
workers = 3  # 워커 프로세스 수
accesslog = 'gunicorn/access.log'
errorlog = 'gunicorn/error.log'
loglevel = 'info'
daemon = False
reload = True
timeout = 120  # 타임아웃 시간(초)