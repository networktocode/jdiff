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
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupMemberBinding.objects.all(),
        label="Monitor",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroupMemberBinding
        fields = [
            "q",
            "slug",
            "name",
            "port",
            "address",
            "fqdn",
            "monitor",
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
            "port",
            "address",
            "fqdn",
            "monitor",
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
    member = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupMemberBinding.objects.all(),
        label="Member",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroup
        fields = ["q", "slug", "name", "comment", "member", "service_type", "td", "ssl_profile", "snow_id"]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(monitor__icontains=value)
            | Q(member__icontains=value)
            | Q(type__icontains=value)
            | Q(td__icontains=value)
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
            "description",
            "device",
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
