from nautobot.extras.plugins import PluginConfig

class CiscoSmartLicensing(PluginConfig):
    name = 'cisco_smart_licensing'
    verbose_name = 'Cisco Smart Licensing'
    description = 'A utility for managing Cisco Smart Licensing'
    version = '0.1'
    author = 'Travis Johnson'
    author_email = 'travisjohnsonga@gmail.com'
    base_url = 'cisco-smart-licensing'
    required_settings = ["SMART_LICENSE_TOKEN","SMART_LICENSE_SECRET"]
    default_settings = {
        'loud': False
    }

config = CiscoSmartLicensing