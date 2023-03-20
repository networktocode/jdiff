"""Django urlpatterns declaration for lb_nodels plugin."""
from django.urls import path
from nautobot.extras.views import ObjectChangeLogView

from lb_models import models
from lb_models.views import certificate, servicegroupbinding, healthmonitor, servicegroup, vserver

# Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
urlpatterns = [
    path("certificate/", certificate.CertificateListView.as_view(), name="certificate_list"),
    path("certificate/add/", certificate.CertificateCreateView.as_view(), name="certificate_add"),
    path("certificate/import/", certificate.CertificateBulkImportView.as_view(), name="certificate_import"),
    path("certificate/delete/", certificate.CertificateBulkDeleteView.as_view(), name="certificate_bulk_delete"),
    path("certificate/edit/", certificate.CertificateBulkEditView.as_view(), name="certificate_bulk_edit"),
    path("certificate/<slug:slug>/", certificate.CertificateView.as_view(), name="certificate"),
    path("certificate/<slug:slug>/delete/", certificate.CertificateDeleteView.as_view(), name="certificate_delete"),
    path("certificate/<slug:slug>/edit/", certificate.CertificateEditView.as_view(), name="certificate_edit"),
    path(
        "certificate/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="certificate_changelog",
        kwargs={"model": models.Certificate},
    ),
    path("servicegroupbinding/", servicegroupbinding.ServiceGroupBindingListView.as_view(), name="servicegroupbinding_list"),
    path("servicegroupbinding/add/", servicegroupbinding.ServiceGroupBindingCreateView.as_view(), name="servicegroupbinding_add"),
    path("servicegroupbinding/import/", servicegroupbinding.ServiceGroupBindingBulkImportView.as_view(), name="servicegroupbinding_import"),
    path("servicegroupbinding/delete/", servicegroupbinding.ServiceGroupBindingBulkDeleteView.as_view(), name="servicegroupbinding_bulk_delete"),
    path("servicegroupbinding/edit/", servicegroupbinding.ServiceGroupBindingBulkEditView.as_view(), name="servicegroupbinding_bulk_edit"),
    path("servicegroupbinding/<slug:slug>/", servicegroupbinding.ServiceGroupBindingView.as_view(), name="servicegroupbinding"),
    path("servicegroupbinding/<slug:slug>/delete/", servicegroupbinding.ServiceGroupBindingDeleteView.as_view(), name="servicegroupbinding_delete"),
    path("servicegroupbinding/<slug:slug>/edit/", servicegroupbinding.ServiceGroupBindingEditView.as_view(), name="servicegroupbinding_edit"),
    path(
        "servicegroupbinding/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="servicegroupbinding_changelog",
        kwargs={"model": models.ServiceGroupBinding},
    ),
    path("healthmonitor/", healthmonitor.HealthMonitorListView.as_view(), name="healthmonitor_list"),
    path("healthmonitor/add/", healthmonitor.HealthMonitorCreateView.as_view(), name="healthmonitor_add"),
    path("healthmonitor/import/", healthmonitor.HealthMonitorBulkImportView.as_view(), name="healthmonitor_import"),
    path(
        "healthmonitor/delete/",
        healthmonitor.HealthMonitorBulkDeleteView.as_view(),
        name="healthmonitor_bulk_delete",
    ),
    path("healthmonitor/edit/", healthmonitor.HealthMonitorBulkEditView.as_view(), name="healthmonitor_bulk_edit"),
    path("healthmonitor/<slug:slug>/", healthmonitor.HealthMonitorView.as_view(), name="healthmonitor"),
    path(
        "healthmonitor/<slug:slug>/delete/",
        healthmonitor.HealthMonitorDeleteView.as_view(),
        name="healthmonitor_delete",
    ),
    path(
        "healthmonitor/<slug:slug>/edit/",
        healthmonitor.HealthMonitorEditView.as_view(),
        name="healthmonitor_edit",
    ),
    path(
        "healthmonitor/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="healthmonitor_changelog",
        kwargs={"model": models.HealthMonitor},
    ),
    path("servicegroup/", servicegroup.ServiceGroupListView.as_view(), name="servicegroup_list"),
    path("servicegroup/add/", servicegroup.ServiceGroupCreateView.as_view(), name="servicegroup_add"),
    path("servicegroup/import/", servicegroup.ServiceGroupBulkImportView.as_view(), name="servicegroup_import"),
    path("servicegroup/delete/", servicegroup.ServiceGroupBulkDeleteView.as_view(), name="servicegroup_bulk_delete"),
    path("servicegroup/edit/", servicegroup.ServiceGroupBulkEditView.as_view(), name="servicegroup_bulk_edit"),
    path("servicegroup/<slug:slug>/", servicegroup.ServiceGroupView.as_view(), name="servicegroup"),
    path("servicegroup/<slug:slug>/delete/", servicegroup.ServiceGroupDeleteView.as_view(), name="servicegroup_delete"),
    path("servicegroup/<slug:slug>/edit/", servicegroup.ServiceGroupEditView.as_view(), name="servicegroup_edit"),
    path(
        "servicegroup/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="servicegroup_changelog",
        kwargs={"model": models.ServiceGroup},
    ),
    path("vserver/", vserver.vserverListView.as_view(), name="vserver_list"),
    path("vserver/add/", vserver.vserverCreateView.as_view(), name="vserver_add"),
    path("vserver/import/", vserver.vserverBulkImportView.as_view(), name="vserver_import"),
    path("vserver/delete/", vserver.vserverBulkDeleteView.as_view(), name="vserver_bulk_delete"),
    path("vserver/edit/", vserver.vserverBulkEditView.as_view(), name="vserver_bulk_edit"),
    path("vserver/<slug:slug>/", vserver.vserverView.as_view(), name="vserver"),
    path("vserver/<slug:slug>/delete/", vserver.vserverDeleteView.as_view(), name="vserver_delete"),
    path("vserver/<slug:slug>/edit/", vserver.vserverEditView.as_view(), name="vserver_edit"),
    path(
        "vserver/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vserver_changelog",
        kwargs={"model": models.vserver},
    ),
]
