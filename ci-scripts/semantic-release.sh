#!/usr/bin/env bash

# shellcheck source=ci-scripts/common.sh
SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}"/common.sh

parse_environment_variables() {
    GITHUB_TOKEN=${GITHUB_TOKEN:?'GITHUB_TOKEN variable missing.'}
}

install_dependencies() {
    sudo npm install --silent --global \
        semantic-release \
        @semantic-release/changelog \
        @semantic-release/exec \
        @semantic-release/git \
        @semantic-release/github
}

enable_debug
parse_environment_variables
install_dependencies
npx semantic-release --debug
