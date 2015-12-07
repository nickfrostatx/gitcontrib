#!/usr/bin/env python3

from subprocess import check_output
from sys import argv, exit
from os import chdir, devnull
import os


__version__ = '0.1.0'


def usage():
    print("Usage:\ngitcontrib <Path> <File Extension>")


# monad
def pretty_output(loc, auth_loc, expected_contrib):
    print("\033[37;1mPROJECT CONTRIBUTIONS:\033[0m")
    print("\033[37mThe project has \033[34;1m%d\033[0;37m lines of code.\033[0m" % loc)
    print()
    print("\033[37mContributors (%d):\033[0m" % len(auth_loc.keys()))
    print('', end='   ')
    print('\n   '.join(auth_loc.keys()))
    print()
    print("\033[37mContribution breakdown:\033[0m")
    outs = []
    for a in auth_loc:
        outs.append((a, auth_loc[a]))
    outs.sort(key = lambda u: u[1])
    outs.reverse()
    for a in outs:
        if a[1] >= expected_contrib*loc:
            print('   ', a[0], ' has contributed ', '\033[32;1m', a[1], '\033[0m', ' lines of code ', '(\033[032;1m%.2f%%\033[0m) ' % (a[1]*100/loc), sep="")
        else:
            print('   ', a[0], ' has contributed ', '\033[31;1m', a[1], '\033[0m', ' lines of code ', '(\033[031;1m%.2f%%\033[0m) ' % (a[1]*100/loc), sep="")


def git_contrib(location, ext):
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
        if not f.endswith('.' + ext):
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

    pretty_output(loc, auth_loc, 1 / len(auth_loc))
    return 0


def main():
    if (len(argv) != 3):
        usage()
        return 1
    return git_contrib(argv[1], argv[2])


if __name__ == '__main__':
    exit(main())
