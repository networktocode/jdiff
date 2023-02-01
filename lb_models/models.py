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
    start_date = models.DateField
    end_date = models.DateField
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
        return reverse("plugins:lb_models:vip_certificate", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.issuer,
            self.version_number,
            self.serial_number,
            self.signature,
            self.signature_algorithm,
            self.signature_algorithm,
            self.start_date,
            self.end_date,
            self.subject_name,
            self.subject_pub_key,
            self.subject_pub_key_algorithm,
        )

    def __str__(self):
        """Stringify instance."""
        return self.serial_number


class VIPPoolResponse(BaseModel):
    """VIP pool response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    code = models.SmallIntegerField()
    string = models.CharField(max_length=200)
    send = models.CharField(max_length=50)

    csv_headers = ["slug", "name", "description", "code", "string", "send"]
    clone_fields = ["slug", "name", "code", "string", "send"]

    def get_absolute_url(self):
        """Return detail view for VIP pool response."""
        return reverse("plugins:lb_models:vip_pool_response", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (self.slug, self.name, self.description, self.code, self.string, self.send)

    def __str__(self):
        """Stringify instance."""
        return self.name


class VIPPoolMember(BaseModel):
    """VIP pool response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    protocol = models.CharField(max_length=20, choices=Protocols)
    port = models.SmallIntegerField()
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
    fqdn = models.CharField(max_length=50)
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


class VIPHealthMonitor(BaseModel):
    """VIP pool response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    send = models.CharField(max_length=50)
    receive = models.CharField(max_length=50)

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
