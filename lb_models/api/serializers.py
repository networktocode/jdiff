"""API serializers for LB Models."""

from nautobot.core.api.serializers import ValidatedModelSerializer

from lb_models import models

from . import nested_serializers
from nautobot.dcim.api import nested_serializers as dcim_nested_serializers
from nautobot.ipam.api import nested_serializers as ipam_nested_serializers


class SSLCertKeySerializer(ValidatedModelSerializer):
    """SSLCertKey Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.SSLCertKey
        fields = "__all__"


class MonitorSerializer(ValidatedModelSerializer):
    """Monitor Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Monitor
        fields = "__all__"


class ServiceGroupMemberBindingSerializer(ValidatedModelSerializer):
    """Service Group Member Serializer."""

    address = ipam_nested_serializers.NestedIPAddressSerializer()
    monitor = nested_serializers.MonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroupMemberBinding
        fields = "__all__"


class ServiceGroupSerializer(ValidatedModelSerializer):
    """Service Group Serializer."""

    member = nested_serializers.ServiceGroupMemberBindingNestedSerializer()

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
    sslcertkey = nested_serializers.SSLCertKeyNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.Vserver
        fields = "__all__"
