#!/usr/bin/env bash

semantic_release() {
    npm install --silent
    npm run semantic-release
}

semantic_release
