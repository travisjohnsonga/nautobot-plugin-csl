import sys
import time

from django.conf import settings
from django.db import transaction

from nautobot.apps.jobs import (
    DryRunVar,
    IntegerVar,
    Job,
    JobButtonReceiver,
    JobHookReceiver,
    register_jobs,
)
from nautobot.dcim.models import Location
from nautobot.extras.choices import ObjectChangeActionChoices

name = "Cisco Smart Licensing Jobs"

class BalanceSmartLicensesDryRunJob(Job):
    dryrun = DryRunVar()

    class Meta:
        approval_required = False
        has_sensitive_variables = False
        description = "Running this job will balance out the Smart Licenses for all virtual accounts"
    
    def run(self, dryrun):
        try:
            with transaction.atomic():
                locations = Location.objects.all()
                
                if dryrun:
                    log_msg += " (DRYRUN)"
                self.logger.info(log_msg, locations.count())
                virtual_accounts = []
                for loc in locations:
                    if loc.location_type == 'Hospital':
                        virtual_accounts.append(f'{loc.cf["state"]}{loc.facility}')
                log_msg = f"Virtual account list:\n{virtual_accounts}"
        except Exception:
            self.logger.error("%s failed. Database changes rolled back.", self.__name__)
            raise

class BalanceSmartLicensesJob(Job):
    # specify template_name to override the default job scheduling template
    # template_name = "example_plugin/example_with_custom_template.html"

    class Meta:
        name = "Balance Cisco Smart Licenses"
        description = """
            Running this job will balance out the Smart Licenses for all virtual accounts
        """

    def run(self):
        locations = Location.objects.all()
        virtual_accounts = []
        for loc in locations:
            if loc.location_type == 'Hospital':
                virtual_accounts.append(f'{loc.cf["state"]}{loc.facility}')
        log_msg = f"Virtual account list items: "
        self.logger.info(log_msg, virtual_accounts.count())

class BalanceSmartLicensesJob(Job):
    # specify template_name to override the default job scheduling template
    # template_name = "example_plugin/example_with_custom_template.html"

    class Meta:
        name = "Generate Smart License Tokens"
        description = """
            Running this job will balance out the Smart Licenses for all virtual accounts
        """

    def run(self):
        locations = Location.objects.all()
        virtual_accounts = []
        for loc in locations:
            if loc.location_type == 'Hospital':
                virtual_accounts.append(f'{loc.cf["state"]}{loc.facility}')
        log_msg = f"Virtual account list items: (Hospital Locations)"
        self.logger.info(log_msg, virtual_accounts.count())

jobs = (
    BalanceSmartLicensesDryRunJob,
    BalanceSmartLicensesJob
)

register_jobs(*jobs)