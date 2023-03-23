"""Tables for LB Models."""

import django_tables2 as tables
from nautobot.utilities.tables import BaseTable, ButtonsColumn, ToggleColumn


from lb_models import models


class CertificateTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.Certificate,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Certificate
        fields = [
            "slug",
            "issuer",
            "version_number",
            "serial_number",
            "name",
            "key",
            "password",
            "start_date",
            "end_date",
        ]


class ServiceGroupBindingTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.ServiceGroupBinding,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroupBinding
        fields = [
            "slug",
            "name",
            "description",
            "protocol",
            "port",
            "address",
            "fqdn",
            "monitor",
        ]


class HealthMonitorTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.HealthMonitor,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.HealthMonitor
        fields = [
            "slug",
            "name",
            "description",
            "type",
            "lrtm",
            "secure",
            "url",
            "send",
            "code",
            "receive",
            "httprequest",
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

    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceGroup
        fields = ["slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]


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
            "description",
            "device",
            "interface",
            "address",
            "pool",
            "vlan",
            "vrf",
            "fqdn",
            "protocol",
            "port",
            "method",
            "certificate",
            "owner",
        ]


class CustomerTable(BaseTable):
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

        model = models.Customer
        fields = [
            "slug",
            "customer_id",
            "site",
            "name",
            "fqdn",
            "oe",
            "email",
            "class_type",
            "accessibility",
            "test_url",
        ]
