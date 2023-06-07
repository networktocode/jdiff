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
    Methods,
    PersistenceType,
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
    name = models.CharField(max_length=50, null=True)
    private_key_filename = models.CharField(max_length=100, null=True)
    private_crt_filename = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    snow_id = models.CharField(max_length=20, null=True)

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
    name = models.CharField(max_length=50, null=True)
    ssl_certkey = models.OneToOneField(SSLCertKey, on_delete=models.CASCADE)

    fields = [
        "slug",
        "name",
        "ssl_certkey",
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
    name = models.CharField(max_length=50, null=True)
    server_port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(0)], null=True)
    server_name = models.ForeignKey(to="Server", on_delete=models.CASCADE)

    fields = [
        "slug",
        "name",
        "server_port",
        "server_name",
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
            self.server_port,
            self.server_name,
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
    name = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20, choices=MonitorTypes)
    lrtm = models.BooleanField(default=False)
    snow_id = models.CharField(max_length=20, null=True)
    args = models.JSONField(blank=True, null=True)

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
    monitor = models.ForeignKey(to="Monitor", on_delete=models.CASCADE)

    fields = [
        "slug",
        "name",
        "monitor",
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
    name = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    service_group_member = models.ForeignKey(to="ServiceGroupMemberBinding", on_delete=models.PROTECT, null=True)
    monitor = models.ForeignKey(to="ServiceGroupMonitorBinding", on_delete=models.PROTECT, null=True)
    service_type = models.CharField(max_length=20, choices=ServiceGroupTypes, null=True)
    ssl_profile = models.CharField(max_length=50, null=True)
    snow_id = models.CharField(max_length=20, null=True)

    fields = ["slug", "name", "comment", "service_group_member", "service_type", "monitor", "ssl_profile", "snow_id"]
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
            self.service_group_member,
            self.service_type,
            self.monitor,
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
    name = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=50, blank=True, null=True)
    device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        verbose_name="Device",
    )
    ipv4_address = models.ForeignKey(
        to="ipam.IPAddress", on_delete=models.CASCADE, verbose_name="Member Address", null=True
    )

    service_group_binding = models.ForeignKey(to="ServerServiceGroupBinding", on_delete=models.PROTECT, null=True)
    service_type = models.CharField(max_length=20, choices=ServiceGroupTypes, null=True)
    lb_method = models.CharField(max_length=20, choices=Methods, null=True)
    ssl_binding = models.ForeignKey(to="SSLServerBinding", on_delete=models.CASCADE, null=True)
    customer_app_profile = models.ForeignKey(to="CustomerAppProfile", on_delete=models.CASCADE, null=True)
    ssl_profile = models.CharField(max_length=50, null=True)
    persistence_type = models.CharField(max_length=20, choices=PersistenceType, null=True)
    args = models.JSONField(blank=True, null=True)
    snow_id = models.CharField(max_length=20, null=True)
    td = models.PositiveSmallIntegerField(MinValueValidator=1,  MaxValueValidator=32767, null=True)

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
        "td"
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
            self.comment,
            self.device,
            self.ipv4_address,
            self.service_group_binding,
            self.service_type,
            self.lb_method,
            self.ssl_binding,
            self.customer_app_profile,
            self.ssl_profile,
            self.persistence_type,
            self.args,
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
class CustomerAppProfile(OrganizationalModel):
    """CustomerAppProfile model implementation."""

    slug = AutoSlugField(populate_from="profile_name")
    profile_name = models.CharField(max_length=50, null=True)
    application_name = models.CharField(max_length=50, null=True)
    site = models.ForeignKey(to="dcim.Site", on_delete=models.PROTECT, related_name="+", verbose_name="Site", null=True)
    fqdn = models.CharField(max_length=50, null=True)
    oe_bu = models.CharField(max_length=50, null=True)
    owner_contact = models.EmailField(null=True)
    class_type = models.CharField(max_length=20, choices=ApplicationClassTypes, null=True)
    accessibility = models.CharField(max_length=20, choices=ApplicationAccessibility, null=True)
    test_url = models.URLField(null=True)

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
class Server(PrimaryModel):
    """Server model implementation."""

    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=50, null=True)
    state = models.BooleanField(default=False)
    ipv4_address = models.ForeignKey(
        to="ipam.IPAddress",
        on_delete=models.CASCADE,
        verbose_name="IPv4 Server Address",
    )
    td = models.IntegerField(null=True)

    fields = ["slug", "name", "state", "ipv4_address", "td"]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Monitor."""
        return reverse("plugins:lb_models:server", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (self.slug, self.name, self.state, self.ipv4_address, self.td)

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
class ServerServiceGroupBinding(PrimaryModel):
    """Server Service Group Binding response model implementation."""

    slug = AutoSlugField(populate_from="name")
    service_group = models.ForeignKey(to="ServiceGroup", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)

    fields = [
        "slug",
        "name",
        "service_group",
    ]
    csv_headers = fields
    clone_fields = fields

    def get_absolute_url(self):
        """Return detail view for Server Service Group Binding."""
        return reverse("plugins:lb_models:serverservicegroupbinding", args=[self.slug])

    def to_csv(self):
        """To CSV format."""
        return (
            self.slug,
            self.name,
            self.service_group,
        )

    def __str__(self):
        """Stringify instance."""
        return self.name
