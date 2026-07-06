#!/bin/bash

git config --global --show-origin --get-regexp '^url\.' || true
git config --global url."https://github.com/".insteadOf "git@github.com:"

# Verify Git now rewrites the exact failing clone target to HTTPS.
GIT_TRACE=1 git ls-remote git@github.com:danielrosehill/Claude-Sysadmin-Homelab-Plugin.git HEAD
