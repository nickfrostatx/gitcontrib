# -*- coding: utf-8 -*-
"""Test them contribs."""

from gitcontrib import usage, git
from subprocess import check_call
import pytest


@pytest.fixture
def git_repo(tmpdir):
    check_call(['git', 'init', str(tmpdir)])
    return tmpdir


def test_usage(capsys):
    usage()
    out, err = capsys.readouterr()
    assert err == 'Usage:\ngitcontrib [path] [extension ...]\n'


def test_git(git_repo):
    assert 'nothing to commit' in git(str(git_repo), 'status')
