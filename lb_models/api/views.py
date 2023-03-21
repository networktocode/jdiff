"""API views for lb-models."""

from nautobot.core.api.views import ModelViewSet
from lb_models import filters, models
from lb_models.api import serializers


class CertificateViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Certificate serializer viewset."""

    serializer_class = serializers.CertificateSerializer
    filterset_class = filters.CertificateFilterSet
    queryset = models.Certificate.objects.all()


class HealthMonitorViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Health Monitor serializer viewset."""

    serializer_class = serializers.HealthMonitorSerializer
    filterset_class = filters.HealthMonitorFilterSet
    queryset = models.HealthMonitor.objects.all()


class ServiceGroupBindingViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Service Group Member viewset."""

    serializer_class = serializers.ServiceGroupBindingSerializer
    filterset_class = filters.ServiceGroupBindingFilterSet
    queryset = models.ServiceGroupBinding.objects.all()


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
