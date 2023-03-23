"""Models for LB Models."""

from django.db import models
from django.urls import reverse
from nautobot.core.models.generics import PrimaryModel
from django.core.validators import MaxValueValidator, MinValueValidator
from nautobot.extras.utils import extras_features
from nautobot.core.fields import AutoSlugField
from .choices import (
    Protocols,
    HealthMonitorTypes,
    ServiceGroupTypes,
    ApplicationClassTypes,
    ApplicationAccessibility,
)


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
class Certificate(PrimaryModel):
    """Certificate model implementation."""

    slug = AutoSlugField(populate_from="name")
    issuer = models.CharField(max_length=50, blank=True, null=True)
    version_number = models.CharField(max_length=50, blank=True, null=True)
    serial_number = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

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
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Certificate."""
        return reverse("plugins:lb_models:certificate", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.issuer,
            self.version_number,
            self.serial_number,
            self.key,
            self.password,
            self.start_date,
            self.end_date,
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
class ServiceGroupBinding(PrimaryModel):
    """Service Group response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    protocol = models.CharField(max_length=20, choices=Protocols)
    port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(1)])
    address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.CASCADE,
        verbose_name="IPv4 Address",
        blank=True,
        null=True,
    )
    fqdn = models.CharField(max_length=200)
    monitor = models.ForeignKey(to="HealthMonitor", on_delete=models.PROTECT)

    csv_headers = [
        "slug",
        "name",
        "description",
        "protocol",
        "port",
        "address",
        "fqdn",
        "monitor",
    ]
    clone_fields = ["slug", "name", "protocol", "port", "monitor"]

    def get_absolute_url(self):
        """Return detail view for Service Group memeber."""
        return reverse("plugins:lb_models:servicegroupbinding", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.description,
            self.protocol,
            self.port,
            self.address,
            self.fqdn,
            self.monitor,
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
class HealthMonitor(PrimaryModel):
    """Service Group response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=HealthMonitorTypes)
    lrtm = models.BooleanField(blank=True, null=True)
    secure = models.BooleanField(blank=True, null=True)
    url = models.URLField(max_length=50, blank=True, null=True)
    send = models.CharField(max_length=50, blank=True, null=True)
    string = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=50)
    httprequest = models.CharField(max_length=50)
    receive = models.CharField(max_length=50, blank=True, null=True)

    csv_headers = [
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
    clone_fields = [
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

    def get_absolute_url(self):
        """Return detail view for Health Monitor."""
        return reverse("plugins:lb_models:healthmonitor", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.description,
            self.type,
            self.lrtm,
            self.secure,
            self.url,
            self.send,
            self.receive,
            self.httprequest,
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
class ServiceGroup(PrimaryModel):
    """Service Group model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    monitor = models.ForeignKey(to="HealthMonitor", on_delete=models.PROTECT)
    member = models.ForeignKey(to="ServiceGroupBinding", on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=ServiceGroupTypes)
    td = models.SmallIntegerField()
    sslprofile = models.CharField(max_length=50)

    csv_headers = ["slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]
    clone_fields = ["slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]

    def get_absolute_url(self):
        """Return detail view for Service Group memeber."""
        return reverse("plugins:lb_models:servicegroup", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (self.slug, self.name, self.description, self.monitor, self.member, self.type, self.td, self.sslprofile)

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
class Vserver(PrimaryModel):
    """Vserver implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="Device",
    )
    interface = models.ForeignKey(
        to="dcim.Interface",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="Interface",
    )
    address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.CASCADE,
        verbose_name="Member Address",
        blank=True,
        null=True,
    )

    pool = models.ForeignKey(to="ServiceGroup", on_delete=models.PROTECT)
    vlan = models.ForeignKey(
        to="ipam.vlan",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="VLAN",
    )
    vrf = models.ForeignKey(
        to="ipam.vrf",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="vrf",
    )
    fqdn = models.CharField(max_length=200)
    protocol = models.CharField(max_length=20, choices=Protocols)
    port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(1)])
    method = models.CharField(max_length=50)
    certificate = models.ForeignKey(to="Certificate", on_delete=models.CASCADE)
    owner = models.CharField(max_length=50)

    csv_headers = [
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
    ]

    def get_absolute_url(self):
        """Return detail view for vserver."""
        return reverse("plugins:lb_models:vserver", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.description,
            self.device,
            self.interface,
            self.address,
            self.pool,
            self.vlan,
            self.vrf,
            self.fqdn,
            self.protocol,
            self.port,
            self.method,
            self.certificate,
            self.owner,
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
class Customer(PrimaryModel):
    """Customer model implementation."""

    slug = AutoSlugField(populate_from="id")
    customer_id = models.CharField(max_length=50)
    site = models.ForeignKey(
        to="dcim.Site",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="Site",
    )
    name = models.CharField(max_length=50)
    fqdn = models.CharField(max_length=50)
    oe = models.CharField(max_length=50)
    email = models.EmailField()
    class_type = models.CharField(max_length=20, choices=ApplicationClassTypes)
    accessibility = models.CharField(max_length=20, choices=ApplicationAccessibility)
    test_url = models.URLField()

    csv_headers = ["slug", "customer_id", "site", "name", "fqdn", "oe", "email", "class_type", "accessibility", "test_url"]
    clone_fields = ["slug", "customer_id", "site", "name", "fqdn", "oe", "email", "class_type", "accessibility", "test_url"]

    def get_absolute_url(self):
        """Return detail view for Customer memeber."""
        return reverse("plugins:lb_models:customer", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.customer_id,
            self.site,
            self.name,
            self.fqdn,
            self.oe,
            self.email,
            self.class_type,
            self.accessibility,
            self.test_url,
        )

    def __str__(self):
        """Stringify instance."""
        return self.id
