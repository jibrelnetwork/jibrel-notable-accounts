import os

accesslog = '-'
access_log_format = '%t [ID:%{request-id}i] [RA:%a] [PID:%P] [C:%s] [S:%b] [T:%D] [HT:%{host}i] [R:%r]'
bind = "0.0.0.0:{port!s}".format(port=os.environ["API_PORT"])
loglevel = os.environ["LOG_LEVEL"]
worker_class = 'aiohttp.worker.GunicornWebWorker'
workers = int(os.environ["GUNICORN_WORKERS"])
