"""Template content for nautobot_data_validation_engine."""
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension

from nautobot.extras.utils import registry


def tab_factory(content_type_label):
    """Generate a CiscoSmartLicenseTab object for a given content type."""

    class CiscoSmartLicenseTab(TemplateExtension):  # pylint: disable=W0223
        """Dynamically generated DataComplianceTab class."""

        model = content_type_label

        def detail_tabs(self):
            return [
                {
                    "title": "Cisco Smart Licensing",
                    "url": reverse(
                        "plugins:cisco_smart_licensing:smart_license_detail_tab",
                        kwargs={"id": self.context["object"].id, "model": self.model},
                    ),
                },
            ]

    return CiscoSmartLicenseTab