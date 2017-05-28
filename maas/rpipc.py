# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Raspberry Pi Power Control Driver."""

__all__ = []

import urllib.error
import urllib.parse
import urllib.request

import json

from provisioningserver.drivers.power import PowerDriver
from provisioningserver.logger import get_maas_logger
from twisted.internet.defer import maybeDeferred


maaslog = get_maas_logger("drivers.power.rpipc")


class RaspberryPiPowerControlDriver(PowerDriver):

    name = 'rpipc'
    description = "Raspberry Pi Power Control Driver."
    settings = []

    def detect_missing_packages(self):
        # no required packages
        return []

    def get_url(self,system_id,context):
        return '/'.join([context['power_address'],context['node_name']])

    def change_power(self, system_id, context, on):
        power = 'poweron' if on else 'poweroff'
        maaslog.info(power)
        values = {'action': power}
        maaslog.info(values)
        data = json.dumps(values).encode('ascii') # data should be bytes
        maaslog.info(data)
        req = urllib.request.Request(self.get_url(system_id,context))
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req,data) as response:
            maaslog.info(response.read())

    def power_on(self, system_id, context):
        """Power on machine manually."""
        maaslog.info("Having Raspberry Pi turn on %s." % system_id)
        self.change_power(system_id, context, True)

    def power_off(self, system_id, context):
        """Power off machine manually."""
        maaslog.info("Having Raspberry Pi turn off %s." % system_id)
        self.change_power(system_id, context, False)

    def power_query(self, system_id, context):
        """Power query machine manually."""
        maaslog.info("Getting power state for %s from Raspberry Pi." % system_id)
        with urllib.request.urlopen(self.get_url(system_id,context)) as response:
            body = response.read()
            maaslog.info(body)
            decoded = body.decode(response.info().get_param('charset') or 'utf-8')
            maaslog.info(decoded)
            data = json.loads(decoded)
            maaslog.info(data)
            return data['power']
        return 'unknown'
