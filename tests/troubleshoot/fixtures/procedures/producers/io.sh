#!/usr/bin/env bash
# ## Mechanism rows — decoy heading inside a comment: rc=runner-unavailable must not count
aidev_seed_now() {
  IFS=' ' read -r up _ </proc/uptime || return 1
  prefix=runner
  rc=$prefix-unavailable
  [ -x "$(command -v git)" ] || { rc=runner-unavailable; return 1; }
  timeout 120 git clone "$REPO_URL" || { rc=runner-unavailable; exit 2; }
  rc=cloned
}
aidev_seed_now
echo "seed-repo-outcome=$rc"
