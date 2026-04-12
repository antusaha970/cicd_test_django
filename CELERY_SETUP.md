# Celery & Celery Beat Setup Guide

This Django project uses Celery and Celery Beat to automatically increment a counter every 30 seconds.

## Architecture Overview

- **Django**: Web framework
- **Celery**: Distributed task queue
- **Celery Beat**: Task scheduler
- **Redis**: Message broker and result backend

## Prerequisites

1. Redis server must be installed and running
2. Python virtual environment with required packages

## Installation

1. Install the required packages:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Make sure Redis is running:

```bash
redis-cli ping
# Should return: PONG
```

## Running the Application

You need to start **three separate processes**:

### 1. Start Celery Worker

The worker executes the tasks:

```bash
source venv/bin/activate
celery -A config worker --loglevel=info
```

### 2. Start Celery Beat (in a new terminal)

The beat scheduler sends tasks to the worker every 30 seconds:

```bash
source venv/bin/activate
celery -A config beat --loglevel=info
```

### 3. Start Django Development Server (in a new terminal)

```bash
source venv/bin/activate
python manage.py runserver
```

## Accessing the Application

- **Home Page**: http://127.0.0.1:8000/
- **Live Counter Page**: http://127.0.0.1:8000/counter/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

## How It Works

1. **Celery Beat** sends a task message every 30 seconds to the Redis broker
2. **Celery Worker** picks up the task from Redis and executes it
3. The task increments the counter value in the database
4. The **counter page** auto-refreshes every 5 seconds to show the latest value
5. You can see the counter increasing in real-time!

## Files Added/Modified

### New Files:

- `config/celery.py` - Celery app configuration
- `api/tasks.py` - Celery task definitions
- `templates/counter.html` - Counter page template

### Modified Files:

- `requirements.txt` - Added celery and redis packages
- `config/__init__.py` - Import celery app
- `config/settings.py` - Added Celery configuration
- `api/models.py` - Added Counter model
- `api/views.py` - Added counter_page view
- `config/urls.py` - Added counter URL route
- `templates/home.html` - Added link to counter page

## Celery Configuration

In `config/settings.py`:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'increment-counter-every-30-seconds': {
        'task': 'api.tasks.increment_counter',
        'schedule': 30.0,  # 30 seconds
    },
}
```

## Troubleshooting

### Celery worker not receiving tasks

- Make sure Redis is running: `redis-cli ping`
- Check if worker is connected to the correct broker
- Clear Redis and restart: `redis-cli FLUSHDB`

### Counter not incrementing

- Check Celery Beat logs to see if tasks are being sent
- Check Celery Worker logs to see if tasks are being executed
- Verify the database migration was applied: `python manage.py migrate`

### Connection errors

- Ensure Redis server is running on port 6379
- Check firewall settings if Redis is on a different machine

## Production Considerations

For production deployment:

1. Use a more robust broker like RabbitMQ or Redis Sentinel
2. Run Celery workers as systemd services
3. Use flower for monitoring: `celery -A config flower`
4. Configure proper logging
5. Set up proper error handling and task retries
6. Use environment variables for configuration

## Monitoring

You can monitor Celery tasks using:

- Worker logs (terminal output)
- Django admin panel (view Counter model)
- Flower (optional): `pip install flower && celery -A config flower`
