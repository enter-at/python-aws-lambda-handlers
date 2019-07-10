#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}"/common.sh

version=$1
echo "new version ${version}"
echo "\"\"\"Release version number.\"\"\"\n__version__ = '${version}'  # noqa" >> lambda_handlers/version.py
