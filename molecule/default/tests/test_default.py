import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("name", [
    ("haproxy"),
])
def test_packages(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


def test_haproxy_port(host):
    haproxy = host.addr("127.0.0.1")
    haproxy.port(80).is_reachable


def test_haproxy_config(host):
    haproxy_config = host.file("/etc/haproxy/haproxy.cfg")
    haproxy_config.exists
    oct(haproxy_config.mode) == '0644'
    haproxy_config.user == 'root'
    haproxy_config.group == 'root'
