# Troubleshoot: poll-augment-review.sh ARG_MAX

**status:** success
**tier_reached:** 1
**confidence:** 0.95

## Diagnosis

`poll-augment-review.sh:79-85` merged issue + inline comments with `jq --argjson`, which places the JSON on **argv**. Busy Augment threads (Fix-This URLs) exceed ARG_MAX → `/usr/bin/jq: Argument list too long`. Observed on PR 238.

## Fix

Write comment JSON to temp files; merge with `jq --slurpfile` (file/stdin, not argv). Tests: static grep forbids `--argjson issue_comments`; 2MB inline stub still parses.

Commit: `cead8a7c` on `feature/sc-implement-protocol`.
