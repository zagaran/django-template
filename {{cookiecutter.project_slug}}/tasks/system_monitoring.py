from django.utils import timezone

{%- if cookiecutter.sentry != "enabled" %}
from common.models import TaskMonitor
{%- else %}
from common.models import User
{%- endif %}
from config.celery import app


@app.task
def update_task_monitor():
    {%- if cookiecutter.sentry == "enabled" %}
    # Auto-instrumented cron monitor hook for worker server downtime detection
    # Just run any query to check db access
    User.objects.exists()
    {%- else %}
    # Update task monitor to current time
    TaskMonitor.objects.update_or_create(defaults={"last_run": timezone.now()})
    {%- endif %}