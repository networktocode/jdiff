"""Django API urlpatterns declaration for lb_models plugin."""

from nautobot.core.api import OrderedDefaultRouter

from lb_models.api import views

router = OrderedDefaultRouter()
router.register("certificate", views.CertificateViewSet)
router.register("viphealthmonitor", views.VIPHealthMonitorViewSet)
router.register("vippoolmember", views.VIPPoolMemberViewSet)
router.register("vippool", views.VIPPoolViewSet)
router.register("vip", views.VIPViewSet)


app_name = "lb_models-api"
urlpatterns = router.urls
