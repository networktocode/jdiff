"""Django urlpatterns declaration for lb_nodels plugin."""
from django.urls import path
from nautobot.extras.views import ObjectChangeLogView

from lb_models import models
from lb_models.views import certificates

# Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
urlpatterns = [
    path("certificate/", certificates.VIPCertificateListView.as_view(), name="vipcertificate_list"),
    path("certificate/add/", certificates.VIPCertificateCreateView.as_view(), name="vipcertificate_add"),
    path("certificate/import/", certificates.VIPCertificateBulkImportView.as_view(), name="vipcertificate_import"),
    path("certificate/delete/", certificates.VIPCertificateBulkDeleteView.as_view(), name="vipcertificate_bulk_delete"),
    path("certificate/edit/", certificates.VIPCertificateBulkEditView.as_view(), name="vipcertificate_bulk_edit"),
    path("certificate/<slug:slug>/", certificates.VIPCertificateView.as_view(), name="vipcertificate"),
    path(
        "certificate/<slug:slug>/delete/", certificates.VIPCertificateDeleteView.as_view(), name="vipcertificate_delete"
    ),
    path("certificate/<slug:slug>/edit/", certificates.VIPCertificateEditView.as_view(), name="vipcertificate_edit"),
    path(
        "certificate/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vipcertificate_changelog",
        kwargs={"model": models.VIPCertificate},
    ),
]
