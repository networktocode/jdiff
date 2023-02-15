"""API nested serializers for fcc_dispatching."""
from rest_framework import serializers

from nautobot.core.api import WritableNestedSerializer

from lb_models import models


class VIPPoolMemberNestedSerializer(WritableNestedSerializer):
    """VIP Pool Member Nested Serializer."""

    pool = serializers.CharField(source="name")

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = "__all__"

class VIPPoolNestedSerializer(WritableNestedSerializer):
    """VIP Pool Nested Serializer."""

    pool = serializers.CharField(source="name")

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = "__all__"


class VIPCertificateNestedSerializer(WritableNestedSerializer):
    """VIP Certificate Nested Serializer."""

    certificate = serializers.CharField(source="serial_number")

    class Meta:
        """Meta attributes."""

        model = models.VIPCertificate
        fields = "__all__"


class VIPHealthMonitorNestedSerializer(WritableNestedSerializer):
    """Team Nested Serializer."""

    monitor = serializers.CharField(source="name")

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = "__all__"
