"""Filtering for lb_models."""
import django_filters
from nautobot.utilities.filters import BaseFilterSet, NameSlugSearchFilterSet
from django.db.models import Q
from lb_models import models
from versionfield import VersionField


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
