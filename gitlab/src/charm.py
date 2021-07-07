#!/usr/bin/env python3
# Copyright 2021 Erik Lönroth
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""
import json
import logging
import os
import subprocess

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus
import utils

logger = logging.getLogger(__name__)

from ops.model import (
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus,
    ModelError
)



class OperatorGitlabCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self._stored.set_default(things=[])
        self.unit.status = ActiveStatus()

        # Events
        event_bindings = {
            self.on.install: self._on_install,
            self.on.config_changed: self._on_config_changed,
            self.on.upgrade_charm: self._on_install,
            # self.on.start: self._on_start,
            # self.on.stop: self._on_stop,
            # self.on.update_status: self._on_update_status
        }
        # Observe
        for event, handler in event_bindings.items():
            self.framework.observe(event, handler)

    def _on_config_changed(self, event):
        current = self.config["thing"]
        if current not in self._stored.things:
            logger.debug("found a new thing: %r", current)
            self._stored.things.append(current)

    def _on_install(self, event):
        self.unit.status = MaintenanceStatus("Installing external repo.")
        # Stage 1 - get upstream repo
        cmd = 'curl -L curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash'
        ps = subprocess.Popen(cmd, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              universal_newlines=True)
        output = ps.communicate()[0]
        logger.debug(output)

        subprocess.check_call(['apt', 'update'])

        # Stage 2 - install deps and mta
        self.unit.status = MaintenanceStatus("Installing dependencies.")
        install_cmd = 'apt install -y curl openssh-server ca-certificates tzdata perl postfix'
        install_env = os.environ.copy()
        subprocess.check_call(install_cmd.split(), env=install_env)

        # Stage 3 - install gitlab
        self.unit.status = MaintenanceStatus("Installing gitlab.")
        ## First get the external IP from the relation "website".

        ## website_relation = self.model.get_relation("website")
        ip = str(self.model.get_binding("website").network.bind_address)

        ## Install software with the environment variable EXTERNAL_URL set to the unite IP.
        install_cmd = 'apt install -y gitlab-ee'
        install_env = os.environ.copy()
        install_env['EXTERNAL_URL'] = ip
        subprocess.check_call(install_cmd.split(), env=install_env)
        self.unit.status = MaintenanceStatus("Completing installation.")
        self.setversion()
        utils.open_port('80')
        self.unit.status = ActiveStatus("Ready")


    def setversion(self):
        # Opening JSON file
        f = open('/opt/gitlab/version-manifest.json')
        data = json.load(f)
        v = data['software']['gitlab-rails']['display_version']
        f.close()
        self.unit.set_workload_version(v)

if __name__ == "__main__":
    main(OperatorGitlabCharm)
