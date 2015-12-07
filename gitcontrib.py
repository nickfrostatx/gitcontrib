#!/usr/bin/env python
"""gitcontrib: Compare the activity of different git contributors."""

from __future__ import print_function
from subprocess import check_output, CalledProcessError
import sys
import os


__version__ = '0.1.0'


def usage():
    """Print the program usage information."""
    sys.stderr.write('Usage:\ngitcontrib [path] [extension ...]\n')


def color(col, text):
    """Wrap a string with terminal styling."""
    return '\x1b[{0}m{1}\x1b[0m'.format(col, text)


def grey(text):
    """Wrap a string in grey text styling."""
    return color('37', text)


# monad
def pretty_output(loc, auth_loc, expected_contrib):
    """Display summary statistics."""
    print(grey('PROJECT CONTRIBUTIONS'))
    print(grey('The project has'), color('34;1', loc), grey('lines of code'))
    print()
    print(grey('Contributors ({0:d}):'.format(len(auth_loc))))
    print('   ' + '\n   '.join(auth_loc.keys()))
    print()
    print(grey('Contribution breakdown:'))
    for u, uloc in sorted(auth_loc.items(), key=lambda u: u[1], reverse=True):
        col = '32;1' if uloc >= expected_contrib * loc else '31;1'
        print('   {0} has contributed,'.format(u),
              color(col, uloc), 'lines of code',
              '(' + color(col, '{0:.2f}%'.format((uloc*100. / loc))) + ')')


def git(path, *args):
    """Call git on the specified repository."""
    cmd = ['git', '--git-dir=' + os.path.join(path, '.git'),
           '--work-tree=' + path]
    return check_output(cmd + list(args)).decode()


def git_contrib(path, ext):
    """Count the total lines written by each contributor."""
    auth_loc = {}
    git_files = git(path, 'ls-tree', '--name-only', '-r', 'HEAD')
    for f in git_files.split('\n'):
        if f.split('.')[-1] not in ext:
            continue
        blame = git(path, 'blame', '--line-porcelain', 'HEAD', '--', f)
        for line in blame.split('\n'):
            if line.startswith('author '):
                author = line[7:]
                if author not in auth_loc:
                    auth_loc[author] = 0
                auth_loc[author] += 1
    return auth_loc


def main():
    """Parse sys.argv and call git_contrib."""
    if (len(sys.argv) < 3):
        usage()
        return 1

    try:
        contrib = git_contrib(sys.argv[1], set(sys.argv[2:]))
    except CalledProcessError as e:
        return e.returncode

    loc = sum(contrib.values())

    if len(contrib) == 0:  # auth_loc and drop it
        sys.stderr.write('No git-commit authors found\n')
        return 1

    pretty_output(loc, contrib, 1. / len(contrib))
    return 0


if __name__ == '__main__':
    sys.exit(main())
