"""API views for lb-models."""

from nautobot.core.api.views import ModelViewSet
from lb_models import filters, models
from lb_models.api import serializers


class SSLCertKeyViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """SSLCertKey serializer viewset."""

    serializer_class = serializers.SSLCertKeySerializer
    filterset_class = filters.SSLCertKeyFilterSet
    queryset = models.SSLCertKey.objects.all()


class MonitorViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Monitor serializer viewset."""

    serializer_class = serializers.MonitorSerializer
    filterset_class = filters.MonitorFilterSet
    queryset = models.Monitor.objects.all()


class ServiceGroupMemberBindingViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Service Group Member viewset."""

    serializer_class = serializers.ServiceGroupMemberBindingSerializer
    filterset_class = filters.ServiceGroupMemberBindingFilterSet
    queryset = models.ServiceGroupMemberBinding.objects.all()


class ServiceGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Service Group viewset."""

    serializer_class = serializers.ServiceGroupSerializer
    filterset_class = filters.ServiceGroupFilterSet
    queryset = models.ServiceGroup.objects.all()


class vserverViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """vserver viewset."""

    serializer_class = serializers.vserverSerializer
    filterset_class = filters.VserverFilterSet
    queryset = models.Vserver.objects.all()
