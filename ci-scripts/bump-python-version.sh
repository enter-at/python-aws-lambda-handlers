#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "$0")
source "${SCRIPT_PATH}"/common.sh

version=$1
echo "new version ${version}"
(
cat <<EOF
"""Release version number."""
__version__ = '${version}'  # noqa
EOF
) >lambda_handlers/version.py
