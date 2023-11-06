from django.shortcuts import HttpResponse, render
from django.views.generic import View
import requests, json, datetime

from django.shortcuts import HttpResponse, render
from django.views.generic import View
from django.conf import settings

from nautobot.apps import views
from nautobot.dcim.models import Location

PLUGIN_CFG = settings.PLUGINS_CONFIG.get("CISCO_SMART_LICENSING", {})

class csl:
    

     
    
    def __init__(self, client_id = None, client_secret = None):
        self.client_id = PLUGIN_CFG.get("SMART_LICENSE_CLIENT_ID")
        self.client_secret = PLUGIN_CFG.get("SMART_LICENSE_CLIENT_SECRET")
        self.oauth_token = None
        self.oauth_token_type = None
        self.oauth_token_expires = None
        self.token_timestamp = None
        self.account = PLUGIN_CFG.get("SMART_LICENSE_ACCOUNT")
        self.source_virtual_account = PLUGIN_CFG.get("SMART_LICENSE_SOURCE_VIRTUAL_ACCOUNT")

    def GetAuthToken(self):
        url = 'https://cloudsso.cisco.com/as/token.oauth2'
        payload = 'grant_type=client_credentials&client_id=' + str(self.client_id) + '&client_secret=' + str(self.client_secret)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        json_response = json.loads(response.content)
        
        self.oauth_token = json_response['access_token']
        self.oauth_token_type = json_response['token_type']
        self.oauth_token_expires = json_response['expires_in']
        
        
    def GetVirtualAccounts(self):
        if self.oauth_token == None:
            self.GetAuthToken()
            
        url = f'https://swapi.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{self.account}/CUSTOMER/virtual-accounts'
        headers = {
            'Authorization': 'Bearer ' + self.oauth_token,
                }
        response = requests.request('GET', url=url, headers=headers)
        json_response = json.loads(response.content)
        return json_response
    
    def CreateVirtualAccount(self, acct_name, acct_description):
        url = f"https://swapi.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{self.account}/CUSTOMER/virtual-accounts"

        payload = json.dumps({
        "name": acct_name,
        "description": acct_description,
        "isDefault": "false",
        "commerceAccessLevel": "PUBLIC"
        })
        headers = {
        'Authorization': 'Bearer ' + self.oauth_token,
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload) 
        json_response = json.loads(response.content)
        return json_response
    
    def TransferLicense(self, source_va, target_va, lic_type, qty):
        url = f'https://swapi.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{self.account}/virtual-accounts/' + source_va + '/licenses/transfer'
        payload = json.dumps({
            "licenses": [
                {
                "license": lic_type.split(':')[0],
                "licenseType":lic_type.split(':')[1],
                "quantity": qty,
                "targetVirtualAccount": target_va,
                "precedence": "LONGEST_TERM_FIRST"
                }
            ]
            })
        print(payload)
        headers = {
            'Authorization': 'Bearer ' + self.oauth_token,
            'Content-Type': 'application/json',
            }
        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = json.loads(response.content)
        return json_response
    
    def GetRegistrationTokens(self, virtual_account):
        url = f'https://swapi.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{self.account}/virtual-accounts/' + virtual_account +'/tokens'
        headers = {
            'Authorization': 'Bearer ' + self.oauth_token,
            'Content-Type': 'application/json',
            }
        response = requests.request('GET', url=url, headers=headers)
        json_response = json.loads(response.content)
        return json_response
    
    def CreateRegistrationToken(self, virtual_account):
        url = f'https://swapi.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{self.account}/virtual-accounts/' + virtual_account +'/tokens'

        payload = json.dumps({
        "description": "devregtoken",
        "expiresAfterDays": 1,
        "exportControlled": "Allowed"
        })
        headers = {
            'Authorization': 'Bearer ' + self.oauth_token,
            'Content-Type': 'application/json',
            }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = json.loads(response.content)
        return json_response
    
    def GetVALicense(self, virt_acct):
        url = f'https://swapi.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{self.account}/licenses'
        payload = json.dumps({
            "virtualAccounts": 
                virt_acct
            ,
            "limit": 500,
            "offset": 0
            })
        print(payload)
        headers = {
        'Authorization': 'Bearer ' + self.oauth_token,
        'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            json_response = response.json()['licenses']
            return json_response
        else:
            return None

class LocationSmartLicenseTab(views.ObjectView):
    """
    This view's template extends the circuit detail template,
    making it suitable to show as a tab on the circuit detail page.

    Views that are intended to be for an object detail tab's content rendering must
    always inherit from nautobot.apps.views.ObjectView.
    """
    
  
    queryset = Location.objects.all()
    template_name = "cisco_smart_licensing/location_tab.html"
    print(queryset)
    def get_extra_context(self, request, instance):

        print(f'UUID PK IS {self.kwargs["pk"]}')
        print(f'INSTANCE IS {instance}')
        print(f'REQUEST IS {request}')
        print(f'PK IS {self.kwargs}')

        loc_data = Location.objects.get(pk=self.kwargs["pk"])
        location_virtual_account = f'{loc_data.cf["state"]}{loc_data.facility}'
       
        cslclient = csl()
        virtual_accounts =[]
        virtual_accounts.append(location_virtual_account)
        print(virtual_accounts)
        cslclient.GetAuthToken()
        licenses = cslclient.GetVALicense(virtual_accounts)

        print(licenses)
        return {
            "licenses": licenses,
        }