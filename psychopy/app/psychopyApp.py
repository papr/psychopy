#!/usr/bin/env python2

# Part of the PsychoPy library
# Copyright (C) 2015 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

from __future__ import absolute_import, print_function

import sys
from psychopy.app._psychopyApp import PsychoPyApp, __version__

#NB the PsychoPyApp classes moved to _psychopyApp.py as of version 1.78.00
#to allow for better upgrading possibilities from the mac app bundle. this file
#now used solely as a launcher for the app, not as the app itself.

if __name__=='__main__':
    if '-x' in sys.argv:
        # run a .py script from the command line using StandAlone python
        targetScript = sys.argv[sys.argv.index('-x') + 1]
        from psychopy import core
        import os
        core.shellCall([sys.executable, os.path.abspath(targetScript)])
        sys.exit()
    if '-v' in sys.argv or '--version' in sys.argv:
        info = 'PsychoPy2, version %s (c)Jonathan Peirce 2015, GNU GPL license'
        print(info % __version__)
        sys.exit()
    if '-h' in sys.argv or '--help' in sys.argv:
        print("""Starts the PsychoPy2 application.

Usage:  python PsychoPy.py [options] [file]

Without options or files provided this starts PsychoPy using prefs to
decide on the view(s) to open.  If optional [file] is provided action
depends on the type of the [file]:

 Python script 'file.py' -- opens coder

 Experiment design 'file.psyexp' -- opens builder

Options:
    -c, --coder, coder       opens coder view only
    -b, --builder, builder   opens builder view only
    -x script.py             directly execute script.py using StandAlone python

    -v, --version    prints version and exits
    -h, --help       prints this help and exit

    --firstrun       launches configuration wizard
    --no-splash      suppresses splash screen

""")
        sys.exit()

    else:
        showSplash = True
        if '--no-splash' in sys.argv:
            showSplash = False
            del sys.argv[sys.argv.index('--no-splash')]
        app = PsychoPyApp(0, showSplash=showSplash)
        app.MainLoop()
