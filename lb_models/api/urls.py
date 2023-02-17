"""Django API urlpatterns declaration for lb_models plugin."""

from nautobot.core.api import OrderedDefaultRouter

from lb_models.api import views

router = OrderedDefaultRouter()
router.register("vipcertificate", views.VIPCertificateViewSet)
router.register("viphealtmonitor", views.VIPHealthMonitorViewSet)
router.register("vippool", views.VIPPoolViewSet)
router.register("vippoolmember", views.VIPPoolMemberViewSet)
# router.register("vip", views.VIPViewSet)


app_name = "lb_models-api"
urlpatterns = router.urls
