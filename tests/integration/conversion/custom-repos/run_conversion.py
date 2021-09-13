import re

from collections import namedtuple

import pytest


try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def get_system_version(system_release_content=None):
    """Return a namedtuple with major and minor elements, both of an int type.
    Examples:
    Oracle Linux Server release 6.10
    Oracle Linux Server release 7.8
    CentOS release 6.10 (Final)
    CentOS Linux release 7.6.1810 (Core)
    CentOS Linux release 8.1.1911 (Core)
    """
    match = re.search(r".+?(\d+)\.(\d+)\D?", system_release_content)
    if not match:
        return "not match"
    version = namedtuple("Version", ["major", "minor"])(int(match.group(1)), int(match.group(2)))

    return version


def test_run_conversion_using_custom_repos(shell, convert2rhel):

    with open("/etc/system-release", "r") as file:
        system_release = file.read()
        system_version = get_system_version(system_release_content=system_release)
        if system_version.major == 7:
            enable_repo_opt = "--enablerepo rhel-7-server-rpms --enablerepo rhel-7-server-optional-rpms --enablerepo rhel-7-server-extras-rpms"
        elif system_version.major == 8:
            enable_repo_opt = "--enablerepo rhel-8-for-x86_64-baseos-rpms --enablerepo rhel-8-for-x86_64-appstream-rpms"

    with convert2rhel("-y --no-rpm-va --disable-submgr {} --debug".format(enable_repo_opt)) as c2r:
        c2r.expect("Conversion successful!")

    assert c2r.exitstatus == 0