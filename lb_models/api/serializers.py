"""API serializers for fcc_dispatching."""

from nautobot.core.api.serializers import ValidatedModelSerializer

from lb_models import models

from . import nested_serializers
from nautobot.dcim.api import nested_serializers as dcim_nested_serializers
from nautobot.ipam.api import nested_serializers as ipam_nested_serializers


class VIPCertificateSerializer(ValidatedModelSerializer):
    """VIP Certificate Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.VIPCertificate
        fields = [
            "slug",
            "issuer",
            "version_number",
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


class VIPHealthMonitorSerializer(ValidatedModelSerializer):
    """VIP Health Monitor Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.VIPHealthMonitor
        fields = [
            "id",
            "slug",
            "name",
            "description",
            "type",
            "url",
            "send",
            "code",
            "receive",
        ]


class VIPPoolSerializer(ValidatedModelSerializer):
    """VIP Pool Serializer."""

    monitor = nested_serializers.VIPHealthMonitorNestedSerializer()
    member = nested_serializers.VIPPoolMemberNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIPPool
        fields = ["id", "slug", "name", "description", "monitor", "member"]


class VIPPoolMemberSerializer(ValidatedModelSerializer):
    """VIP Pool Member Serializer."""

    address = ipam_nested_serializers.NestedIPAddressSerializer()
    monitor = nested_serializers.VIPHealthMonitorNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIPPoolMember
        fields = [
            "id",
            "slug",
            "name",
            "description",
            "protocol",
            "port",
            "address",
            "fqdn",
            "monitor",
            "member_args",
        ]


class VIPSerializer(ValidatedModelSerializer):
    """VIP Serializer."""

    device = dcim_nested_serializers.NestedDeviceSerializer()
    interface = dcim_nested_serializers.NestedInterfaceSerializer()
    address = ipam_nested_serializers.NestedIPAddressSerializer()
    pool = nested_serializers.VIPPoolNestedSerializer()
    vlan = ipam_nested_serializers.NestedVLANSerializer()
    vrf = ipam_nested_serializers.NestedVRFSerializer()
    certificate = nested_serializers.VIPCertificateNestedSerializer()

    class Meta:
        """Meta attributes."""

        model = models.VIP
        fields = [
            "id",
            "slug",
            "name",
            "description",
            "device",
            "interface",
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
            "vip_args",
        ]
