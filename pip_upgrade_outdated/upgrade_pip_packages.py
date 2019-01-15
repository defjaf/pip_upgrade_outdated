#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script upgrades all outdated python packages.
"""

### By Andrew Jaffe <a.h.jaffe@gmail.com>
### https://andrewjaffe.net/
### https://twitter.com/defjaf
### 20 March 2018

## based on https://gist.github.com/serafeimgr/b4ca5d0de63950cc5349d4802d22f3f0
## __author__ = "serafeimgr"
## modified by AHJ to allow different pip executables (pip2, pip3, etc), more command-line arguments

## do we really want to do this with multiprocessing, or just a single giant call to pip?
##   now can choose with a command-line argument
##   and can also choose between single (batch) upgrade and individual (sequential) commands

## does the parsing really work given the new-style headers in the formatting?
##  -- no: needed to add --format legacy; could also use freeze (split with "==")
##  -- changed to use --format json to let someone else do the parsing for me...

from __future__ import print_function

from multiprocessing import Pool, cpu_count
from subprocess import PIPE, Popen

import json
import argparse
import functools

__version__ = "1.5"


def run_command(command):
    """
    Executes a command.
    @param: command
    @returns: stdout, stderr
    """
    stdout, stderror = Popen(command,
                             stdout=PIPE,
                             stderr=PIPE,
                             shell=True).communicate()
    return stdout, stderror


def upgrade_package(package, pip_cmd="pip", pip_args="", verbose=False, dry_run=False):
    """
    Upgrade a package.

    @param: package or space-joined list of packages
    """

    upgrade_command = " ".join((pip_cmd, "install {} --upgrade {}".format(" ".join(pip_args), package)))

    if verbose:
        print("Upgrade command: ", upgrade_command)

    # Skip actually running the command on a dry run
    if dry_run:
        return

    stdout, stderr = run_command(upgrade_command)
    if stderr:
        print("Error:", stderr.decode())

    print(stdout.decode())


def collect_packages(pip_cmd="pip", verbose=False):
    """
    Collect outdated packages.

    @returns : list of packages
    """

    outdated_command = " ".join((pip_cmd, "list --outdated --format json"))
    stdout, stderr = run_command(outdated_command)

    if stderr:
        print("Error:", stderr.decode())

    if verbose and stdout and stdout != b'[]\n':
        print(stdout.decode())

    ### decode needed for python 3.5?
    pkgs = json.loads(stdout.decode())

    ### only if verbose?
    for p in pkgs:
        print("{}: {} ({})".format(p['name'], p['latest_version'], p['latest_filetype']))

    return [p['name'] for p in pkgs]


def main():
    """ Upgrade outdated python packages. """

    ## AHJ: all argparse stuff new
    descr = 'Upgrade outdated python packages with pip. Any unknown arguments will be passed to pip.'

    parser = argparse.ArgumentParser(description=descr)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-3", dest="pip_cmd", action="store_const", const="pip3", default="pip", help="use pip3")
    group.add_argument("-2", dest="pip_cmd", action="store_const", const="pip2", default="pip", help="use pip2")
    group.add_argument("--pip_cmd", action="store", default="pip", help="use PIP_CMD (default pip)")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--serial", "-s", action="store_true", default=True, help="upgrade in serial via a single batch pip upgrade command (default)")
    group.add_argument("--parallel", "-p", action="store_true", default=False, help="upgrade in parallel via individual pip ugrade commands")
    group.add_argument("--sequential", "-q", action="store_true", default=False, help="upgrade in serial via individual pip ugrade commands")

    parser.add_argument("--user", "-u", dest="user", action="store_const", const="--user", default="",
                        help="Adds the --user flag when installing the packages")

    parser.add_argument("--dry_run", "-n", action="store_true", help="get list, but don't upgrade")

    parser.add_argument("--verbose", "-v", action="count", default=0, help="may be specified multiple times")
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)

    parser.add_argument('--exclude', '-x', action='append', metavar='PKG', help='exclude PKG; may be specified multiple times')

    args, pip_args = parser.parse_known_args()
    
    if args.parallel or args.sequential:
        ## special case since is the default of the mutually exclusive group above
        args.serial = False   

    pip_cmd = args.pip_cmd

    ## special case --user flag so it appears in the help
    if args.user:
        pip_args.append(args.user)

    if args.verbose > 1:
        print(args)
        print("pip_cmd=%s" % pip_cmd)
        if pip_args:
            print("pip_args:", pip_args)

    packages = collect_packages(pip_cmd=pip_cmd, verbose=args.verbose)
    if args.verbose:
        if packages:
            print("Outdated packages: ", packages)
        else:
            print("No outdated packages.")

    if args.exclude:
        excluded = []
        for ex in args.exclude:
            if ex in packages:
                packages.remove(ex)
                excluded.append(ex)
        if args.verbose:
            print("Excluded: ", excluded)

    if not packages:
        return

    if args.parallel:
        if args.verbose > 1:
            print("Parallel execution")
        pool = Pool(cpu_count())
        pool.map(functools.partial(upgrade_package, pip_cmd=pip_cmd, pip_args=pip_args, verbose=args.verbose,
                 dry_run=args.dry_run), packages)
        pool.close()
        pool.join()
    elif args.sequential:
        if args.verbose > 1:
            print("Sequential execution")
        # Upgrade each package as a separate command in case one package fails to upgrade, others still are upgraded
        for package in packages:
            upgrade_package(package, pip_cmd=pip_cmd, pip_args=pip_args, verbose=args.verbose, dry_run=args.dry_run)
    elif args.serial:
        if args.verbose > 1:
            print("Serial (batch) execution")
        all_packages = " ".join(packages)
        upgrade_package(all_packages, pip_cmd=pip_cmd, pip_args=pip_args, verbose=args.verbose,
                        dry_run=args.dry_run)
