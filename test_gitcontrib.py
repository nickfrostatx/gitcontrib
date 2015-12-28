# -*- coding: utf-8 -*-
"""Test them contribs."""

import gitcontrib
import pytest
import subprocess
import sys


@pytest.fixture
def git_repo(tmpdir):
    subprocess.check_call(['git', 'init', str(tmpdir)])
    return tmpdir


def test_usage(capsys):
    gitcontrib.usage()
    out, err = capsys.readouterr()
    assert err == 'Usage:\ngitcontrib [-p path] [extension ...]\n'


def test_git(git_repo):
    assert 'nothing to commit' in gitcontrib.git(str(git_repo), 'status')


def test_badArg(capsys):
    sys.argv = ['gitcontrib', '-a']
    gitcontrib.main()
    out, err = capsys.readouterr()
    assert err == 'Usage:\ngitcontrib [-p path] [extension ...]\n'
