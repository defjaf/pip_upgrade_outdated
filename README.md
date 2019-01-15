# pip_upgrade_outdated

Run `pip install --upgrade` for all outdated packages (`pip list --outdated`).

Allow specifying which version of `pip` to run, and parallel or serial execution of the upgrade step.

### Command line usage

```
usage: pip_upgrade_outdated [-h] [-3 | -2 | --pip_cmd PIP_CMD]
                            [--serial | --parallel]
                            [--sequential_run | --batch_run] [--user]
                            [--dry_run] [--verbose] [--version]
                            [--exclude PKG]

Upgrade outdated python packages with pip. Any unknown arguments will be passed to pip.

optional arguments:
  -h, --help            show this help message and exit
  -3                    use pip3
  -2                    use pip2
  --pip_cmd PIP_CMD     use PIP_CMD (default pip)
  --serial, -s          upgrade in serial via a single pip upgrade command (default)
  --parallel, -p        upgrade in parallel via individual pip upgrade commands
  --sequential, -q      upgrade in serial via individual pip upgrade commands
  --user, -u            Adds the --user flag when installing the packages
  --dry_run, -n         get list, but don't upgrade
  --verbose, -v         may be specified multiple times
  --version             show program's version number and exit
  --exclude PKG, -x PKG
                        exclude PKG; may be specified multiple times
```

### TODO

* Need better error handling?
* Should the script explicitly return a value to the shell?
* allow patterns in exclude option

### Sources

* code based on https://gist.github.com/serafeimgr/b4ca5d0de63950cc5349d4802d22f3f0
* project structure based on https://gehrcke.de/2014/02/distributing-a-python-command-line-application/
