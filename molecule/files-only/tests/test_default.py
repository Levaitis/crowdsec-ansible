# SPDX-FileCopyrightText: 2025 Leonardo Vasi <dev@levaitis.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
def test_files_rendered(host):
    assert host.file('/etc/crowdsec/config.yaml').exists
    assert host.file('/srv/crowdsec/docker-compose.yml').exists
    # check perms
    assert host.file('/etc/subuid').mode == 0o644
    assert host.file('/etc/subgid').mode == 0o644
