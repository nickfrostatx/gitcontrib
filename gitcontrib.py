#!/usr/bin/env python
"""gitcontrib: Compare the activity of different git contributors."""

from __future__ import print_function
from functools import partial
import getopt
import json
import os
import subprocess
import sys


__version__ = '0.1.0'

BOLD    = '\033[1m'
CLEAR   = '\033[0m'
BLUE    = '\033[34m'
GREEN   = '\033[32m'
RED     = '\033[31m'

def usage():
    """Print the program usage information."""
    sys.stderr.write(
        'Usage:\ngitcontrib [--json] [-p, --path path] [extension(s) ...]\n'
    )

def print_color(string, color=CLEAR):
    print(color + string + CLEAR, sep='', end='')

def pretty_print(total_lines, auth_dict, expected_contrib):
    print_color('PROJECT CONTRIBUTIONS\n', BOLD)
    print_color('This project has ')
    print_color(str(total_lines), BLUE)
    print_color(' lines of code\n\n')

    print_color('Contributors ({0:d}):\n'.format(len(auth_dict)), BOLD)
    print_color('   ' + '\n   '.join(auth_dict.keys()))

    print_color('\n\nContribution breakdown:\n')

    for u, uloc in sorted(auth_dict.items(), key=lambda u: u[1], reverse=True):
        col = GREEN if uloc >= expected_contrib * total_lines else RED

        print_color('   {0} has contributed '.format(u))
        print_color(str(uloc), col)

        plural = ' line ' if uloc == 1 else ' lines '

        print_color(plural + 'of code (')
        print_color('{0:.2f}%'.format((uloc * 100. / total_lines)), col)
        print_color(')\n')

def jsonify(total_lines, auth_dict, expected_contrib):
    j_data = {}
    j_data["total_lines"] = total_lines

    for u, uloc in auth_dict.items():
        percent = uloc * 100. / total_lines
        expected = uloc >= expected_contrib * total_lines
        j_data[u] = {
            "lines": uloc,
            "percent": '{0:.2f}'.format(percent),
            "met_expected": expected,
        }
    return json.dumps(j_data)

def git(path, *args):
    """Call git on the specified repository."""
    cmd = ['git', '--git-dir=' + os.path.join(path, '.git'),
           '--work-tree=' + path] + list(args)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    data = proc.communicate()[0]
    if proc.returncode != 0:
        raise OSError('git command failed', proc.returncode)
    return data


def git_contrib(path, ext):
    """Count the total lines written by each contributor."""
    auth_loc = {}
    git_files = git(path, 'ls-tree', '--name-only', '-r', 'HEAD').decode()

    for f in git_files.split('\n'):
        if not f or '*' not in ext and f.split('.')[-1] not in ext:
            continue
        blame = git(path, 'blame', '--line-porcelain', 'HEAD', '--', f)
        for line in blame.split(b'\n'):
            if line.startswith(b'author '):
                author = line[7:].decode()
                if author not in auth_loc:
                    auth_loc[author] = 0
                auth_loc[author] += 1
    return auth_loc


def main():
    """Parse sys.argv and call git_contrib."""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:", [
            'path=', 'json'])
    except getopt.GetoptError as err:
        usage()
        return 1
    path = "."
    ext = "*"
    jflag = False
    for opt, arg in opts:
        if opt in ("-p", "--path"):
            path = arg
        elif opt == "--json":
            jflag = True
        else:
            from os import abort
            abort()
    if len(args) > 0:
        ext = args
    try:
        contrib = git_contrib(path, set(ext))
    except OSError as e:
        return e.args[1]

    loc = sum(contrib.values())

    if len(contrib) == 0:
        sys.stderr.write('No git-commit authors found\n')
        return 1

    if jflag:
        print(jsonify(loc, contrib, 1. / len(contrib)))
    else:
        pretty_print(loc, contrib, 1. / len(contrib))
    return 0


if __name__ == '__main__':
    sys.exit(main())
