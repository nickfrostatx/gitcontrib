# -*- coding: utf-8 -*-
"""Test them contribs."""

import gitcontrib
import pytest
import subprocess


@pytest.fixture
def git_repo(tmpdir):
    subprocess.check_call(['git', 'init', str(tmpdir)])
    return tmpdir


def test_usage(capsys):
    gitcontrib.usage()
    out, err = capsys.readouterr()
    assert err == 'Usage:\ngitcontrib [path] [extension ...]\n'


def test_colors():
    assert gitcontrib.color('34;1', 'Bright') == '\x1b[34;1mBright\x1b[0m'
    assert gitcontrib.grey('Normal grey') == '\x1b[37mNormal grey\x1b[0m'


def test_git(git_repo):
    assert 'nothing to commit' in gitcontrib.git(str(git_repo), 'status')
