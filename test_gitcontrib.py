# -*- coding: utf-8 -*-
"""Test them contribs."""

import gitcontrib
import json
import pytest
import subprocess
import sys


u_string = 'Usage:\ngitcontrib [--json] [-p, --path path] [extension(s) ...]\n'


@pytest.fixture
def git_repo(tmpdir):
    subprocess.check_call(['git', 'init', str(tmpdir)])
    return tmpdir


def test_usage(capsys):
    gitcontrib.usage()
    out, err = capsys.readouterr()
    assert err == u_string


def test_git(git_repo):
    # NOTE XXX TODO NO NO NO NO WRONG BAD NO XXX
    assert b'nothing to commit' in gitcontrib.git(str(git_repo), 'status')


def test_badArg(capsys):
    sys.argv = ['gitcontrib', '-a']
    gitcontrib.main()
    out, err = capsys.readouterr()
    assert err == u_string


def test_json(capsys):
    total = 20
    auth = {'a': 12, 'b': 2, 'c': 1, 'd': 5}
    expect = 0.25
    j_data = json.loads(gitcontrib.jsonify(total, auth, expect))
    assert j_data['a']['met_expected']
    assert j_data['b']['lines'] == 2
