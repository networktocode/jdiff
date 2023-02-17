"""Filtering for lb_models."""
import django_filters
from nautobot.utilities.filters import BaseFilterSet, NameSlugSearchFilterSet
from django.db.models import Q
from lb_models import models


class VIPCertificateFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for VIPCertificate."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.VIPCertificate
        fields = [
            "q",
            "slug",
            "issuer",
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

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(issuer__icontains=value)
            | Q(serial_number__icontains=value)
            | Q(signature_algorithm__icontains=value)
            | Q(signature_algorithm_id__icontains=value)
            | Q(subject_name__icontains=value)
            | Q(subject_pub_key__icontains=value)
            | Q(subject_pub_key_algorithm__icontains=value)
        )
        return queryset.filter(qs_filter)


class VIPPoolMemberFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for VIPPoolMember."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.VIPPoolMember.objects.all(),
        label="Monitor",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.VIPPoolMember
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


class VIPHealthMonitorFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for VIPHealthMonitor."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.VIPHealthMonitor
        fields = ["q", "slug", "name", "description", "type", "url", "send", "receive", "code", "string"]

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
        )
        return queryset.filter(qs_filter)


class VIPPoolFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for VIP Pool."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    monitor = django_filters.ModelMultipleChoiceFilter(
        queryset=models.VIPHealthMonitor.objects.all(),
        label="Monitor",
    )
    member = django_filters.ModelMultipleChoiceFilter(
        queryset=models.VIPPoolMember.objects.all(),
        label="Member",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.VIPPool
        fields = ["q", "slug", "name", "description", "monitor", "member"]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(monitor__icontains=value)
            | Q(member__icontains=value)
        )
        return queryset.filter(qs_filter)


class VIPFilterSet(BaseFilterSet, NameSlugSearchFilterSet):
    """Filter for VIP."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.VIP
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
