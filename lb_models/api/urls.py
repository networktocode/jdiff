"""Django API urlpatterns declaration for lb_models plugin."""

from nautobot.core.api import OrderedDefaultRouter

from lb_models.api import views

router = OrderedDefaultRouter()
router.register("certificate", views.CertificateViewSet)
router.register("healthmonitor", views.HealthMonitorViewSet)
router.register("servicegroupbinding", views.ServiceGroupBindingViewSet)
router.register("servicegroup", views.ServiceGroupViewSet)
router.register("vserver", views.vserverViewSet)


app_name = "lb_models-api"
urlpatterns = router.urls
