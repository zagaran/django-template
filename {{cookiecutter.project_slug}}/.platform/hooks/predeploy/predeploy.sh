#!/bin/bash
{% if cookiecutter.feature_annotations == "on" -%}# START_FEATURE elastic_beanstalk{%- endif %}
source $PYTHONPATH/activate

{% if cookiecutter.django_react == "enabled" or cookiecutter.sass_bootstrap == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}# START_FEATURE django_react, sass_bootstrap{%- endif %}
npm install --production
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE django_react, sass_bootstrap{%- endif %}
{%- endif %}

{% if cookiecutter.django_react == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}# START_FEATURE django_react{%- endif %}
$(npm bin)/nwb build --no-vendor
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE django_react{%- endif %}
{%- endif %}

{% if cookiecutter.sass_bootstrap == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}# START_FEATURE sass_bootstrap{%- endif %}
python manage.py compilescss
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE sass_bootstrap{%- endif %}
{%- endif %}

python manage.py collectstatic --noinput --ignore *.scss
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE elastic_beanstalk{%- endif %}
