"""Filtering for lb_models."""
import django_filters
from nautobot.utilities.filters import BaseFilterSet, NameSlugSearchFilterSet
from django.db.models import Q
from lb_models import models


class CertificateFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Certificate."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.Certificate
        fields = [
            "q",
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

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(issuer__icontains=value)
            | Q(serial_number__icontains=value)
            | Q(version_number__icontains=value)
            | Q(name__icontains=value)
            | Q(key__icontains=value)
        )
        return queryset.filter(qs_filter)


class ServiceGroupBindingFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for ServiceGroupBinding."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupBinding.objects.all(),
        label="Monitor",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroupBinding
        fields = [
            "q",
            "slug",
            "name",
            "description",
            "protocol",
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


class HealthMonitorFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for HealthMonitor."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.HealthMonitor
        fields = [
            "q",
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

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(type__icontains=value)
            | Q(url__icontains=value)
            | Q(send__icontains=value)
            | Q(recevier__icontains=value)
            | Q(httprequest__icontains=value)
        )
        return queryset.filter(qs_filter)


class ServiceGroupFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Service Group."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.HealthMonitor.objects.all(),
        label="Monitor",
    )
    member = django_filters.ModelMultipleChoiceFilter(
        queryset=models.ServiceGroupBinding.objects.all(),
        label="Member",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroup
        fields = ["q", "slug", "name", "description", "monitor", "member", "type", "td", "sslprofile"]

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
            | Q(sslprofile__icontains=value)
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
            "certificate",
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
            | Q(certificate__icontains=value)
            | Q(owner__icontains=value)
        )
        return queryset.filter(qs_filter)


class CustomerFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for Customer."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.Customer
        fields = ["slug", "id", "site", "name", "fqdn", "oe", "email", "class_type", "accessibility", "test_url"]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(site__icontains=value)
            | Q(name__icontains=value)
            | Q(fqdn__icontains=value)
            | Q(oe__icontains=value)
            | Q(email__icontains=value)
            | Q(class_type__icontains=value)
            | Q(accessibility__icontains=value)
            | Q(test_url__icontains=value)
        )
        return queryset.filter(qs_filter)
