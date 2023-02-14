"""Tables for fcc_dispatching."""

import django_tables2 as tables
from nautobot.utilities.tables import BaseTable, ButtonsColumn, ToggleColumn


from lb_models import models


class VIPCertificateTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.VIPCertificate,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.VIPCertificate
        fields = (
            "issuer",
            "version_number",
            "serial_number",
            "signature",
            "signature_algorithm",
            "signature_algorithm_id",
            "start_date",
            "end_date",
            "subject_name",
            "subject_pub_key",
            "subject_pub_key_algorithm",
        )


class VIPPoolMemberTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.VIPPoolMember,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = (
            "slug",
            "name",
            "description",
            "protocol",
            "port",
            "ipv4_address",
            "ipv6_address",
            "fqdn",
            "monitor",
            "member_args",
        )


class VIPHealthMonitorTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.VIPHealthMonitor,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = (
            "slug",
            "name",
            "description",
            "type",
            "url",
            "send",
            "code",
            "receive",
        )


class VIPPoolTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.VIPPool,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.VIPPool
        fields = ("slug", "name", "description", "monitor", "member")


class VIPTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    actions = ButtonsColumn(
        models.VIP,
        buttons=("changelog", "edit", "delete", "add"),
        pk_field="slug",
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.VIP
        fields = (
            "slug",
            "name",
            "description",
            "device",
            "interface",
            "ipv4_address",
            "ipv6_address",
            "pool",
            "vlan",
            "vrf",
            "fqdn",
            "protocol",
            "port",
            "method",
            "certificate",
            "owner",
            "vip_args",
        )
