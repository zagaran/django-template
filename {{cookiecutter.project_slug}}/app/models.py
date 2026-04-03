from django.db import models

from common.models import TimestampedModel, UploadFile, User


class SampleObject(TimestampedModel):
    created_by = models.ForeignKey(User, related_name="sample_objects", on_delete=models.PROTECT)

    {%- if cookiecutter.direct_upload == "enabled" -%}
    {%- if cookiecutter.feature_annotations == "on" -%}
    # START_FEATURE direct_upload
    attachments = models.ManyToManyField("Attachment", related_name="sample_objects")

    # END_FEATURE direct_upload
    {%- endif -%}
    {%- endif -%}

    name = models.CharField(max_length=512, unique=True)
    description = models.TextField(default="", blank=True)

    def __str__(self) -> str:
        return f'Sample Object {self.name}'

    def get_attachments(self):
        return self.attachments.filter(deleted_on=None)


{%- if cookiecutter.direct_upload == "enabled" -%}
{%- if cookiecutter.feature_annotations == "on" -%}
# START_FEATURE direct_upload
class Attachment(UploadFile):
    pass
# END_FEATURE direct_upload
{%- endif -%}
{%- endif -%}
