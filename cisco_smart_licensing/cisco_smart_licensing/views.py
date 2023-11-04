from django.shortcuts import HttpResponse, render
from django.views.generic import View
import requests, json, datetime

import yaml
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, ExpressionWrapper, F, FloatField, Max, Q
from django.shortcuts import redirect, render
from django.urls import reverse

from django.utils.html import format_html
from django.utils.timezone import make_aware
from django.views.generic import View
from django_pivot.pivot import pivot
from nautobot.apps import views
from nautobot.core.views import generic
from nautobot.core.views.mixins import ObjectPermissionRequiredMixin, PERMISSIONS_ACTION_MAP
from nautobot.dcim.models import Device
from nautobot.extras.models import Job, JobResult
#from rest_framework.decorators import action
#from rest_framework.response import Response
class csl:
    def __init__(self, client_id = None, client_secret = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = None
        self.oauth_token_type = None
        self.oauth_token_expires = None
        self.token_timestamp = None
        self.account = ''
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
        print(response.content)
        json_response = response.json()['licenses']
        print(json_response)
        return json_response

class CiscoSmartLicenseLocationUIViewSet(views.ObjectDetailViewMixin,
    views.ObjectDestroyViewMixin,
    views.ObjectBulkDestroyViewMixin,
    views.ObjectListViewMixin,
    ):

    #@action(detail=True, methods=["get"])
    def locatontab(self,request, pk, *args, **kwargs):
        smart_license = csl()
        smart_license.client_id = 'id'
        smart_license.client_secret = 'secret'

        smart_license.GetAuthToken()
        licenses = smart_license.GetVALicense(virt_acct=['va'])
        
        context = {}
        context['licenses'] = licenses
        context["active_tab"] = request.GET.get("tab")
        return render(request, "cisco_smart_licensing/location_tab.html")
