# Wave 1.6 Branch B (log-config inspection), persisted on receipt; degraded: true (auggie not in roster)
- collect-conflict-evidence.sh:30 `set -u -o pipefail`, no `set -e`; every failure is an explicit `|| fail <reason>`.
- :32-33 LIMIT_SECONDS=60, DEADLINE=SECONDS+60; :68-70 check_deadline fails `timeout` once SECONDS >= DEADLINE.
- :76, :86 bounded checks the deadline before and after each command; :78-81 `timeout "$remaining"` only when on PATH, exit 124 -> `fail timeout`; :83-86 without `timeout` a slow command is caught only by the after-check.
- :43 `trap cleanup EXIT`; :37-42 removes $TMP under `git rev-parse --git-path sc-pr-submit-tmp`; writes nothing to stdout.
- :47 `exec 3>&1 4>&2`; :49-54 fail writes detail to fd 4 and the one line `EVIDENCE_FAIL <reason>` to fd 3, exit 2, so a failure inside capture (:185, stdout to $TMP/raw) still reaches the caller.
- :25-26 reasons usage | foreign_merge | out_not_empty | unreadable | timeout; :240-244 success is one jq JSON line, exit 0.
- refs/conflict-intent.md:30 any EVIDENCE_FAIL escalates to Tier 3, abort, `sync_tier3` (general rule :12; call site :19).
- refs/conflict-mechanical.md:296 halt row `sync_tier3` (trigger list includes "evidence failure"); :95 Tier 2 halt step; :216 abort = ownership check then `sync_concluded{aborted}`; :275 every halt is `terminal_halted{reason}` after `sync_concluded`.
- Gap (informational): the specific EVIDENCE_FAIL reason and stderr detail are not written to the run-log; only `sync_tier3` is recorded.
