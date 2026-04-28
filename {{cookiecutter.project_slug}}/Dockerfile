{% if cookiecutter.feature_annotations == "on" -%}# START_FEATURE docker{%- endif %}
FROM python:3.11-bookworm

# reduces file creation
ENV PYTHONDONTWRITEBYTECODE=1
# disables output buffering so logs are flushed to console
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# LTS Version of Node is 22
ARG NODE_VERSION=22
{% if cookiecutter.django_react == "enabled" -%}
{% if cookiecutter.feature_annotations == "on" -%}# START_FEATURE django_react{%- endif %}
# if using nwb, nwb requires Node 16. TODO remove nwb
ARG NODE_VERSION=16
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE django_react{%- endif %}
{% endif -%}

# install node
RUN curl -fsSL https://deb.nodesource.com/setup_{$NODE_VERSION}.x | bash -
RUN apt-get update && apt install nodejs -y

RUN set -ex \
    && buildDeps=" \
      build-essential \
      libpq-dev \
    " \
    && deps=" \
      curl \
      vim \
      nano \
      procps \
      postgresql-client \
    " \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends

# Install python dependencies
ADD requirements.txt /app/requirements.txt
RUN set -ex \
    && pip install --no-cache-dir -r /app/requirements.txt

# Cleanup installs
RUN set -ex \
    && apt purge -y --auto-remove $buildDeps \
       $(! command -v gpg > /dev/null || echo 'gnupg dirmngr') \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

{% if cookiecutter.django_react == "enabled" -%}
{% if cookiecutter.feature_annotations == "on" -%}# START_FEATURE django_react{%- endif %}
COPY ./nwb.config.js /app/nwb.config.js
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE django_react{%- endif %}
{% endif -%}

COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json
RUN npm install

# Copy project files into the container
COPY . /app/
# Add temporary copy of env file to allow running management commands
COPY ./config/.env.build /app/config/.env

{% if cookiecutter.django_react == "enabled" -%}
{% if cookiecutter.feature_annotations == "on" -%}# START_FEATURE django_react{%- endif %}
RUN ./node_modules/.bin/nwb build --no-vendor
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE django_react{%- endif %}

{% endif -%}


{% if cookiecutter.sass_bootstrap == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}# START_FEATURE sass_bootstrap{%- endif %}
RUN python manage.py compilescss
{% if cookiecutter.feature_annotations == "on" -%}# END_FEATURE sass_bootstrap{%- endif %}

{% endif -%}

RUN python manage.py collectstatic --noinput

RUN rm /app/config/.env

# Remove node_modules to save space
RUN rm -rf /app/node_modules

# Remove system dependencies (reduce size)
RUN set -ex \
    && apt purge -y --auto-remove $buildDeps $(! command -v gpg > /dev/null || echo 'gnupg dirmngr') \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "3", "config.wsgi:application", "--access-logfile", "-", "--error-logfile", "-"]
{% if cookiecutter.feature_annotations == "on" %}# END_FEATURE docker{%- endif %}
