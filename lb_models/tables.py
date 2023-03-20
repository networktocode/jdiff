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
    certificate = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Certificate
        fields = (
            "slug",
            "issuer",
            "version_number",
            "serial_number",
            "signature",
            "signature_algorithm",
            "signature_algorithm_id",
            "certificate",
            "certificate_key",
            "certificate_password",
            "start_date",
            "end_date",
            "subject_name",
            "subject_pub_key",
            "subject_pub_key_algorithm",
        )


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
        fields = (
            "slug",
            "name",
            "description",
            "protocol",
            "port",
            "address",
            "fqdn",
            "monitor",
        )


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
        fields = (
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
            )


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
        fields = ("slug", "name", "description", "monitor", "member", "type", "td", "sslprofile")


class vserverTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.vserver,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )
    name = tables.Column(linkify=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.vserver
        fields = (
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
            "vserver_args",
        )
