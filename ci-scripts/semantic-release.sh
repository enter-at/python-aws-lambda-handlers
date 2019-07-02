#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}"/common.sh

enable_debug
npm install
ls -la
npm run semantic-release
semantic_release
