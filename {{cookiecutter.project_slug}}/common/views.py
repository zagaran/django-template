from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.http.response import HttpResponse
{%- if cookiecutter.crispy_forms == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE crispy_forms
{%- endif %}
from django.views.generic.edit import FormView

{%- if cookiecutter.reference_examples == "on" %}
from common.forms import SampleForm
{%- endif %}
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE crispy_forms
{%- endif %}
{%- endif %}
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
{%- if cookiecutter.reports == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE reports
{%- endif %}
from django.core.files.storage import storages
from reports.reports import UsersReport, PermissionsReport
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE reports
{%- endif %}
{%- endif %}

class IndexView(TemplateView):
    template_name = "common/index.html"


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
class DjangoReactView(TemplateView):
    # TODO: delete me; this is just a reference example
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
{%- if cookiecutter.reference_examples == "on" %}
{%- if cookiecutter.crispy_forms == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE crispy_forms
{%- endif %}
class SampleFormView(FormView):
    # TODO: delete me; this is just a reference example
    form_class = SampleForm
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE crispy_forms
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
{%- if cookiecutter.reference_examples == "on" %}
{%- if cookiecutter.reports == "enabled" %}


{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE reports
{%- endif %}

class SampleReportView(TemplateView):
    # TODO: delete me; this is just a reference example
    report_classes = [UsersReport, PermissionsReport]
    template_name = 'common/sample_report_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = []
        for ReportClass in self.report_classes:
            prefix = ReportClass.report_folder
            report_file_paths = [f"{prefix}/{file_name}" for file_name in
                                 storages["reports"].listdir(prefix)[1]]
            reports.extend({
                               "name": prefix,
                               "generated_on": storages[
                                   "reports"].get_created_time(file),
                               "url": storages["reports"].url(file)
                           } for file in report_file_paths)
        context["reports"] = reports
        return context

    def post(self, request):
        for ReportClass in self.report_classes:
            ReportClass().write_report()
        return redirect("report_generation_demo")

{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE reports
{%- endif %}

{%- endif %}
{%- endif %}

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)
