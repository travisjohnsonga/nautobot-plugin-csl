# Cisco Smart Licensing

This plugin links to Cisco Smart Licensing API to display smart licensing usage.

## Installation

To install this example plugin from this directory run this command:

```no-highlight
pip install .
```

And then add it to your `PLUGINS` setting in your `nautobot_config.py`:

```python
PLUGINS = [
    "cisco_smart_licensing",
]
```

Required configuration in `PLUGIN_CONFIG` 
```
PLUGINS_CONFIG = {
    'cisco_smart_licensing': {
        'SMART_LICENSE_CLIENT_ID': os.getenv("SMART_LICENSE_CLIENT_ID", ""),
        'SMART_LICENSE_CLIENT_SECRET': os.getenv("SMART_LICENSE_CLIENT_SECRET", ""),
        'SMART_LICENSE_ACCOUNT': os.getenv("SMART_LICENSE_ACCOUNT","abc.com"),
        'SMART_LICENSE_SOURCE_VIRTUAL_ACCOUNT': os.getenv("SMART_LICENSE_SOURCE_VIRTUAL_ACCOUNT", "default"),
        #A list of location types, for all location types, use '*'
        'SMART_LICENSE_LOCATION_TYPES':['']
    }
}
```

## Virtual Account Setup

To use this plugin, the virtual account's should be configured in the format of stateFacility

Examle tx1234

This may be fixed later to add a field for storing the virtual account name, but this is how I started out with it in the place that pays my paychecks.

## Jobs

### Balance Smart Licenses

Licenses from the `SMART_LICENSE_SOURCE_VIRTUAL_ACCOUNT` and move them to the facility level virtual account.  If the facility level virtual account has extra licenses, the job will move the overage back to the `SMART_LICENSE_SOURCE_VIRTUAL_ACCOUNT`

### Generate Smart Tokens

This generates Smart Licenses and stores in a location custom field call `SMART_LICENSE_TOKEN`
This is mainly for use with ansible to handle smart licensing, but also to allow staff to access a token without having to have access to the smart license portal.
