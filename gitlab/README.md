# operator-gitlab
  The gitlab server, installed as described here: https://about.gitlab.com/install/#ubuntu
  After installation, the initial root password is located in /etc/gitlab/initial_root_password

This charm does not need a database or anything since its bundled with the installation.


## Deployment

At least 6G seems to be needed to deploy.

    juju deploy ./gitlab.charm --constraints="mem=6G"

The initial root password is found in: /etc/gitlab/initial_root_password

## Configuration
Nothing yet

## Actions
Nothing yet

## Author
Erik Lönroth https://eriklonroth.com

## Upstream repo
https://github.com/erik78se/operator-gitlab
