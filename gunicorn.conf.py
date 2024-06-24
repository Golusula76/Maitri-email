# Gunicorn configuration file
bind = "0.0.0.0:10000"
workers = 2
worker_class = "gevent"
timeout = 60
keepalive = 5