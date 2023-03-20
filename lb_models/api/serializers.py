"""API serializers for LB Models."""

from nautobot.core.api.serializers import ValidatedModelSerializer

from lb_models import models

from . import nested_serializers
from nautobot.dcim.api import nested_serializers as dcim_nested_serializers
from nautobot.ipam.api import nested_serializers as ipam_nested_serializers


class CertificateSerializer(ValidatedModelSerializer):
    """VIP Certificate Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = "__all__"


class VIPHealthMonitorSerializer(ValidatedModelSerializer):
    """VIP Health Monitor Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = "__all__"


class VIPPoolMemberSerializer(ValidatedModelSerializer):
    """VIP Pool Member Serializer."""

    address = ipam_nested_serializers.NestedIPAddressSerializer()
    monitor = nested_serializers.VIPHealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = "__all__"


class VIPPoolSerializer(ValidatedModelSerializer):
    """VIP Pool Serializer."""

    member = nested_serializers.VIPPoolMemberNestedSerializer()
    monitor = nested_serializers.VIPHealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = "__all__"


class VIPSerializer(ValidatedModelSerializer):
    """VIP Serializer."""

    device = dcim_nested_serializers.NestedDeviceSerializer()
    interface = dcim_nested_serializers.NestedInterfaceSerializer()
    address = ipam_nested_serializers.NestedIPAddressSerializer()
    pool = nested_serializers.VIPPoolNestedSerializer()
    vlan = ipam_nested_serializers.NestedVLANSerializer()
    vrf = ipam_nested_serializers.NestedVRFSerializer()
    certificate = nested_serializers.CertificateNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIP
        fields = "__all__"
