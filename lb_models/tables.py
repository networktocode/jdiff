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
            "name",
            "private_key_filename",
            "private_crt_filename",
            "snow_id",
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
            "name",
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
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "slug",
            "name",
            "server_port",
            "server_name",
        ]


class ServiceGroupMonitorBindingTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.ServiceGroupMonitorBinding,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroupMonitorBinding
        fields = [
            "slug",
            "name",
            "monitor",
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
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Monitor
        fields = ["slug", "name", "comment", "type", "lrtm", "args", "snow_id"]


class ServiceGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.ServiceGroup,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroup
        fields = ["slug", "name", "comment", "service_group_member", "service_type", "monitor", "ssl_profile", "snow_id"]


class VserverTable(BaseTable):
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

        model = models.Vserver
        fields = [
            "slug",
            "name",
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
            "args",
            "snow_id",
            "td",
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
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Server
        fields = ["slug", "name", "state", "ipv4_address", "td"]


class CustomerAppProfileTable(BaseTable):
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
