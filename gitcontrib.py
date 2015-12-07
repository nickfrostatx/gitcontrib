#!/usr/bin/env python3

# TODO
# Multiple source extensions
# Handle different name same email as one contributor
# Handle different email same name as one contributor
# Handle github-side edits being double-counted

import subprocess as sp
from sys import argv, exit
from os import chdir, devnull

def usage():
    print("Usage:\ngitcontrib <Path> <File Extension>");

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

    try:
        sp.check_call(['ls', '.git'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    except:
        print("%s is not a git repository" % location)
        return 1

    (s, author_out) = sp.getstatusoutput("git log | grep Author | sort -u")
    if s != 0:
        print(author_out)
        return 0
    authors = author_out.split('\n')
    authors = [a.replace("Author: ", "") for a in authors]
    
    try:
        assert len(authors) > 0
    except AssertionError:
        print("No git-commit authors found")
        return 1

    files = sp.getoutput("find . -iname \*.%s" % ext).replace('\n', ' ')
    if len(files):
        try:
            loc = int(sp.getoutput("wc -l %s" % files).split("\n")[-1].split()[0]);
            assert loc >= 0
        except:
            print("Error in parsing files (check file permissions?)")
            return 1
    else:
        print("No files with extension '%s' in %s" % (ext, location))
        return 1
    auth_loc = {}
    for a in authors:
        aloc = 0
        try:
            name = a[0:a.index("<") - 1]
        except:
            name = a
        for f in files.split():
            aloc += sum([int(x) for x in sp.getoutput("git blame %s | grep \"%s\" | wc -l" % (f, name)).split('\n')])
        auth_loc[a] = aloc 
    pretty_output(loc, auth_loc, 1 / len(authors))
    return 0

def main():
    if (len(argv) != 3):
        usage()
        return 1
    return git_contrib(argv[1], argv[2])

if __name__ == '__main__':
    exit(main())
