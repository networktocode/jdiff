"""Django urlpatterns declaration for lb_nodels plugin."""
from django.urls import path
from nautobot.extras.views import ObjectChangeLogView

from lb_models import models
from lb_models.views import certificate, monitor, servicegroupbinding, servicegroup, vserver, customer

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
    path(
        "servicegroupbinding/",
        servicegroupbinding.ServiceGroupBindingListView.as_view(),
        name="servicegroupbinding_list",
    ),
    path(
        "servicegroupbinding/add/",
        servicegroupbinding.ServiceGroupBindingCreateView.as_view(),
        name="servicegroupbinding_add",
    ),
    path(
        "servicegroupbinding/import/",
        servicegroupbinding.ServiceGroupBindingBulkImportView.as_view(),
        name="servicegroupbinding_import",
    ),
    path(
        "servicegroupbinding/delete/",
        servicegroupbinding.ServiceGroupBindingBulkDeleteView.as_view(),
        name="servicegroupbinding_bulk_delete",
    ),
    path(
        "servicegroupbinding/edit/",
        servicegroupbinding.ServiceGroupBindingBulkEditView.as_view(),
        name="servicegroupbinding_bulk_edit",
    ),
    path(
        "servicegroupbinding/<slug:slug>/",
        servicegroupbinding.ServiceGroupBindingView.as_view(),
        name="servicegroupbinding",
    ),
    path(
        "servicegroupbinding/<slug:slug>/delete/",
        servicegroupbinding.ServiceGroupBindingDeleteView.as_view(),
        name="servicegroupbinding_delete",
    ),
    path(
        "servicegroupbinding/<slug:slug>/edit/",
        servicegroupbinding.ServiceGroupBindingEditView.as_view(),
        name="servicegroupbinding_edit",
    ),
    path(
        "servicegroupbinding/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="servicegroupbinding_changelog",
        kwargs={"model": models.ServiceGroupBinding},
    ),
    path("monitor/", monitor.MonitorListView.as_view(), name="monitor_list"),
    path("monitor/add/", monitor.MonitorCreateView.as_view(), name="monitor_add"),
    path("monitor/import/", monitor.MonitorBulkImportView.as_view(), name="monitor_import"),
    path(
        "monitor/delete/",
        monitor.MonitorBulkDeleteView.as_view(),
        name="monitor_bulk_delete",
    ),
    path("monitor/edit/", monitor.MonitorBulkEditView.as_view(), name="monitor_bulk_edit"),
    path("monitor/<slug:slug>/", monitor.MonitorView.as_view(), name="monitor"),
    path(
        "monitor/<slug:slug>/delete/",
        monitor.MonitorDeleteView.as_view(),
        name="monitor_delete",
    ),
    path(
        "monitor/<slug:slug>/edit/",
        monitor.MonitorEditView.as_view(),
        name="monitor_edit",
    ),
    path(
        "monitor/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="monitor_changelog",
        kwargs={"model": models.Monitor},
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
    path("vserver/", vserver.VserverListView.as_view(), name="vserver_list"),
    path("vserver/add/", vserver.VserverCreateView.as_view(), name="vserver_add"),
    path("vserver/import/", vserver.VserverBulkImportView.as_view(), name="vserver_import"),
    path("vserver/delete/", vserver.VserverBulkDeleteView.as_view(), name="vserver_bulk_delete"),
    path("vserver/edit/", vserver.VserverBulkEditView.as_view(), name="vserver_bulk_edit"),
    path("vserver/<slug:slug>/", vserver.VserverView.as_view(), name="vserver"),
    path("vserver/<slug:slug>/delete/", vserver.VserverDeleteView.as_view(), name="vserver_delete"),
    path("vserver/<slug:slug>/edit/", vserver.VserverEditView.as_view(), name="vserver_edit"),
    path(
        "vserver/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="vserver_changelog",
        kwargs={"model": models.Vserver},
    ),
    path("customer/", customer.CustomerListView.as_view(), name="customer_list"),
    path("customer/add/", customer.CustomerCreateView.as_view(), name="customer_add"),
    path("customer/import/", customer.CustomerBulkImportView.as_view(), name="customer_import"),
    path("customer/delete/", customer.CustomerBulkDeleteView.as_view(), name="customer_bulk_delete"),
    path("customer/edit/", customer.CustomerBulkEditView.as_view(), name="customer_bulk_edit"),
    path("customer/<slug:slug>/", customer.CustomerView.as_view(), name="customer"),
    path("customer/<slug:slug>/delete/", customer.CustomerDeleteView.as_view(), name="customer_delete"),
    path("customer/<slug:slug>/edit/", customer.CustomerEditView.as_view(), name="customer_edit"),
    path(
        "customer/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="customer_changelog",
        kwargs={"model": models.Customer},
    ),
]
