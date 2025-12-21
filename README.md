# Ansible Role: CrowdSec

An Ansible role for installing and configuring [CrowdSec](https://www.crowdsec.net/), an open-source and collaborative security engine.

## Description

This role installs and configures CrowdSec on Debian/Ubuntu and RedHat/CentOS-based systems. CrowdSec is a free, modern & collaborative behavior detection engine, coupled with a global IP reputation network. It stacks on fail2ban's philosophy but is IPV6 compatible and 60x faster.

## Requirements

- Ansible 2.9 or higher
- Supported operating systems:
  - Ubuntu 20.04, 22.04, 24.04
  - Debian 10, 11, 12
  - RHEL/CentOS/Rocky/AlmaLinux 8, 9

## Role Variables

### Main Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
# CrowdSec version to install (leave empty for latest)
crowdsec_version: ""

# CrowdSec service state and enabled status
crowdsec_service_state: started
crowdsec_service_enabled: true

# CrowdSec configuration directories
crowdsec_config_dir: /etc/crowdsec
crowdsec_data_dir: /var/lib/crowdsec/data
crowdsec_log_dir: /var/log/crowdsec

# API settings
crowdsec_local_api_url: "http://127.0.0.1:8080"

# Log settings
crowdsec_log_level: info  # Options: trace, debug, info, warning, error
crowdsec_log_mode: file    # Options: file, stdout

# Collections to install (CrowdSec security scenarios)
crowdsec_collections:
  - crowdsecurity/linux
  - crowdsecurity/sshd

# Acquisition configuration (log files to monitor)
crowdsec_acquisitions:
  - source: file
    filenames:
      - /var/log/auth.log
      - /var/log/syslog
    labels:
      type: syslog

# Prometheus metrics
crowdsec_prometheus_enabled: true
crowdsec_prometheus_level: full
crowdsec_prometheus_listen_addr: "127.0.0.1"
crowdsec_prometheus_listen_port: 6060

# Console enrollment (optional)
crowdsec_enroll_key: ""
crowdsec_enroll_name: ""
crowdsec_enroll_tags: []
crowdsec_enroll_overwrite: false

# Bouncers to install
crowdsec_bouncers: []

# Package state
crowdsec_package_state: present  # Options: present, latest
```

## Dependencies

None.

## Example Playbook

### Basic Installation

```yaml
- hosts: servers
  become: yes
  roles:
    - role: crowdsec
```

### Advanced Configuration

```yaml
- hosts: servers
  become: yes
  roles:
    - role: crowdsec
      vars:
        crowdsec_log_level: debug
        crowdsec_collections:
          - crowdsecurity/linux
          - crowdsecurity/sshd
          - crowdsecurity/nginx
          - crowdsecurity/apache2
        crowdsec_acquisitions:
          - source: file
            filenames:
              - /var/log/auth.log
              - /var/log/syslog
            labels:
              type: syslog
          - source: file
            filenames:
              - /var/log/nginx/access.log
              - /var/log/nginx/error.log
            labels:
              type: nginx
        crowdsec_enroll_key: "your-enrollment-key"
        crowdsec_enroll_name: "my-server"
        crowdsec_enroll_tags:
          - production
          - web
```

### With Firewall Bouncer

```yaml
- hosts: servers
  become: yes
  roles:
    - role: crowdsec
      vars:
        crowdsec_collections:
          - crowdsecurity/linux
          - crowdsecurity/sshd
        crowdsec_bouncers:
          - name: firewall-bouncer
            api_key: "your-bouncer-api-key"
```

## Collections

Collections are bundles of parsers and scenarios for specific services. Common collections include:

- `crowdsecurity/linux` - Base Linux collection
- `crowdsecurity/sshd` - SSH protection
- `crowdsecurity/nginx` - Nginx web server
- `crowdsecurity/apache2` - Apache web server
- `crowdsecurity/mysql` - MySQL database
- `crowdsecurity/postgresql` - PostgreSQL database

Find more collections at: https://hub.crowdsec.net/browse/#collections

## Bouncers

Bouncers are components that block malicious IPs. Popular bouncers:

- `cs-firewall-bouncer` - iptables/nftables bouncer
- `cs-nginx-bouncer` - Nginx bouncer
- `cs-cloudflare-bouncer` - Cloudflare bouncer

Find more bouncers at: https://hub.crowdsec.net/browse/#bouncers

## CrowdSec Console Enrollment

To enroll your CrowdSec instance with the [CrowdSec Console](https://app.crowdsec.net/):

1. Create an enrollment key in the CrowdSec Console
2. Set the `crowdsec_enroll_key` variable
3. Optionally set `crowdsec_enroll_name` and `crowdsec_enroll_tags`

## Tags

This role supports the following tags for selective execution:

- `crowdsec` - All tasks
- `crowdsec-install` - Installation tasks only
- `crowdsec-config` - Configuration tasks only
- `crowdsec-collections` - Collection installation only
- `crowdsec-bouncers` - Bouncer installation only
- `crowdsec-enroll` - Console enrollment only
- `crowdsec-service` - Service management only

Example: Install and configure without starting service

```bash
ansible-playbook playbook.yml --tags crowdsec-install,crowdsec-config --skip-tags crowdsec-service
```

## License

GPL-2.0-or-later

## Author Information

This role was created for use with the mash project.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- CrowdSec Documentation: https://doc.crowdsec.net/
- CrowdSec Hub: https://hub.crowdsec.net/
- CrowdSec Community: https://discourse.crowdsec.net/
