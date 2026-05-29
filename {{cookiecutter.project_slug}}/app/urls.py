from django.urls import path

from app import views
from app.constants import SAMPLE_OBJECT_PK_URL_KWARG
{%- if cookiecutter.direct_upload == "enabled" %}
from app.constants import ATTACHMENT_PK_URL_KWARG
{%- endif %}

urlpatterns = [
    path(
        "dashboard/",
        views.DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        "sample-objects/create/",
        views.SampleObjectCreateView.as_view(),
        name='sample-object-create'
    ),
    path(
        f"sample-objects/<uuid:{SAMPLE_OBJECT_PK_URL_KWARG}>/",
        views.SampleObjectDetailView.as_view(),
        name='sample-object'
    ),
    path(
        f"sample-objects/<uuid:{SAMPLE_OBJECT_PK_URL_KWARG}>/edit/",
        views.SampleObjectEditView.as_view(),
        name='sample-object-edit'
    ),
    {%- if cookiecutter.direct_upload == "enabled" %}
    {%- if cookiecutter.feature_annotations == "on" %}

    # START_FEATURE direct_upload
    {%- endif %}
    path(
        "attachments/upload-start/",
        views.FileUploadStartView.as_view(),
        name='attachment_upload_start'
    ),
    path(
        f"attachments/<uuid:{ATTACHMENT_PK_URL_KWARG}>/upload-stream/",
        views.FileUploadStreamView.as_view(),
        name='attachment_upload_stream'
    ),
    path(
        f"attachments/<uuid:{ATTACHMENT_PK_URL_KWARG}>/upload-complete/",
        views.FileUploadCompleteView.as_view(),
        name='attachment_upload_complete'
    ),
    path(
        f"attachments/<uuid:{ATTACHMENT_PK_URL_KWARG}>/delete/",
        views.FileDeleteView.as_view(),
        name='attachment_delete'
    ),
    path(
        f"attachments/<uuid:{ATTACHMENT_PK_URL_KWARG}>/download/",
        views.FileDownloadView.as_view(),
        name='attachment_download'
    ),
    path(
        f"attachments/<uuid:{ATTACHMENT_PK_URL_KWARG}>/open/",
        views.FileOpenView.as_view(),
        name='attachment_open'
    ),
    {%- if cookiecutter.feature_annotations == "on" %}
    # END_FEATURE direct_upload
    {%- endif %}
    {%- endif %}
]
