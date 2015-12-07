#!/usr/bin/env python

from __future__ import print_function
from subprocess import check_output
from sys import argv, exit
from os import chdir, devnull
import os


__version__ = '0.1.0'


def usage():
    """Print the program usage information."""
    print("Usage:\ngitcontrib <Path> <File Extension>")


def color(col, text):
    return '\x1b[{0}m{1}\x1b[0m'.format(col, text)


def grey(text):
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
        print('   {0} has contributed,'.format(u), color(col, uloc), 'lines of code',
              '(' + color(col, '{0:.2f}%'.format((uloc*100. / loc))) + ')')


def git_contrib(location, ext):
    """Count the total lines written by each contributor."""
    try:
        chdir(location)
    except:
        print("Error accessing %s (check file permissions?)" % location)
        return 1

    if not os.path.exists('.git'):
        print("%s is not a git repository" % location)
        return 1

    auth_loc = {}
    git_files = check_output('git ls-tree --name-only -r HEAD', shell=True)
    for f in git_files.decode().split('\n'):
        if f.split('.')[-1] not in ext:
            continue
        cmd = ('git blame --line-porcelain HEAD "{0}" | grep  "^author "'
               .format(f))
        for line in check_output(cmd, shell=True).decode().split('\n'):
            if line:
                author = line[7:]
                if author not in auth_loc:
                    auth_loc[author] = 0
                auth_loc[author] += 1

    loc = sum(auth_loc.values())

    if len(auth_loc) == 0:
        print("No git-commit authors found")
        return 1

    pretty_output(loc, auth_loc, 1. / len(auth_loc))
    return 0


def main():
    """Parse sys.argv and call git_contrib."""
    if (len(argv) < 3):
        usage()
        return 1
    return git_contrib(argv[1], set(argv[2:]))


if __name__ == '__main__':
    exit(main())
