"""Models for LB Models."""

from django.db import models
from django.urls import reverse
from nautobot.core.models.generics import PrimaryModel, OrganizationalModel
from django.core.validators import MaxValueValidator, MinValueValidator
from nautobot.extras.utils import extras_features
from nautobot.core.fields import AutoSlugField
from .choices import (
    Protocols,
    MonitorTypes,
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
    monitor = models.ForeignKey(to="Monitor", on_delete=models.PROTECT)

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
    csv_headers = fields
    clone_fields = fields

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
class Monitor(OrganizationalModel):
    """Service Group response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=MonitorTypes)
    lrtm = models.BooleanField(blank=True, null=True, default=False)
    args = models.JSONField(blank=True, null=True)
    snow_id = models.CharField(max_length=100, blank=True, null=True)

    fields = [
        "slug",
        "name",
        "comment",
        "type",
        "lrtm",
        "args",
        "snow_id"
    ]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Monitor."""
        return reverse("plugins:lb_models:monitor", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.comment,
            self.type,
            self.lrtm,
            self.args,
            self.snow_id
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
class ServiceGroup(OrganizationalModel):
    """Service Group model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True, null=True)
    monitor = models.ForeignKey(to="Monitor", on_delete=models.PROTECT)
    member = models.ForeignKey(to="ServiceGroupBinding", on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=ServiceGroupTypes)
    td = models.SmallIntegerField()
    sslprofile = models.CharField(max_length=50)

    fields = ["slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]
    csv_headers = fields
    clone_fields = fields

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
    csv_headers = fields
    clone_fields = fields

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
class Customer(OrganizationalModel):
    """Customer model implementation."""

    slug = AutoSlugField(populate_from="customer_id")
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

    fields = ["slug", "customer_id", "site", "name", "fqdn", "oe", "email", "class_type", "accessibility", "test_url"]
    csv_headers = fields
    clone_fields = fields

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
        return self.customer_id
