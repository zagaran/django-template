from django.utils import timezone

from common.models import TaskMonitor
from config.celery import app


@app.task
def update_task_monitor():
    # Update task monitor to current time
    TaskMonitor.objects.update_or_create(defaults={"last_run": timezone.now()})