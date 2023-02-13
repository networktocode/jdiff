"""Django urlpatterns declaration for lb_nodels plugin."""
from django.urls import path
from nautobot.extras.views import ObjectChangeLogView

from lb_models import models
from lb_models.views import certificate, poolmember, healthmonitor, pool

# Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
urlpatterns = [
    path("certificate/", certificate.VIPCertificateListView.as_view(), name="vipcertificate_list"),
    path("certificate/add/", certificate.VIPCertificateCreateView.as_view(), name="vipcertificate_add"),
    path("certificate/import/", certificate.VIPCertificateBulkImportView.as_view(), name="vipcertificate_import"),
    path("certificate/delete/", certificate.VIPCertificateBulkDeleteView.as_view(), name="vipcertificate_bulk_delete"),
    path("certificate/edit/", certificate.VIPCertificateBulkEditView.as_view(), name="vipcertificate_bulk_edit"),
    path("certificate/<slug:slug>/", certificate.VIPCertificateView.as_view(), name="vipcertificate"),
    path(
        "certificate/<slug:slug>/delete/", certificate.VIPCertificateDeleteView.as_view(), name="vipcertificate_delete"
    ),
    path("certificate/<slug:slug>/edit/", certificate.VIPCertificateEditView.as_view(), name="vipcertificate_edit"),
    path(
        "certificate/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vipcertificate_changelog",
        kwargs={"model": models.VIPCertificate},
    ),
    path("poolmember/", poolmember.VIPPoolMemberListView.as_view(), name="vippoolmember_list"),
    path("poolmember/add/", poolmember.VIPPoolMemberCreateView.as_view(), name="vippoolmember_add"),
    path("poolmember/import/", poolmember.VIPPoolMemberBulkImportView.as_view(), name="vippoolmember_import"),
    path("poolmember/delete/", poolmember.VIPPoolMemberBulkDeleteView.as_view(), name="vippoolmember_bulk_delete"),
    path("poolmember/edit/", poolmember.VIPPoolMemberBulkEditView.as_view(), name="vippoolmember_bulk_edit"),
    path("poolmember/<slug:slug>/", poolmember.VIPPoolMemberView.as_view(), name="vippoolmember"),
    path(
        "poolmember/<slug:slug>/delete/", poolmember.VIPPoolMemberDeleteView.as_view(), name="vippoolmember_delete"
    ),
    path("poolmember/<slug:slug>/edit/", poolmember.VIPPoolMemberEditView.as_view(), name="vippoolmember_edit"),
    path(
        "poolmember/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vippoolmember_changelog",
        kwargs={"model": models.VIPPoolMember},
    ),
    path("healthmonitor/", healthmonitor.VIPHealthMonitorListView.as_view(), name="viphealthmonitor_list"),
    path("healthmonitor/add/", healthmonitor.VIPHealthMonitorCreateView.as_view(), name="viphealthmonitor_add"),
    path("healthmonitor/import/", healthmonitor.VIPHealthMonitorBulkImportView.as_view(), name="viphealthmonitor_import"),
    path("healthmonitor/delete/", healthmonitor.VIPHealthMonitorBulkDeleteView.as_view(), name="viphealthmonitor_bulk_delete"),
    path("healthmonitor/edit/", healthmonitor.VIPHealthMonitorBulkEditView.as_view(), name="viphealthmonitor_bulk_edit"),
    path("healthmonitor/<slug:slug>/", healthmonitor.VIPHealthMonitorView.as_view(), name="viphealthmonitor"),
    path(
        "healthmonitor/<slug:slug>/delete/", healthmonitor.VIPHealthMonitorDeleteView.as_view(), name="viphealthmonitor_delete"
    ),
    path("healthmonitor/<slug:slug>/edit/", healthmonitor.VIPHealthMonitorEditView.as_view(), name="viphealthmonitor_edit"),
    path(
        "healthmonitor/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="viphealthmonitor_changelog",
        kwargs={"model": models.VIPHealthMonitor},
    ),
    path("pool/", pool.VIPPoolListView.as_view(), name="vippool_list"),
    path("pool/add/", pool.VIPPoolCreateView.as_view(), name="vippool_add"),
    path("pool/import/", pool.VIPPoolBulkImportView.as_view(), name="vippool_import"),
    path("pool/delete/", pool.VIPPoolBulkDeleteView.as_view(), name="vippool_bulk_delete"),
    path("pool/edit/", pool.VIPPoolBulkEditView.as_view(), name="vippool_bulk_edit"),
    path("pool/<slug:slug>/", pool.VIPPoolView.as_view(), name="vippool"),
    path(
        "pool/<slug:slug>/delete/", pool.VIPPoolDeleteView.as_view(), name="vippool_delete"
    ),
    path("pool/<slug:slug>/edit/", pool.VIPPoolEditView.as_view(), name="vippool_edit"),
    path(
        "pool/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vippool_changelog",
        kwargs={"model": models.VIPPool},
    ),
]
