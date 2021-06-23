#!/usr/bin/env bash

#
# Purpose: Merge current branch into main
#

# set -e: exit asap if a command exits with a non-zero status
set -e

# set -o pipefail: Don't mask errors from a command piped into another command
set -o pipefail

# set -x: prints all lines before running debug (debugging)
set -x

# set -u: treat unset variables as an error and exit immediately
set -u

_VERSION="$(python -c 'from aws_in_docker import __version__; print(__version__)')"

git checkout "main"
git merge "release-${_VERSION}"
git push
git branch --delete "release-${_VERSION}"
