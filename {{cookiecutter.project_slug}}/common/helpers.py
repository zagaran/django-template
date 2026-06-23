{%- if cookiecutter.direct_upload == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE direct_upload
{%- endif %}
import os


def get_attachment_extension(filename: str):
    _, extension = os.path.splitext(filename)
    extension = extension.lower().replace('.', '')
    return extension


def remove_attachment_extension(filename: str):
    name, _ = os.path.splitext(filename)
    return name
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE direct_upload
{%- endif %}
{%- endif %}
