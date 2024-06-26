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

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)
