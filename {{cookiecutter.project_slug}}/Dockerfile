{%- if cookiecutter.docker == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE docker
{%- endif %}
FROM python:3.8.8-slim-buster

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN set -ex \
    && buildDeps=" \
      build-essential \
      libpq-dev \
    " \
    && deps=" \
      postgresql-client-11 \
    " \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps \
       $(! command -v gpg > /dev/null || echo 'gnupg dirmngr') \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
{% if cookiecutter.django_react == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE django_react
{%- endif %}
COPY ./nwb.config.js /app/nwb.config.js
COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN npm install -G nwb
RUN npm install
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_react
{%- endif -%}
{%- endif %}
COPY . /app/
COPY ./config/.env.example /app/config/.env
{% if cookiecutter.django_react == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE django_react
{%- endif %}
RUN ./node_modules/.bin/nwb build --no-vendor
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_react
{%- endif -%}
{%- endif -%}
{%- if cookiecutter.sass_bootstrap == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE sass_bootstrap
{%- endif %}
RUN python manage.py compilescss
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE sass_bootstrap
{%- endif -%}
{%- endif %}
RUN python manage.py collectstatic --noinput

RUN rm /app/config/.env

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi:application"]
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE docker
{%- endif %}
{%- endif %}
