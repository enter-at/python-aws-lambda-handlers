#!/usr/bin/env bash

version=$1
echo "new version ${version}"
echo "__version__ = '${version}'" >lambda_handlers/version.py
