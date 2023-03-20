"""API views for lb-models."""

from nautobot.core.api.views import ModelViewSet
from lb_models import filters, models
from lb_models.api import serializers


class CertificateViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """VIP Certificate serializer viewset."""

    serializer_class = serializers.CertificateSerializer
    filterset_class = filters.CertificateFilterSet
    queryset = models.Certificate.objects.all()


class VIPHealthMonitorViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """VIP Health Monitor serializer viewset."""

    serializer_class = serializers.VIPHealthMonitorSerializer
    filterset_class = filters.VIPHealthMonitorFilterSet
    queryset = models.VIPHealthMonitor.objects.all()


class VIPPoolMemberViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """VIP Pool Member viewset."""

    serializer_class = serializers.VIPPoolMemberSerializer
    filterset_class = filters.VIPPoolMemberFilterSet
    queryset = models.VIPPoolMember.objects.all()


class VIPPoolViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """VIP Pool viewset."""

    serializer_class = serializers.VIPPoolSerializer
    filterset_class = filters.VIPPoolFilterSet
    queryset = models.VIPPool.objects.all()


class VIPViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """VIP viewset."""

    serializer_class = serializers.VIPSerializer
    filterset_class = filters.VIPFilterSet
    queryset = models.VIP.objects.all()
