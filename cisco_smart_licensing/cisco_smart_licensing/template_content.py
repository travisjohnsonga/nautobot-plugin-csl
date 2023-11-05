"""Template content for nautobot_data_validation_engine."""
from django.urls import reverse
from nautobot.extras.plugins import TemplateExtension


class CiscoSmartLicenseTab(TemplateExtension):  # pylint: disable=W0223
    """Dynamically generated DataComplianceTab class."""

    model = "dcim.location"

    def detail_tabs(self):
            """
            You may define extra tabs to render on a model's detail page by utilizing this method.
            Each tab is defined as a dict in a list of dicts.

            For each of the tabs defined:
            - The <title> key's value will become the tab link's title.
            - The <url> key's value is used to render the HTML link for the tab.

            Since the `model` attribute of this class is set as "circuits.circuit",
            these tabs will be added to the Circuit model's detail page.

            This example demonstrates defining one tab.
            """
            return [
                {
                    "title": "Cisco Smart Licensing",
                    "url": reverse("plugins:cisco_smart_licensing:location_smart_license_detail_tab", kwargs={"pk": self.context["object"].pk}),
                },
            ]

template_extensions = [CiscoSmartLicenseTab]