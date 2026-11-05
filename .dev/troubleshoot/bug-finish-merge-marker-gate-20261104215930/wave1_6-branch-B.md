# Wave 1.6 Branch B (log-config inspection), persisted on receipt; degraded: true (auggie not in roster)
- finish-merge.sh:19-47: fail() writes one detail line to stderr and one `FINISH_FAIL <reason>` line to stdout, unconditionally; set -u -o pipefail; EXIT trap removes temp dir.
- finish-merge.sh:206-212 (:208): marker width hard-coded to 7 (each alternative followed by space or end of line); not read from git. Unobserved hypothesis: a CRLF `=======\r` line also misses.
- finish-merge.sh:231-232: markers detail reports counts only.
- finish-merge.sh:235-251 (:246-249): path lists come from name-only diffs that DO list mode-only changes; the comparison is blob-id only, so a mode-only change passes with no output at all.
- finish-merge.sh:253-258, :270-280: commit output re-emitted to stderr; step 8 checks clean tree only; no committed-mode check.
- refs/conflict-mechanical.md:3, :103-120, :291: caller consumes the token; a silent pass yields exit 0 + JSON.
- refs/conflict-mechanical.md:73-78: merge runs with -c merge.conflictStyle=zdiff3 -c rerere.enabled=false; no conflict-marker-size override; width follows the per-path gitattribute (repo .gitattributes, .git/info/attributes, core.attributesFile). No .gitattributes in this worktree.
- tests/pr_submit/test_conflict_scripts.py:48-64: hermetic env (GIT_CONFIG_GLOBAL=/dev/null, HOME in tmp) -> default width 7 only; no test covers wider markers, CRLF markers or a mode-only change; the harness stays green with both bugs.
- reachability_verdicts (forced unknown, degraded): :42, :232, :248, :255.
