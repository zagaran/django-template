{%- if cookiecutter.crispy_forms == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE crispy_forms
{% endif -%}
from crispy_forms.helper import Layout
from crispy_forms.layout import Fieldset
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE crispy_forms
{%- endif %}
{% endif -%}
from django import forms
from django.http import HttpRequest
from app.models import SampleObject
{%- if cookiecutter.direct_upload == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE direct_upload
{%- endif %}
from app.fields import DirectUploadFileField
from app.models import Attachment
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE direct_upload
{%- endif %}
{%- endif %}
from common.forms import ActionFormMixin{% if cookiecutter.crispy_forms == "enabled" %}, CrispyFormMixin{% endif %}


class SampleObjectBaseForm({% if cookiecutter.crispy_forms == "enabled" %}CrispyFormMixin, {% endif %}ActionFormMixin, forms.ModelForm):
    request: HttpRequest
    {%- if cookiecutter.direct_upload == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE direct_upload
    {%- endif %}
    attachments = DirectUploadFileField(queryset=Attachment.objects.filter(deleted_on=None), required=False)
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE direct_upload
    {%- endif %}
    {%- endif %}

    class Meta:
        model = SampleObject
        exclude = ['created_by']
        {%- if cookiecutter.vue == "enabled" %}
        {%- if cookiecutter.feature_annotations == "on" %}
        # START_FEATURE vue
        {%- endif %}
        widgets = {
            # v-pre stops Vue from compiling the user-supplied textarea content as a template
            "description": forms.Textarea(attrs={"v-pre": True}),
        }
        {%- if cookiecutter.feature_annotations == "on" %}
        # END_FEATURE vue
        {%- endif %}
        {%- endif %}
    {%- if cookiecutter.crispy_forms == "enabled" %}

    {% if cookiecutter.feature_annotations == "on" %}# START_FEATURE crispy_forms
    {% endif %}layout = Layout(
        Fieldset(
            "Details",
            "name",
            "description"
        ),
        {%- if cookiecutter.direct_upload == "enabled" %}
        {%- if cookiecutter.feature_annotations == "on" %}
        # START_FEATURE direct_upload
        {%- endif %}
        "attachments"
        {%- if cookiecutter.feature_annotations == "on" %}
        # END_FEATURE direct_upload
        {%- endif %}
        {%- endif %}
    )
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE crispy_forms
    {%- endif %}
    {%- endif %}

    def __init__(self, request: HttpRequest, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class SampleObjectCreateForm(SampleObjectBaseForm):
    action_title = "Create Sample Object"

    def save(self, commit=True):
        self.instance.created_by = self.request.user
        return super().save(commit)


class SampleObjectEditForm(SampleObjectBaseForm):
    action_title = "Edit {instance}"
