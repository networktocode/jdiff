"""Django API urlpatterns declaration for lb_models plugin."""

from nautobot.core.api import OrderedDefaultRouter

from lb_models.api import views

router = OrderedDefaultRouter()
router.register("sslcertkey", views.SSLCertKeyViewSet)
router.register("monitor", views.MonitorViewSet)
router.register("servicegroupmemberbinding", views.ServiceGroupMemberBindingViewSet)
router.register("servicegroup", views.ServiceGroupViewSet)
router.register("vserver", views.vserverViewSet)


app_name = "lb_models-api"
urlpatterns = router.urls
