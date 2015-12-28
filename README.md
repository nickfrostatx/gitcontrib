Git Contrib
===========

[![Build Status](https://img.shields.io/travis/nickfrostatx/gitcontrib.svg)](https://travis-ci.org/nickfrostatx/gitcontrib)
[![Coverage](https://img.shields.io/coveralls/nickfrostatx/gitcontrib.svg)](https://coveralls.io/github/nickfrostatx/gitcontrib)
[![Version](https://img.shields.io/pypi/v/gitcontrib.svg)](https://pypi.python.org/pypi/gitcontrib)
[![License](https://img.shields.io/pypi/l/gitcontrib.svg)](https://raw.githubusercontent.com/nickfrostatx/gitcontrib/master/LICENSE)

The roommates coming together to write some code.. oh god

**TODO**
* Handle different name same email as one contributor
* Handle different email same name as one contributor
* Handle github-side edits being double-counted
* ncurses taking over my term kinda makes me double-take, how do you guys feel about it
* (at least) Make ncurses background use your term background color rather than being grey
* --simple or --json to make it output raw json so that it can ship to a badge/webapp view/module
* Add setup/install hook which runs `git config alias.contrib "!gitcontrib.py"` so that our package can be called with `git contrib`
* Manpage install + cleanup if installed via a package manager
