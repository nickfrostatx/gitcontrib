#!/usr/bin/env python
"""gitcontrib: Compare the activity of different git contributors."""

from __future__ import print_function
from functools import partial
import curses
import os
import subprocess
import sys


__version__ = '0.1.0'


def usage():
    """Print the program usage information."""
    sys.stderr.write('Usage:\ngitcontrib [path] [extension ...]\n')


# monad
def pretty_print(total_lines, auth_dict, expected_contrib):
    stdscr = curses.initscr()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.curs_set(0)

    # Tuple unpacking sets each of these equal to a curses color
    t_colors = tuple([curses.color_pair(x) for x in range(1, 4)])
    (T_RED, T_GREEN, T_BLUE) = t_colors

    stdscr.addstr('PROJECT CONTRIBUTIONS\n')
    stdscr.addstr('This project has ')
    stdscr.addstr(str(total_lines), T_BLUE)
    stdscr.addstr(' lines of code\n\n')
    stdscr.addstr('Contributors ({0:d}):\n'.format(len(auth_dict)))
    stdscr.addstr('   ' + '\n   '.join(auth_dict.keys()))
    stdscr.addstr('\n\nContribution breakdown:\n')
    for u, uloc in sorted(auth_dict.items(), key=lambda u: u[1], reverse=True):
        col = T_GREEN if uloc >= expected_contrib * total_lines else T_RED
        stdscr.addstr('   {0} has contributed '.format(u))
        stdscr.addstr(str(uloc), col)
        stdscr.addstr(' lines of code (')
        stdscr.addstr('{0:.2f}%'.format((uloc*100. / total_lines)), col)
        stdscr.addstr(')\n')

    stdscr.refresh()
    stdscr.getkey()
    curses.endwin()


def git(path, *args):
    """Call git on the specified repository."""
    cmd = ['git', '--git-dir=' + os.path.join(path, '.git'),
           '--work-tree=' + path] + list(args)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    data = proc.communicate()[0].decode()
    if proc.returncode != 0:
        raise OSError('git command failed', proc.returncode)
    return data


def git_contrib(path, ext):
    """Count the total lines written by each contributor."""
    auth_loc = {}
    git_files = git(path, 'ls-tree', '--name-only', '-r', 'HEAD')
    for f in git_files.split('\n'):
        if not f or '*' not in ext and f.split('.')[-1] not in ext:
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
    if len(sys.argv) < 2:
        usage()
        return 1
    if len(sys.argv) < 3:
        sys.argv.append("*")

    try:
        contrib = git_contrib(sys.argv[1], set(sys.argv[2:]))
    except OSError as e:
        return e.args[1]

    loc = sum(contrib.values())

    if len(contrib) == 0:  # auth_loc and drop it
        sys.stderr.write('No git-commit authors found\n')
        return 1

    pretty_print(loc, contrib, 1. / len(contrib))
    return 0


if __name__ == '__main__':
    sys.exit(main())
