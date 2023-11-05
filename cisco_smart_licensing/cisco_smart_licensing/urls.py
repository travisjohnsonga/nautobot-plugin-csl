from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

from nautobot.apps.urls import NautobotUIViewSetRouter
from . import views


app_name = "cisco_smart_licensing"
router = NautobotUIViewSetRouter()

urlpatterns = [
    
    path(
        "location/<uuid:pk>/location_smart_license_detail_tab/", views.LocationSmartLicenseTab.as_view(), name="location_smart_license_detail_tab")  
]
urlpatterns += router.urls
