"""Filtering for lb_models."""
import django_filters
from nautobot.utilities.filters import BaseFilterSet, NameSlugSearchFilterSet
from django.db.models import Q
from lb_models import models


class SSLCertKeyFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for SSLCertKey."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.SSLCertKey
        fields = [
            "q",
            "slug",
            "name",
            "private_key_filename",
            "private_crt_filename",
            "password",
            "snow_id",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(private_key_filename__icontains=value)
            | Q(private_crt_filename__icontains=value)
            | Q(name__icontains=value)
            | Q(snow_id__icontains=value)
        )
        return queryset.filter(qs_filter)


class SSLServerBindingFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for SSLServerBinding."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    ssl_certkey = django_filters.ModelMultipleChoiceFilter(
        queryset=models.SSLCertKey.objects.all(),
        label="SSL Certkey",
    )
    vserver = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Vserver.objects.all(),
        label="VServer",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.SSLServerBinding
        fields = [
            "q",
            "slug",
            "name",
            "ssl_certkey",
            "vserver",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(ssl_certkey__icontains=value) | Q(vserver__icontains=value)
        return queryset.filter(qs_filter)


class ServiceGroupMemberBindingFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for ServiceGroupMemberBinding."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    server_name = django_filters.ModelMultipleChoiceFilter(
        queryset=models.Server.objects.all(),
        label="Server",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "q",
            "slug",
            "server_name",
            "server_port",
            "name",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(server_name__icontains=value)
            | Q(server_port__icontains=value)
            | Q(name__icontains=value)
        )
        return queryset.filter(qs_filter)


class ServiceGroupMonitorBindingFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for ServiceGroupMonitorBinding."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupMonitorBinding.objects.all(),
        label="Monitor",
    )
    service_group = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroup.objects.all(),
        label="Service Group",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "q",
            "slug",
            "name",
            "monitor",
            "service_group",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(protocol__icontains=value)
            | Q(port__icontains=value)
            | Q(address__icontains=value)
            | Q(fqdn__icontains=value)
            | Q(monitor__icontains=value)
        )
        return queryset.filter(qs_filter)


class MonitorFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Monitor."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.Monitor
        fields = ["q", "slug", "name", "comment", "type", "lrtm", "args", "snow_id"]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(comment__icontains=value)
            | Q(type__icontains=value)
            | Q(snow_id__icontains=value)
        )
        return queryset.filter(qs_filter)


class ServiceGroupFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Service Group."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupMonitorBinding.objects.all(),
        label="Monitor",
    )
    service_group_member = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupMemberBinding.objects.all(),
        label="Service Group Member Binding",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroup
        fields = [
            "q",
            "slug",
            "name",
            "comment",
            "service_group_member",
            "service_type",
            "monitor",
            "ssl_profile",
            "snow_id",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(comment__icontains=value)
            | Q(monitor__icontains=value)
            | Q(service_group_member__icontains=value)
            | Q(type__icontains=value)
            | Q(name__icontains=value)
            | Q(ssl_profile__icontains=value)
        )
        return queryset.filter(qs_filter)


class VserverFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for vserver."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

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
            "td"
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(device__icontains=value)
            | Q(interface__icontains=value)
            | Q(address__icontains=value)
            | Q(pool__icontains=value)
            | Q(vlan__icontains=value)
            | Q(vrf__icontains=value)
            | Q(fqdn__icontains=value)
            | Q(protocol__icontains=value)
            | Q(port__icontains=value)
            | Q(method__icontains=value)
            | Q(sslcertkey__icontains=value)
            | Q(owner__icontains=value)
            | Q(td__icontains=value)
        )
        return queryset.filter(qs_filter)


class ServerFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Server."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.Server
        fields = ["slug", "name", "state", "ipv4_address", "td"]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(state__icontains=value)
            | Q(ipv4_address__icontains=value)
            | Q(td__icontains=value)
        )
        return queryset.filter(qs_filter)


class CustomerAppProfileFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for CustomerAppProfile."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

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

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(application_name__icontains=value)
            | Q(profile_name__icontains=value)
            | Q(site__icontains=value)
            | Q(fqdn__icontains=value)
            | Q(oe_bu__icontains=value)
            | Q(owner_contact__icontains=value)
            | Q(class_type__icontains=value)
            | Q(accessibility__icontains=value)
            | Q(test_url__icontains=value)
        )
        return queryset.filter(qs_filter)


class ServerServiceGroupBindingFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Server Service Group Binding."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServerServiceGroupBinding
        fields = [
            "slug",
            "name",
            "service_group",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(id__icontains=value) | Q(ame__icontains=value) | Q(service_group__icontains=value)
        return queryset.filter(qs_filter)


class ServiceGroupMonitorBindingFilterForm(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Server Service Group Binding."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroupMonitorBinding
        fields = [
            "slug",
            "name",
            "monitor",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(id__icontains=value) | Q(name__icontains=value) | Q(monitor__icontains=value)
        return queryset.filter(qs_filter)
