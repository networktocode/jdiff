"""API nested serializers for LB Models."""
from rest_framework import serializers

from nautobot.core.api import WritableNestedSerializer
from nautobot.ipam.api import nested_serializers as ipam_nested_serializers

from lb_models import models


class HealthMonitorNestedSerializer(WritableNestedSerializer):
    """Health Monitor Nested Serializer."""

    monitor = serializers.CharField(source="name")

    class Meta:
        """Meta attributes."""

        model = models.HealthMonitor
        fields = ["monitor"]


class ServiceGroupBindingNestedSerializer(WritableNestedSerializer):
    """Service Group Member Nested Serializer."""

    member = serializers.CharField(source="name")
    monitor = HealthMonitorNestedSerializer()
    address = ipam_nested_serializers.NestedIPAddressSerializer()

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupBinding
        fields = ["member", "monitor", "address"]


class ServiceGroupNestedSerializer(WritableNestedSerializer):
    """Service Group Nested Serializer."""

    pool = serializers.CharField(source="name")
    member = ServiceGroupBindingNestedSerializer()
    monitor = HealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = ["pool", "member", "monitor"]


class CertificateNestedSerializer(WritableNestedSerializer):
    """Certificate Nested Serializer."""

    certificate = serializers.CharField(source="name")

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = ["certificate"]
