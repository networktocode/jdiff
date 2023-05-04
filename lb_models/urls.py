"""Django urlpatterns declaration for lb_nodels plugin."""
from django.urls import path
from nautobot.extras.views import ObjectChangeLogView

from lb_models import models
from lb_models.views import (
    sslcertkey,
    sslserverbinding,
    monitor,
    servicegroupmemberbinding,
    servicegroup,
    vserver,
    customerappprofile,
)

# Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
urlpatterns = [
    path("sslcertkey/", sslcertkey.SSLCertKeyListView.as_view(), name="sslcertkey_list"),
    path("sslcertkey/add/", sslcertkey.SSLCertKeyCreateView.as_view(), name="sslcertkey_add"),
    path("sslcertkey/import/", sslcertkey.SSLCertKeyBulkImportView.as_view(), name="sslcertkey_import"),
    path("sslcertkey/delete/", sslcertkey.SSLCertKeyBulkDeleteView.as_view(), name="sslcertkey_bulk_delete"),
    path("sslcertkey/edit/", sslcertkey.SSLCertKeyBulkEditView.as_view(), name="sslcertkey_bulk_edit"),
    path("sslcertkey/<slug:slug>/", sslcertkey.SSLCertKeyView.as_view(), name="sslcertkey"),
    path("sslcertkey/<slug:slug>/delete/", sslcertkey.SSLCertKeyDeleteView.as_view(), name="sslcertkey_delete"),
    path("sslcertkey/<slug:slug>/edit/", sslcertkey.SSLCertKeyEditView.as_view(), name="sslcertkey_edit"),
    path(
        "sslcertkey/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="sslcertkey_changelog",
        kwargs={"model": models.SSLCertKey},
    ),
    path("sslserverbinding/", sslserverbinding.SSLServerBindingListView.as_view(), name="sslserverbinding_list"),
    path("sslserverbinding/add/", sslserverbinding.SSLServerBindingCreateView.as_view(), name="sslserverbinding_add"),
    path(
        "sslserverbinding/import/",
        sslserverbinding.SSLServerBindingBulkImportView.as_view(),
        name="sslserverbinding_import",
    ),
    path(
        "sslserverbinding/delete/",
        sslserverbinding.SSLServerBindingBulkDeleteView.as_view(),
        name="sslserverbinding_bulk_delete",
    ),
    path(
        "sslserverbinding/edit/",
        sslserverbinding.SSLServerBindingBulkEditView.as_view(),
        name="sslserverbinding_bulk_edit",
    ),
    path("sslserverbinding/<slug:slug>/", sslserverbinding.SSLServerBindingView.as_view(), name="sslserverbinding"),
    path(
        "sslserverbinding/<slug:slug>/delete/",
        sslserverbinding.SSLServerBindingDeleteView.as_view(),
        name="sslserverbinding_delete",
    ),
    path(
        "sslserverbinding/<slug:slug>/edit/",
        sslserverbinding.SSLServerBindingEditView.as_view(),
        name="sslserverbinding_edit",
    ),
    path(
        "sslserverbinding/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="sslserverbinding_changelog",
        kwargs={"model": models.SSLServerBinding},
    ),
    path(
        "servicegroupmemberbinding/",
        servicegroupmemberbinding.ServiceGroupMemberBindingListView.as_view(),
        name="servicegroupmemberbinding_list",
    ),
    path(
        "servicegroupmemberbinding/add/",
        servicegroupmemberbinding.ServiceGroupMemberBindingCreateView.as_view(),
        name="servicegroupmemberbinding_add",
    ),
    path(
        "servicegroupmemberbinding/import/",
        servicegroupmemberbinding.ServiceGroupMemberBindingBulkImportView.as_view(),
        name="servicegroupmemberbinding_import",
    ),
    path(
        "servicegroupmemberbinding/delete/",
        servicegroupmemberbinding.ServiceGroupMemberBindingBulkDeleteView.as_view(),
        name="servicegroupmemberbinding_bulk_delete",
    ),
    path(
        "servicegroupmemberbinding/edit/",
        servicegroupmemberbinding.ServiceGroupMemberBindingBulkEditView.as_view(),
        name="servicegroupmemberbinding_bulk_edit",
    ),
    path(
        "servicegroupmemberbinding/<slug:slug>/",
        servicegroupmemberbinding.ServiceGroupMemberBindingView.as_view(),
        name="servicegroupmemberbinding",
    ),
    path(
        "servicegroupmemberbinding/<slug:slug>/delete/",
        servicegroupmemberbinding.ServiceGroupMemberBindingDeleteView.as_view(),
        name="servicegroupmemberbinding_delete",
    ),
    path(
        "servicegroupmemberbinding/<slug:slug>/edit/",
        servicegroupmemberbinding.ServiceGroupMemberBindingEditView.as_view(),
        name="servicegroupmemberbinding_edit",
    ),
    path(
        "servicegroupmemberbinding/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="servicegroupmemberbinding_changelog",
        kwargs={"model": models.ServiceGroupMemberBinding},
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
    path(
        "customerappprofile/", customerappprofile.CustomerAppProfileListView.as_view(), name="customerappprofile_list"
    ),
    path(
        "customerappprofile/add/",
        customerappprofile.CustomerAppProfileCreateView.as_view(),
        name="customerappprofile_add",
    ),
    path(
        "customerappprofile/import/",
        customerappprofile.CustomerAppProfileBulkImportView.as_view(),
        name="customerappprofile_import",
    ),
    path(
        "customerappprofile/delete/",
        customerappprofile.CustomerAppProfileBulkDeleteView.as_view(),
        name="customerappprofile_bulk_delete",
    ),
    path(
        "customerappprofile/edit/",
        customerappprofile.CustomerAppProfileBulkEditView.as_view(),
        name="customerappprofile_bulk_edit",
    ),
    path(
        "customerappprofile/<slug:slug>/",
        customerappprofile.CustomerAppProfileView.as_view(),
        name="customerappprofile",
    ),
    path(
        "customerappprofile/<slug:slug>/delete/",
        customerappprofile.CustomerAppProfileDeleteView.as_view(),
        name="customerappprofile_delete",
    ),
    path(
        "customerappprofile/<slug:slug>/edit/",
        customerappprofile.CustomerAppProfileEditView.as_view(),
        name="customerappprofile_edit",
    ),
    path(
        "customerappprofile/<slug:slug>/changelog/",
        ObjectChangeLogView.as_view(),
        name="customerappprofile_changelog",
        kwargs={"model": models.CustomerAppProfile},
    ),
]
