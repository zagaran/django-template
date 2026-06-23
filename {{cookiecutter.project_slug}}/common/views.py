from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.http.response import HttpResponse
{%- if cookiecutter.celery == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE celery
{%- endif %}
from datetime import timedelta
from django.utils import timezone
{%- if cookiecutter.sentry != "enabled" %}
from common.models import TaskMonitor
{%- endif %}
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE celery
{%- endif %}
{%- endif %}

from common.mixins import PermissionRequiredMixin
from common.permissions import Permission


class IndexView(TemplateView):
    template_name = "common/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().get(request, *args, **kwargs)


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("index")


class RobotsTxtView(View):

    def get(self, request):
        if settings.PRODUCTION:
            # Allow all (note that a blank Disallow block means "allow all")
            lines = ["User-agent: *", "Disallow:"]
        else:
            # Block all
            lines = ["User-agent: *", "Disallow: /"]
        return HttpResponse("\n".join(lines), content_type="text/plain")
{%- if cookiecutter.reference_examples == "on" %}
{%- if cookiecutter.django_react == "enabled" %}


{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE django_react
{%- endif %}
class DjangoReactView(PermissionRequiredMixin, TemplateView):
    # TODO: delete me; this is just a reference example
    permission_required = Permission.dashboard
    template_name = 'common/sample_django_react.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hello_msg'] = 'Component'
        context['sample_props'] = {'msg': 'sample props'}
        return context
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_react
{%- endif %}
{%- endif %}
{%- endif %}
{%- if cookiecutter.celery == "enabled" and cookiecutter.sentry != "enabled" %}


{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE celery
{%- endif %}

class TaskMonitorView(View):
    """View for uptime monitoring of task framework"""
    def get(self, request, *args, **kwargs):
        task_monitor, _ = TaskMonitor.objects.get_or_create()
        # Status 500 if last task run was > 15 min ago
        message = f"Last run: {timezone.localtime(task_monitor.last_run).isoformat()}"
        worker_down = task_monitor.last_run < timezone.now() - timedelta(minutes=15)
        return HttpResponse(message, status=500 if worker_down else 200)

{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE celery
{%- endif %}

{%- endif %}

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
