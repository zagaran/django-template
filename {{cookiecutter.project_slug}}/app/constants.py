SAMPLE_OBJECT_PK_URL_KWARG = "sample_object_id"

{%- if cookiecutter.direct_upload == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE direct_upload
{%- endif %}
ATTACHMENT_PK_URL_KWARG = "attachment_id"
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE direct_upload
{%- endif %}
{%- endif %}
