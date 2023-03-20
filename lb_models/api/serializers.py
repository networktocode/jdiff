"""API serializers for LB Models."""

from nautobot.core.api.serializers import ValidatedModelSerializer

from lb_models import models

from . import nested_serializers
from nautobot.dcim.api import nested_serializers as dcim_nested_serializers
from nautobot.ipam.api import nested_serializers as ipam_nested_serializers


class CertificateSerializer(ValidatedModelSerializer):
    """Certificate Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Certificate
        fields = "__all__"


class HealthMonitorSerializer(ValidatedModelSerializer):
    """Health Monitor Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.HealthMonitor
        fields = "__all__"


class ServiceGroupBindingSerializer(ValidatedModelSerializer):
    """Service Group Member Serializer."""

    address = ipam_nested_serializers.NestedIPAddressSerializer()
    monitor = nested_serializers.HealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupBinding
        fields = "__all__"


class ServiceGroupSerializer(ValidatedModelSerializer):
    """Service Group Serializer."""

    member = nested_serializers.ServiceGroupBindingNestedSerializer()
    monitor = nested_serializers.HealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = "__all__"


class vserverSerializer(ValidatedModelSerializer):
    """vserver Serializer."""

    device = dcim_nested_serializers.NestedDeviceSerializer()
    interface = dcim_nested_serializers.NestedInterfaceSerializer()
    address = ipam_nested_serializers.NestedIPAddressSerializer()
    pool = nested_serializers.ServiceGroupNestedSerializer()
    vlan = ipam_nested_serializers.NestedVLANSerializer()
    vrf = ipam_nested_serializers.NestedVRFSerializer()
    certificate = nested_serializers.CertificateNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.vserver
        fields = "__all__"
