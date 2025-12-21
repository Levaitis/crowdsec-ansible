# SPDX-FileCopyrightText: 2025 Leonardo Vasi <dev@levaitis.de>
# SPDX-License-Identifier: AGPL-3.0-or-later
def test_docker_present(host):
    assert host.run('which docker').rc == 0


def test_compose_file(host):
    assert host.file('/srv/crowdsec/docker-compose.yml').exists


def test_api(host):
    res = host.run('curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/')
    assert res.rc == 0
    assert res.stdout == '200'
