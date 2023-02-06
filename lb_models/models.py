"""Models for Fcc Dispatching."""

import struct
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from nautobot.core.models import BaseModel
from versionfield import VersionField

# from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.utils import extras_features
from nautobot.core.fields import AutoSlugField
from .choices import CertAlgorithmChoices, Protocols


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class VIPCertificate(BaseModel):
    """VIP Certificate model implementation."""

    slug = AutoSlugField(populate_from="serial_number")
    issuer = models.CharField(max_length=50)
    version_number = VersionField()
    serial_number = models.CharField(max_length=30, unique=True)
    signature = models.CharField(max_length=50, unique=True)
    signature_algorithm = models.CharField(max_length=20, choices=CertAlgorithmChoices)
    signature_algorithm_id = models.CharField(max_length=30, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    subject_name = models.CharField(max_length=50)
    subject_pub_key = models.CharField(max_length=100)
    subject_pub_key_algorithm = models.CharField(max_length=20, choices=CertAlgorithmChoices)

    csv_headers = [
        "slug",
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
    ]
    clone_fields = [
        "slug",
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
    ]

    def get_absolute_url(self):
        """Return detail view for VIP certificate."""
        return reverse("plugins:lb_models:vipcertificate", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.issuer,
            self.version_number,
            self.serial_number,
            self.signature,
            self.signature_algorithm,
            self.signature_algorithm_id,
            self.start_date,
            self.end_date,
            self.subject_name,
            self.subject_pub_key,
            self.subject_pub_key_algorithm,
        )

    def __str__(self):
        """Stringify instance."""
        return self.serial_number


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class VIPPoolMember(BaseModel):
    """VIP pool response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    protocol = models.CharField(max_length=20, choices=Protocols)
    port = models.SmallIntegerField(blank=True, null=True)
    ipv4_address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="IPv4 Address",
    )
    ipv6_address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="IPv6 Address",
    )
    fqdn = models.URLField(max_length=200)
    monitor = models.ForeignKey(to="VIPHealthMonitor", on_delete=models.PROTECT)
    member_args = models.JSONField()

    csv_headers = [
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
    ]
    clone_fields = ["slug", "name", "protocol", "port", "monitor", "member_args"]

    def clean(self):
        """JSON Schema enforcement for member_args"""
        # TBD
        pass

    def get_absolute_url(self):
        """Return detail view for VIP pool memeber."""
        return reverse("plugins:lb_models:vip_pool_member", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.description,
            self.protocol,
            self.port,
            self.ipv4_address,
            self.ipv6_address,
            self.fqdn,
            self.monitor,
            self.member_args,
        )

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class VIPHealthMonitor(BaseModel):
    """VIP pool response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=50, blank=True, null=True)
    send = models.CharField(max_length=50, blank=True, null=True)
    string = models.CharField(max_length=100, blank=True, null=True)
    code = models.SmallIntegerField(blank=True, null=True)
    receive = models.CharField(max_length=50, blank=True, null=True)

    csv_headers = [
        "slug",
        "name",
        "description",
        "type",
        "url",
        "send",
        "receive",
    ]
    clone_fields = ["slug", "name", "description", "type", "url", "send", "receive"]

    def get_absolute_url(self):
        """Return detail view for VIP pool memeber."""
        return reverse("plugins:lb_models:vip_healt_monitor", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (self.slug, self.name, self.description, self.type, self.url, self.send, self.receive)

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class VIPPool(BaseModel):
    """VIP pool model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    monitor = models.ForeignKey(to="VIPHealthMonitor", on_delete=models.PROTECT)
    member = models.ForeignKey(to="VIPPoolMember", on_delete=models.PROTECT)

    csv_headers = ["slug", "name", "description", "monitor", "member"]
    clone_fields = ["slug", "name", "description", "monitor", "member"]

    def get_absolute_url(self):
        """Return detail view for VIP pool memeber."""
        return reverse("plugins:lb_models:vip_pool", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (self.slug, self.name, self.description, self.monitor, self.member)

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class VIP(BaseModel):
    """VIP implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="Device",
    )
    interface = models.ForeignKey(
        to="dcim.Interface",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="Interface",
    )
    ipv4_address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="IPv4 Address",
    )
    ipv6_address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="IPv6 Address",
    )
    pool = models.ForeignKey(to="VIPPool", on_delete=models.PROTECT)
    vlan = models.ForeignKey(
        to="ipam.vlan",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="VLAN",
    )
    vrf = models.ForeignKey(
        to="ipam.vrf",
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
        verbose_name="vrf",
    )
    fqdn = models.URLField(max_length=200)
    protocol = models.CharField(max_length=20, choices=Protocols)
    port = models.SmallIntegerField(blank=True, null=True)
    method = models.CharField(max_length=50)
    certificate = models.ForeignKey(to="VIPCertificate", on_delete=models.CASCADE)
    owner = models.CharField(max_length=50)
    vip_args = models.JSONField()

    csv_headers = [
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
    ]
    clone_fields = [
        "slug",
        "name",
        "description",
        "device",
        "pool",
        "protocol",
        "port",
        "method",
        "certificate",
        "owner",
        "vip_args",
    ]

    def get_absolute_url(self):
        """Return detail view for VIP."""
        return reverse("plugins:lb_models:vip", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.description,
            self.device,
            self.interface,
            self.ipv4_address,
            self.ipv6_address,
            self.pool,
            self.vlan,
            self.vrf,
            self.fqdn,
            self.protocol,
            self.port,
            self.method,
            self.certificate,
            self.owner,
            self.vip_args,
        )

    def __str__(self):
        """Stringify instance."""
        return self.name
