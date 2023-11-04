from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

from nautobot.apps.urls import NautobotUIViewSetRouter
from nautobot.apps.views import ObjectDynamicGroupsView

from . import views


app_name = "cisco_smart_licensing"
router = NautobotUIViewSetRouter()
router.register("cisco-smart-license", views.CiscoSmartLicenseLocationUIViewSet)
urlpatterns = [
    
    path(
        "docs/",
        RedirectView.as_view(url=static("cisco_smart_licensing/docs/index.html")),
        name="docs",
    ),    
]
urlpatterns += router.urls
