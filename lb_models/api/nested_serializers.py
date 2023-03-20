"""API nested serializers for LB Models."""
from rest_framework import serializers

from nautobot.core.api import WritableNestedSerializer
from nautobot.ipam.api import nested_serializers as ipam_nested_serializers

from lb_models import models


class VIPHealthMonitorNestedSerializer(WritableNestedSerializer):
    """Health Monitor Nested Serializer."""

    monitor = serializers.CharField(source="name")

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = ["monitor"]


class VIPPoolMemberNestedSerializer(WritableNestedSerializer):
    """VIP Pool Member Nested Serializer."""

    member = serializers.CharField(source="name")
    monitor = VIPHealthMonitorNestedSerializer()
    address = ipam_nested_serializers.NestedIPAddressSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = ["member", "monitor", "address"]


class VIPPoolNestedSerializer(WritableNestedSerializer):
    """VIP Pool Nested Serializer."""

    pool = serializers.CharField(source="name")
    member = VIPPoolMemberNestedSerializer()
    monitor = VIPHealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = ["pool", "member", "monitor"]


class CertificateNestedSerializer(WritableNestedSerializer):
    """VIP Certificate Nested Serializer."""

    certificate = serializers.CharField(source="serial_number")

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = ["certificate"]
