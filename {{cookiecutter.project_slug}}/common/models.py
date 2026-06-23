import uuid
{%- if cookiecutter.direct_upload == "enabled" %}
import mimetypes
{%- endif %}

from django.contrib.auth.models import AbstractUser
from django.db import models
{%- if cookiecutter.direct_upload == "enabled" %}
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
{%- if cookiecutter.feature_annotations == "on" %}

# START_FEATURE direct_upload
{%- endif %}
from common.helpers import get_attachment_extension, remove_attachment_extension
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE direct_upload
{%- endif %}
{%- endif %}

{% if cookiecutter.django_social == "enabled" -%}
from common.managers import UserManager
{%- endif %}

from common.permissions import ROLE_PERMISSIONS, UserRole
{%- if cookiecutter.sentry == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}

# START_FEATURE sentry
{%- endif %}
from sentry_sdk import capture_message
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE sentry
{%- endif %}
{%- endif %}


class TimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def update(self, update_dict=None, **kwargs):
        """ Helper method to update objects """
        if not update_dict:
            update_dict = kwargs
        update_fields = {"updated_on"}
        for k, v in update_dict.items():
            setattr(self, k, v)
            update_fields.add(k)
        self.save(update_fields=update_fields)

    class Meta:
        abstract = True


# Create your models here.
class User(AbstractUser, TimestampedModel):
    email = models.EmailField(unique=True)

    {%- if cookiecutter.django_social == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}
    # START_FEATURE django_social
    {%- endif %}
    username = None  # disable the AbstractUser.username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE django_social
    {%- endif %}
    {%- endif %}

    role = models.CharField(max_length=128, default=UserRole.standard, choices=UserRole.choices)

    @property
    def permissions(self):
        return ROLE_PERMISSIONS[self.role]

    def has_permission(self, permission):
        return permission in self.permissions

{%- if cookiecutter.django_storages == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}


# START_FEATURE django_storages
{%- endif %}
def get_upload_prefix(instance, filename):
    return "%s/%s/%s" % (
        "uploads",
        instance.user_id,
        filename,
    )


class UploadFile(TimestampedModel):

    class Meta:
        abstract = True

    user = models.ForeignKey(User, related_name="files", on_delete=models.PROTECT)
    name = models.CharField(max_length=512)
    file = models.FileField(max_length=1024, upload_to=get_upload_prefix)

    {%- if cookiecutter.direct_upload == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}
    # START_FEATURE direct_upload
    {%- endif %}
    upload_completed_on = models.DateTimeField(null=True)
    deleted_on = models.DateTimeField(null=True)

    def get_download_url(self, download_on_open: bool = True):
        extension = get_attachment_extension(self.file.name)
        filename = f"{remove_attachment_extension(self.name)}.{extension}".replace('"', '')
        content_type, _ = mimetypes.guess_type(self.file.name)
        s3_filename = self.file.name

        content_disposition = "attachment" if download_on_open else "inline"

        try:
            if isinstance(self.file.storage, FileSystemStorage):
                return FileResponse(
                    self.file.open(),
                    as_attachment=download_on_open,
                    filename=filename
                )

            # Download file directly from S3
            else:
                url = self.file.storage.url(self.file.name, parameters={
                    "ResponseContentDisposition": f'{content_disposition}; filename="{filename}"',
                    "ResponseContentType": content_type or "application/octet-stream",
                })
                return HttpResponseRedirect(url)

        except Exception:
            {%- if cookiecutter.sentry == "enabled" %}
            capture_message(f"Failed to get object URL from S3 for ({self}) with path ({s3_filename})")
            {%- endif %}
            raise Http404()

    def download_file(self) -> FileResponse | HttpResponse:
        return self.get_download_url(download_on_open=True)

    def view_file(self) -> FileResponse | HttpResponse:
        return self.get_download_url(download_on_open=False)
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE direct_upload
    {%- endif %}
    {%- endif %}
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE django_storages
{%- endif %}
{%- endif %}
{%- if cookiecutter.user_action_tracking == "enabled" %}


{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE user_action_tracking
{%- endif %}
class UserAction(TimestampedModel):
    user = models.ForeignKey(User, related_name="user_actions", on_delete=models.PROTECT)
    url = models.URLField(max_length=2083)
    method = models.CharField(max_length=64)
    url_name = models.CharField(max_length=256, null=True)
    status_code = models.IntegerField()
    user_agent = models.TextField(null=True)
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE user_action_tracking
{%- endif %}
{%- endif %}
{%- if cookiecutter.celery == "enabled" and cookiecutter.sentry != "enabled" %}


{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE celery
{%- endif %}
class TaskMonitor(TimestampedModel):
    """Model to track whether the task framework is successfully running tasks"""
    last_run = models.DateTimeField(auto_now_add=True)
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE celery
{%- endif %}
{%- endif %}
