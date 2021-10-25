from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.base import TemplateView, View
{%- if cookiecutter.crispy_forms == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE crispy_forms
{%- endif %}
from django.views.generic.edit import FormView

from crispy_forms.tests.forms import SampleForm
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE crispy_forms
{%- endif %}
{%- endif %}


class IndexView(TemplateView):
    template_name = "common/index.html"


def HealthCheckView(View):
    def get():
        return HttpResponse("ok")


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("index")
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
