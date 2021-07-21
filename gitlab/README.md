# operator-gitlab
  The gitlab server, installed as described here: https://about.gitlab.com/install/#ubuntu
  After installation, the initial root password is located in /etc/gitlab/initial_root_password

This charm does not need a database or anything since its bundled with the installation.


## Deployment

At least 6G seems to be needed to deploy.

    juju deploy ./gitlab.charm --constraints="mem=6G"
    juju expose gitlab

The initial root password is found in: /etc/gitlab/initial_root_password


## Use with gitlab-runner
This charm works great in conjuction with gitlab-runners for CI/CD.  Read here https://charmhub.io/gitlab-runner/docs

    juju deploy gitlab-runner --config runner-config.yaml
     

## Configuration
Nothing yet

## Actions
Nothing yet

## Author
Erik Lönroth https://eriklonroth.com

## Upstream repo
https://github.com/erik78se/operator-gitlab
