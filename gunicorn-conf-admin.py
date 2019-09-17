import os

accesslog = '-'
bind = "0.0.0.0:{port!s}".format(port=os.environ["ADMIN_PORT"])
loglevel = os.environ["LOG_LEVEL"]
