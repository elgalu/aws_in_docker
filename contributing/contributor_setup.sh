#!/usr/bin/env bash

# This file bootstraps or makes sure contributors are setup for this project
# Based on: https://github.com/pyenv/pyenv-installer/raw/6f1a69aaa56ea/bin/pyenv-installer
#
# Tested on:
# - Linux: Ubuntu 20.04.2 LTS
# - OSX..: TODO

# set -e: exit asap if a command exits with a non-zero status
set -e

# set -o pipefail: Don't mask errors from a command piped into another command
set -o pipefail

# set -x: prints all lines before running debug (debugging)
[ -n "${DEBUG}" ] && set -x
[ -n "${PYENV_DEBUG}" ] && set -x

#-------------------------#
#--- Program Variables ---#
#-------------------------#
[ -z "$PYENV_ROOT" ] && export PYENV_ROOT="${HOME}/.pyenv"
# PYENV_BIN="$HOME/.pyenv/bin/pyenv"
if [ -n "${USE_GIT_URI}" ]; then
    GITHUB="git://github.com"
else
    GITHUB="https://github.com"
fi

# set -u: treat unset variables as an error and exit immediately
set -u

#----------------------------#
#--- OSX vs Linux tooling ---#
#----------------------------#
if [ "$(uname)" == 'Darwin' ]; then
    export _tee='gtee'
    export _cut='gcut'
    export _sed='gsed'
    export _tail='gtail'
    export _date='gdate'
    export _timeout='gtimeout'
else
    export _tee='tee'
    export _cut='cut'
    export _sed='sed'
    export _tail='tail'
    export _date='date'
    export _timeout='timeout'
fi

#------------------------#
#--- Helper Functions ---#
#------------------------#
## Output to standard error
function util.log.error() {
    printf "ERROR $(${_date} "+%H:%M:%S:%N") %s\n" "$*" >&2;
}

## Output a warning to standard output
function util.log.warn() {
    printf "WARN $(${_date} "+%H:%M:%S:%N") %s\n" "$*" >&2;
}

## Output an info standard output
function util.log.info() {
    printf "INFO $(${_date} "+%H:%M:%S:%N") %s\n" "$*" >&1;
}

## Output a new line break to stdout
function util.log.newline() {
    printf "\n" >&1;
}

## Print an error and exit, failing
function util.die() {
    util.log.error "$1"
    # if $2 is defined AND NOT EMPTY, use $2; otherwise, set the exit code to: 150
    errnum=${2-150}
    exit ${errnum}
}

## Git clone each pyenv dependency repo
function checkout() {
    [ -d "$2" ] || git clone --depth 1 "$1" "$2" || util.die "Failed to git clone $1"
}

#-------------------#
#--- PyEnv Setup ---#
#-------------------#
function install_pyenv() {
    checkout "${GITHUB}/pyenv/pyenv.git"            "${PYENV_ROOT}"
    checkout "${GITHUB}/pyenv/pyenv-doctor.git"     "${PYENV_ROOT}/plugins/pyenv-doctor"
    checkout "${GITHUB}/pyenv/pyenv-installer.git"  "${PYENV_ROOT}/plugins/pyenv-installer"
    checkout "${GITHUB}/pyenv/pyenv-update.git"     "${PYENV_ROOT}/plugins/pyenv-update"
    checkout "${GITHUB}/pyenv/pyenv-virtualenv.git" "${PYENV_ROOT}/plugins/pyenv-virtualenv"
    checkout "${GITHUB}/pyenv/pyenv-which-ext.git"  "${PYENV_ROOT}/plugins/pyenv-which-ext"
}

if ! command -v git 1>/dev/null 2>&1; then
    die "pyenv: Git is not installed, can't continue."
fi

# Checks for `.pyenv` file, and suggests to remove it for installing
if [ -d "${PYENV_ROOT}" ]; then
    util.log.info "PyEnv seems to be installed already at '${PYENV_ROOT}'."
else
    install_pyenv
fi

# if ! command -v "${PYENV_BIN}" 1>/dev/null; then
#   { echo
#     colorize 1 "WARNING"
#     echo ": PyEnv is not working."
#     echo
#   } >&2

#   { # Without args, `init` commands print installation help
#     "${PYENV_ROOT}/bin/pyenv" init || true
#     "${PYENV_ROOT}/bin/pyenv" virtualenv-init || true
#   } >&2

#   exit 2
# fi

if ! command -v pyenv 1>/dev/null; then
    util.log.error "seems you still have not added 'pyenv' to the load path."

    { # Without args, `init` commands print installation help
        "${PYENV_ROOT}/bin/pyenv" init || true
        "${PYENV_ROOT}/bin/pyenv" virtualenv-init || true
    } >&2

    if eval "$(${PYENV_ROOT}/bin/pyenv init -)"; then
        util.log.info "PyEnv initialized"
    else
        die "PyEnv failed to initialize with init -"
    fi
fi

#---------------------------------#
#--- Python & VirtualEnv Setup ---#
#---------------------------------#
function pyenv_ensure_required_python_version() {
    local _required_python_version=$(cat .python-version)
    pyenv install "${_required_python_version}" --skip-existing
}

function ensure_venv() {
    if [ ! -d ".venv" ]; then
        python -m venv .venv
        .venv/bin/python -m pip install --upgrade pip
    fi
}

pyenv_ensure_required_python_version || die "Failed to pyenv_ensure_required_python_version"

ensure_venv || die "Failed to create .venv"

source .venv/bin/activate || die "Failed to activate the virtual environment"

pip install poetry || die "Failed to install Poetry in the virtual environment"

# --no-root: Do not install the root package (your project).
poetry install --no-root || die "Failed to poetry install all required dependencies"

# let's make sure `poetry run` works
poetry run invoke setup || die "Failed to invoke setup"

# let's make sure we don't need `poetry run` since the .venv is activated anyways
invoke tests || die "Failed to run tests"

invoke hooks || die "Failed to run hooks"

util.log.info "SUCCESS! Now activate your environment with: source .venv/bin/activate"
