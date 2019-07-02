#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}"/common.sh

enable_debug
npm install
npm run semantic-release
