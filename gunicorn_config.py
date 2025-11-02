import os

# Railway-optimized Gunicorn configuration
bind = f"0.0.0.0:{os.environ.get('PORT', '5005')}"
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True