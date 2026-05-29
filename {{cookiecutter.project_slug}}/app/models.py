from django.db import models

from common.models import TimestampedModel, User
{%- if cookiecutter.django_storages == "enabled" %}
from common.models import UploadFile
{%- endif %}


class SampleObject(TimestampedModel):
    created_by = models.ForeignKey(User, related_name="sample_objects", on_delete=models.PROTECT)
    {%- if cookiecutter.direct_upload == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE direct_upload
    {%- endif %}
    attachments = models.ManyToManyField("Attachment", related_name="sample_objects")
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE direct_upload
    {%- endif %}
    {%- endif %}

    name = models.CharField(max_length=512, unique=True)
    description = models.TextField(default="", blank=True)

    def __str__(self) -> str:
        return f'Sample Object {self.name}'
    {%- if cookiecutter.direct_upload == "enabled" %}

    def get_attachments(self):
        qs = self.attachments.prefetch_related('user')
        return [
            attachment for attachment in qs
            if not attachment.deleted_on and attachment.upload_completed_on
        ]
    {%- endif %}

{%- if cookiecutter.direct_upload == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}


# START_FEATURE direct_upload
{%- endif %}
class Attachment(UploadFile):
    pass
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE direct_upload
{%- endif %}
{%- endif %}
