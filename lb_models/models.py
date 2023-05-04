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
class SSLCertKey(PrimaryModel):
    """SSLCertKey model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    private_key_filename = models.CharField(max_length=100)
    private_crt_filename = models.CharField(max_length=100)
    password = models.CharField(max_length=50, blank=True, null=True)
    snow_id = models.CharField(max_length=20)

    fields = [
        "slug",
        "name",
        "private_key_filename",
        "private_crt_filename",
        "password",
        "snow_id",
    ]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for SSLCertKey."""
        return reverse("plugins:lb_models:sslcertkey", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.private_key_filename,
            self.private_crt_filename,
            self.password,
            self.snow_id,
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
class SSLServerBinding(PrimaryModel):
    """SSLServerBinding model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    ssl_certkey = models.OneToOneField(SSLCertKey, on_delete=models.CASCADE)
    vserver = models.ForeignKey(to=models.Vserver, on_delete=models.CASCADE)

    fields = [
        "slug",
        "name",
        "ssl_certkey",
        "vserver",
    ]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for SSLServerBinding."""
        return reverse("plugins:lb_models:sslserverbinding", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.ssl_certkey,
            self.vserver,
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
class ServiceGroupMemberBinding(PrimaryModel):
    """Service Group response model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, unique=True)
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
        "port",
        "address",
    ]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Service Group memeber."""
        return reverse("plugins:lb_models:servicegroupmemberbinding", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.port,
            self.address,
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
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=MonitorTypes)
    lrtm = models.BooleanField(default=False)
    args = models.JSONField(blank=True, null=True)
    snow_id = models.CharField(max_length=20)

    fields = ["slug", "name", "comment", "type", "lrtm", "args", "snow_id"]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Monitor."""
        return reverse("plugins:lb_models:monitor", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (self.slug, self.name, self.comment, self.type, self.lrtm, self.args, self.snow_id)

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
class ServiceGroupMonitorBinding(PrimaryModel):
    """ServiceGroupMonitorBinding model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50)
    monitor = models.ForeignKey(to=models.Monitor, on_delete=models.CASCADE)
    service_group = models.ForeignKey(to=models.ServiceGroup, on_delete=models.CASCADE)

    fields = [
        "slug",
        "name",
        "monitor",
        "service_group",
    ]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for ServiceGroupMonitorBinding."""
        return reverse("plugins:lb_models:servicegroupmonitorbinding", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.monitor,
            self.service_group,
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
    comment = models.CharField(max_length=50, blank=True, null=True)
    member = models.ForeignKey(to="ServiceGroupMemberBinding", on_delete=models.PROTECT)
    service_type = models.CharField(max_length=20, choices=ServiceGroupTypes)
    td = models.SmallIntegerField()
    ssl_profile = models.CharField(max_length=50)
    snow_id = models.CharField(max_length=20, blank=True, null=True)

    fields = ["slug", "name", "comment", "member", "service_type", "td", "ssl_profile", "snow_id"]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Service Group memeber."""
        return reverse("plugins:lb_models:servicegroup", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.comment,
            self.member,
            self.service_type,
            self.td,
            self.ssl_profile,
            self.snow_id,
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
    sslcertkey = models.ForeignKey(to="SSLCertKey", on_delete=models.CASCADE)
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
        "sslcertkey",
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
            self.sslcertkey,
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
class CustomerAppProfile(OrganizationalModel):
    """CustomerAppProfile model implementation."""

    slug = AutoSlugField(populate_from="profile_name")
    profile_name = models.CharField(max_length=50)
    application_name = models.CharField(max_length=50)
    site = models.ForeignKey(
        to="dcim.Site",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="Site",
    )
    fqdn = models.CharField(max_length=50)
    oe_bu = models.CharField(max_length=50)
    owner_contact = models.EmailField()
    class_type = models.CharField(max_length=20, choices=ApplicationClassTypes)
    accessibility = models.CharField(max_length=20, choices=ApplicationAccessibility)
    test_url = models.URLField()

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
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for CustomerAppProfile memeber."""
        return reverse("plugins:lb_models:customerappprofile", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.profile_name,
            self.application_name,
            self.site,
            self.fqdn,
            self.oe_bu,
            self.owner_contact,
            self.class_type,
            self.accessibility,
            self.test_url,
        )

    def __str__(self):
        """Stringify instance."""
        return self.profile_name
