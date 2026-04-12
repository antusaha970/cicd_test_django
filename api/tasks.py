from celery import shared_task
from .models import Counter


@shared_task
def increment_counter():
    """
    Celery task to increment the counter value by 1.
    This task is scheduled to run every 30 seconds via Celery Beat.
    """
    # Get or create the counter instance
    counter, created = Counter.objects.get_or_create(id=1)
    
    # Increment the counter
    counter.value += 1
    counter.save()
    
    return f"Counter incremented to {counter.value}"
