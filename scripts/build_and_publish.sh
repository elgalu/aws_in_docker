#!/usr/bin/env bash

# Purpose: Build and publish the package into public PyPi
#
# Tested on:
# - Linux: Ubuntu 20.04.2 LTS
# - OSX..: TODO

# set -e: exit asap if a command exits with a non-zero status
set -e

# set -o pipefail: Don't mask errors from a command piped into another command
set -o pipefail

# set -x: prints all lines before running debug (debugging)
set -x

# set -u: treat unset variables as an error and exit immediately
set -u

poetry build

poetry publish
