# -*- coding: utf-8 -*-
"""Test them contribs."""

from gitcontrib import git
from subprocess import check_call
import pytest


@pytest.fixture
def git_repo(tmpdir):
    check_call(['git', 'init', str(tmpdir)])
    return tmpdir


def test_git(git_repo):
    out = git(str(git_repo), 'status')
    assert out == ('On branch master\n\nInitial commit\n\n'
                   'nothing to commit (create/copy files and use "git add" '
                   'to track)\n')
