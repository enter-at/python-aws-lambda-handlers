#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}"/common.sh

parse_environment_variables() {
    export TWINE_USERNAME=${PYPI_USER:?'PYPI_USER variable missing.'}
    export TWINE_PASSWORD=${PYPI_PASS:?'PYPI_PASS variable missing.'}
}

pypi_release() {
    make release
}

enable_debug
parse_environment_variables
pypi_release
