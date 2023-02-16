"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from django.contrib.messages import constants as messages

import environ


env = environ.Env(
    # Sets Django's ALLOWED_HOSTS setting
    ALLOWED_HOSTS=(list, []),
    # Sets Django's DEBUG setting
    DEBUG=(bool, False),
    # Set to True when running locally for development purposes
    LOCALHOST=(bool, False),
    # Set to True in order to put the site in maintenance mode
    MAINTENANCE_MODE=(bool, False),
    # Set to True on the production server environment; setting to False makes the
    # site have a "deny all" robots.txt and a non-production warning on all pages
    PRODUCTION=(bool, True),
    {%- if cookiecutter.django_react == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE django_react
    {%- endif %}
    # Set to True to use JavaScript assets served on localhost:3000 via `nwb serve`
    WEBPACK_LOADER_HOTLOAD=(bool, False),
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE django_react
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.django_ses == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE django_ses
    {%- endif %}
    # Set to configure AWS SES to run in a region other than us-east-1
    AWS_SES_REGION_NAME=(str, "us-east-1"),
    AWS_SES_REGION_ENDPOINT=(str, "email.us-east-1.amazonaws.com"),
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE django_ses
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.sentry == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE sentry
    {%- endif %}
    # Set to the DSN from sentry.io to send errors to Sentry
    SENTRY_DSN=(str, None),
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE sentry
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.debug_toolbar == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE debug_toolbar
    {%- endif %}
    # Set to True to enable the Django Debug Toolbar
    DEBUG_TOOLBAR=(bool, False),
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE debug_toolbar
    {%- endif %}
    {%- endif %}
)
# If ALLWED_HOSTS has been configured, then we're running on a server and
# can skip looking for a .env file (this assumes that .env files
# file is only used for local development and servers use environment variables)
if not env.ALLOWED_HOSTS:
    environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: do not run with debug turned on in production!
DEBUG = env("DEBUG")
{%- if cookiecutter.debug_toolbar == "enabled" %}
{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE debug_toolbar
{%- endif %}
DEBUG_TOOLBAR = DEBUG and env("DEBUG_TOOLBAR")
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE debug_toolbar
{%- endif %}
{%- endif %}

# run with this set to False on server environments
LOCALHOST = env("LOCALHOST")

# set PRODUCTION to be False on non-production server environments to prevent
# them from being indexed by search engines and to have a banner warning
# that this is not the production site
PRODUCTION = env("PRODUCTION")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
if LOCALHOST is True:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
else:
    {%- if cookiecutter.elastic_beanstalk == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}
    # START_FEATURE elastic_beanstalk
    {%- endif %}
    # if using AWS hosting
    from ec2_metadata import ec2_metadata
    ALLOWED_HOSTS.append(ec2_metadata.private_ipv4)
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE elastic_beanstalk
    {%- endif %}
    {%- endif %}

# Application definition
THIRD_PARTY_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    {%- if cookiecutter.django_social == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE django_social
    {%- endif %}
    "social_django",
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE django_social
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.crispy_forms == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE crispy_forms
    {%- endif %}
    "crispy_forms",
    "crispy_bootstrap5",
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE crispy_forms
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.django_react == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE django_react
    {%- endif %}
    "django_react_components",
    "webpack_loader",
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE django_react
    {%- endif %}
    {%- endif %}
    {%- if cookiecutter.sass_bootstrap == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE sass_bootstrap
    {%- endif %}
    "sass_processor",
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE sass_bootstrap
    {%- endif %}
    {%- endif %}
]

{ % - if cookiecutter.debug_toolbar == "enabled" %}
{ % - if cookiecutter.feature_annotations == "on" %}

# START_FEATURE debug_toolbar
{ % - endif %}
if DEBUG_TOOLBAR:
    THIRD_PARTY_APPS += ["debug_toolbar"]
{ % - if cookiecutter.feature_annotations == "on" %}
# END_FEATURE debug_toolbar
{ % - endif %}
{ % - endif %}

LOCAL_APPS = [
    "common",
]

INSTALLED_APPS = THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "common.middleware.MaintenanceModeMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    {%- if cookiecutter.user_action_tracking == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}
    # START_FEATURE user_action_tracking
    {%- endif %}
    "common.middleware.UserActionTrackingMiddleware"
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE user_action_tracking
    {%- endif %}
    {%- endif %}
]

MAINTENANCE_MODE = env("MAINTENANCE_MODE")
{%- if cookiecutter.user_action_tracking == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE user_action_tracking
{%- endif %}
USER_TRACKING_EXEMPT_ROUTES = []
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE user_action_tracking
{%- endif %}
{%- endif %}


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.django_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {"default": env.db()}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
{%- if cookiecutter.django_ses == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE django_ses
{%- endif %}
if LOCALHOST:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "webmaster@localhost"
else:
    EMAIL_BACKEND = "django_ses.SESBackend"
    AWS_SES_REGION_NAME = env("AWS_SES_REGION_NAME")
    AWS_SES_REGION_ENDPOINT = env("AWS_SES_REGION_ENDPOINT")
    AWS_SES_RETURN_PATH = env("DEFAULT_FROM_EMAIL")
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_ses
{%- endif %}
{%- endif %}

# Logging
# https://docs.djangoproject.com/en/dev/topics/logging/#django-security
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"]
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

AUTH_USER_MODEL = "common.User"
{%- if cookiecutter.django_social == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE django_social
{%- endif %}
AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
]

LOGIN_URL = "index"
LOGIN_REDIRECT_URL = "index"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_OAUTH2_SECRET")
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_social
{%- endif %}
{%- endif %}
{%- if cookiecutter.crispy_forms == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE crispy_forms
{%- endif %}
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE crispy_forms
{%- endif %}
{%- endif %}
{%- if cookiecutter.bootstrap_messages == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE bootstrap_messages
{%- endif %}
# Bootstrap styling for Django messages
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE bootstrap_messages
{%- endif %}
{%- endif %}
{%- if cookiecutter.django_storages == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE django_storages
{%- endif %}
if LOCALHOST is True:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = ""
else:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_DEFAULT_ACL = "private"
    AWS_S3_FILE_OVERWRITE = False
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_storages
{%- endif %}
{%- endif %}
{%- if cookiecutter.debug_toolbar == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE debug_toolbar
{%- endif %}
INTERNAL_IPS = ['127.0.0.1']
if DEBUG_TOOLBAR:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE debug_toolbar
{%- endif %}
{%- endif %}
{%- if cookiecutter.django_react == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE django_react
{%- endif %}
if DEBUG:
    WEBPACK_LOADER_HOTLOAD = env('WEBPACK_LOADER_HOTLOAD')
    if WEBPACK_LOADER_HOTLOAD:
        WEBPACK_LOADER = {
            'DEFAULT': {
                'LOADER_CLASS': "config.webpack_loader.DynamicWebpackLoader"
            }
        }
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_react
{%- endif %}
{%- endif %}
{%- if cookiecutter.sentry == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE sentry
{%- endif %}
SENTRY_DSN = env("SENTRY_DSN")
if LOCALHOST is False and SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import ignore_logger
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
    )
    # Silence "invalid HTTP_HOST" errors
    ignore_logger("django.security.DisallowedHost")

{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE sentry
{%- endif %}
{%- endif %}
{%- if cookiecutter.security_settings == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE security_settings
{%- endif %}
if LOCALHOST is False:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    USE_X_FORWARDED_HOST = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_HSTS_SECONDS = 3600  # 1 hour
    # TODO: increase SECURE_HSTS_SECONDS and register with hstspreload.org once production deploy is stable
    # SECURE_HSTS_SECONDS = 3600 * 24 * 365 * 2  # 2 years
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 60 * 60 * 3  # 3 hours
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True  # Only do this if you are not accessing the CSRF cookie with JS
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE security_settings
{%- endif %}
{%- endif %}
{%- if cookiecutter.sass_bootstrap == "enabled" %}

{% if cookiecutter.feature_annotations == "on" %}
# START_FEATURE sass_bootstrap
{%- endif %}
SASS_PRECISION = 8  # Bootstrap's sass requires a precision of at least 8 to prevent layout errors
SASS_PROCESSOR_CUSTOM_FUNCTIONS = {
    'django-static': 'django.templatetags.static.static',
}
SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, 'static/styles'),
    os.path.join(BASE_DIR, 'node_modules'),
]
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'static')
COMPRESS_ROOT = SASS_PROCESSOR_ROOT
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE sass_bootstrap
{%- endif %}
{%- endif %}
