"""Tables for LB Models."""

import django_tables2 as tables
from nautobot.utilities.tables import BaseTable, ButtonsColumn, ToggleColumn


from lb_models import models


class SSLCertKeyTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.SSLCertKey,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.SSLCertKey
        fields = [
            "slug",
            "key_name",
            "private_key_filename",
            "private_crt_filename",
            "snow_ticket_id",
        ]


class SSLServerBindingTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.SSLServerBinding,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.SSLServerBinding
        fields = [
            "slug",
            "server_name",
            "ssl_certkey",
        ]


class ServiceGroupMemberBindingTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.ServiceGroupMemberBinding,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    group_binding_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "slug",
            "group_binding_name",
            "server_port",
            "server_name",
        ]


class MonitorTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.Monitor,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    monitor_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Monitor
        fields = ["slug", "monitor_name", "comment", "monitor_type", "lrtm", "monitor_args", "snow_ticket_id"]


class ServiceGroupMonitorBindingTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.ServiceGroupMonitorBinding,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    group_monitor_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroupMonitorBinding
        fields = [
            "slug",
            "group_monitor_name",
            "monitor",
        ]


class ServiceGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.ServiceGroup,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    service_group_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroup
        fields = [
            "slug",
            "service_group_name",
            "comment",
            "service_group_member",
            "service_type",
            "monitor",
            "ssl_profile",
            "snow_ticket_id",
        ]


class VserverTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.Vserver,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    vserver_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Vserver
        fields = [
            "slug",
            "vserver_name",
            "comment",
            "device",
            "ipv4_address",
            "service_group_binding",
            "service_type",
            "lb_method",
            "ssl_binding",
            "customer_app_profile",
            "ssl_profile",
            "persistence_type",
            "vserver_args",
            "snow_ticket_id",
            "vserver_td",
        ]


class CustomerAppProfileTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.Vserver,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    profile_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.CustomerAppProfile
        fields = [
            "slug",
            "profile_name",
            "application_name",
            "site",
            "fqdn",
            "oe_bu",
            "owner_contact",
            "class_type",
            "accessibility",
            "test_url",
        ]


class ServerTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.Server,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    server_name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Server
        fields = ["slug", "server_name", "state", "ipv4_address", "server_td", "snow_ticket_id"]


class ServerServiceGroupBindingTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.Vserver,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServerServiceGroupBinding
        fields = [
            "slug",
            "name",
            "service_group",
        ]
