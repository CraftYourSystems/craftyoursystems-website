# gunicorn.conf.py — Production server configuration
# Run with: gunicorn -c gunicorn.conf.py app:app

import os

# Number of worker processes
# Formula: (2 × CPU cores) + 1   — good starting point
workers = int(os.getenv('GUNICORN_WORKERS', 3))

# Worker type — sync is fine for this API
worker_class = 'sync'

# Bind to all interfaces on port 5000
# On Railway/Render, use the PORT env variable they provide
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Restart workers after 1000 requests (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = '-'   # stdout
errorlog  = '-'   # stderr
loglevel  = 'info'

# Timeout: kill a worker if it hangs for >30 seconds
timeout = 30
