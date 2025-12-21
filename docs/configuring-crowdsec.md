<!--
SPDX-FileCopyrightText: 2025 Leonardo Vasi <dev@levaitis.de>

SPDX-License-Identifier: AGPL-3.0-only
-->
# Configuring CrowdSec (role)

This document describes the configuration options provided by the Ansible role and explains how to operate CrowdSec in docker-compose mode.

## Overview

The role deploys CrowdSec using a docker-compose stack and manages configuration via host-mounted files rendered by Ansible.

When running in docker mode the role renders configuration files on the host and bind-mounts them into the container. One‑shot operations (collection install, enrollment, bouncer install) run in ephemeral containers which mount the same host directories so they operate on the same state.

## Important directories (host)

- `crowdsec_config_dir` (default: `/etc/crowdsec`) — configuration templates are rendered here (e.g. `config.yaml`, `acquis.yaml`)
- `crowdsec_data_dir` (default: `/var/lib/crowdsec/data`) — database and runtime data
- `crowdsec_log_dir` (default: `/var/log/crowdsec`) — log files

These host directories are mounted into the container at the standard paths used by CrowdSec.

## Main role variables

Provided in `defaults/main.yml`. Key variables (with typical defaults):

- `crowdsec_install_type`: `docker` (role is docker-only)
- `crowdsec_docker_image`: `crowdsecurity/crowdsec`
- `crowdsec_docker_tag`: `latest`
- `crowdsec_container_name`: `crowdsec`
- `crowdsec_compose_dir`: `/srv/crowdsec`
- `crowdsec_compose_file`: `docker-compose.yml`
- `crowdsec_config_dir`: `/etc/crowdsec`
- `crowdsec_data_dir`: `/var/lib/crowdsec/data`
- `crowdsec_log_dir`: `/var/log/crowdsec`
- `crowdsec_docker_ports`: list of `host:container` mappings (default exposes API & prometheus on loopback)
- `crowdsec_docker_env`: additional environment variables for the container
- `crowdsec_host_user`, `crowdsec_host_uid`, `crowdsec_host_group`, `crowdsec_host_gid` — host user/group used to map container root to host via Docker userns remap

Refer to `defaults/main.yml` for the full list.

## Templates

- `templates/config.yaml.j2` — main CrowdSec configuration
- `templates/acquis.yaml.j2` — acquisition configuration (what logs to monitor)
- `templates/docker-compose.yml.j2` — docker-compose file for docker mode

The role renders `acquis.yaml` and `config.yaml` to `{{ crowdsec_config_dir }}` and then mounts that directory into the container.

If you need to customize config beyond variables exposed in the role, update the templates or override variables in your playbook.

## Docker mode specifics

- The compose template runs the container as root inside the container (`user: "0:0"`).
- The role configures Docker daemon `userns-remap` to map container root to a host user (defaults to a `crowdsec` system user). This makes files created by the container root appear owned by the `crowdsec` host user—preserving expected ownership on the host.
- The role will create the host user/group and host directories and set ownership to that user.
- One-shot commands (cscli operations) are executed in ephemeral containers that mount the same host dirs and run `cscli` directly; they are removed automatically.

Caveat: enabling `userns-remap` modifies Docker daemon behavior for all containers on the host. Test on non-production hosts before applying broadly.

## One‑shot operations (collections, enroll, bouncers)

The role uses ephemeral containers to run one-off `cscli` commands. The pattern is:

1. Run a container from the CrowdSec image with `command: cscli <...>`.
2. Mount host `config`, `data` and `log` dirs into the container.
3. Run as root inside the container so the command can read/write the mounted files.
4. Use `auto_remove: true` so the container is removed after the command finishes.

This ensures the same host-backed state is used by both the long-running service and the one-shot operations.

Alternative: if you prefer, the role can be changed to execute `docker exec` against the running container instead of starting ephemeral containers.

## Enrollment

To enroll the instance with the CrowdSec Console set the variable `crowdsec_enroll_key` and optionally `crowdsec_enroll_name` and `crowdsec_enroll_tags`. The role will run the enrollment command in a one-shot container.

## Collections

Control collections with `crowdsec_collections` (list of collection names). The role runs `cscli collections install <collection>` in ephemeral containers so the installed collections are persisted on host mount points.

## Bouncers

List bouncers with `crowdsec_bouncers`. Each bouncer in the list will be added via `cscli bouncers add <name>`; the role uses the same one-shot container approach.

## Permissions, SELinux and AppArmor

- Files are owned by the configured host user (defaults to `crowdsec` UID/GID provided in defaults). Ensure this UID/GID does not conflict with existing users.
- If SELinux is enabled use appropriate mount options or `:Z` in the compose template (the compose template already includes `:Z` for convenience) and verify labels.
- AppArmor or other LSMs may restrict container access to host files; adjust profiles if required.

## Troubleshooting

- If cscli commands report permission errors, verify ownership of host mount points and the Docker userns mapping.
- If docker fails to start after changing `/etc/docker/daemon.json`, verify JSON syntax and merge existing settings (the role currently overwrites daemon.json — see the caveat).
- Use `docker logs <container>` and `docker-compose -f <file> ps` to inspect container status.

## Examples

Enable docker mode in your playbook variables:

```yaml
roles:
  - role: crowdsec
    vars:
      crowdsec_install_type: docker
      crowdsec_compose_dir: /srv/crowdsec
      crowdsec_host_user: crowdsec
      crowdsec_host_uid: 1001
      crowdsec_host_group: crowdsec
      crowdsec_host_gid: 1001
      crowdsec_docker_ports:
        - "127.0.0.1:8080:8080"
        - "127.0.0.1:6060:6060"
```

Run the role and verify the API is reachable on the configured host address: `curl -sS http://127.0.0.1:8080/`.

---

If you want the document expanded with sample `docker-compose` contents or instructions to revert changes to `/etc/docker/daemon.json`, tell me which section to expand.
