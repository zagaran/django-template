from django.conf import settings
from django.conf.urls import url
from django.urls import include, path

from common import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("health_check/", views.HealthCheckView.as_view(), name="index"),
    {%- if cookiecutter.reference_examples == "on" %}
    {%- if cookiecutter.django_react == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}
    # START_FEATURE django_react
    {%- endif %}
    # TODO: delete me; this is just a reference example
    path("django_react/", views.DjangoReactView.as_view(), name='django-react-demo'),
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE django_react
    {%- endif %}
    {%- endif %}
    {%- endif %}
    path("logout", views.LogoutView.as_view(), name="logout")
]
{%- if cookiecutter.debug_toolbar == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}

# START_FEATURE debug_toolbar
{%- endif %}
if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE debug_toolbar
{%- endif %}
{%- endif %}
