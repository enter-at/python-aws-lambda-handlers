#!/usr/bin/env bash

semantic_release() {
    npm install --silent
    npm run semantic-release
}

ls -la
semantic_release
