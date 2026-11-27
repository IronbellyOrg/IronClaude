# Notes for NP-3 (TASK-WF-authorizedNarrow-20261106-214325)

## Dropped findings

- M-004 ('superseding the earlier bash-only limit' cites a limit source.md never states): true but a justification-wording issue with no effect on what an implementer builds; treated as a wording nit.
- Plan notes rejected by the debate (interim verify-sync failure window between Task 1 and Task 3; launcher half of 'launcher/harness' documentation-only): the report records them as not findings.
- Implementation-time review records (artifacts/retries/T2/review-1.md F1.1 and T3/review-1.md F1.1, both graded blocking) concern code defects (ticket published before permission evaluation; UV check before binding check). They are defects of code written during implementation, not of the plan text, so they are not items and do not make any item blocking.

## Verification and caveats

- Base: first 'start sha=' (3ca8984d...) is a tree hash, not a commit. The recorded HEAD at task start (artifacts/retries/T1/q0-head = 7065667af204d4e58613e61e4f1e93616b757033) is a real commit. The start tree equals that commit plus one dirty file: docs/designs/sc-issue-launch-level-hook.md, whose uncommitted version already contains section 19 (the plan's Task 4 updates it and the source cites section 19.1). Section 19 does NOT exist at the base commit, so a sandbox built from base lacks that section; none of the 5 items depends on it. Flagged as a caveat.
- Files the plan edits exist at base (install_hooks.py with _FRESHNESS_SCRIPTS, src and plugin hooks.json, tests/cli/test_install_hooks.py, the design doc, Makefile). Files the implementation created (src and plugins launch-job-identity.sh, tests/hooks/test_launch_job_identity.py, tests/hooks/fixtures/launch_level/live_probe.py) are absent at base, so masked_paths is empty. The design doc was edited, not created, so it is not masked.
- Plan text verified: sha256 of the done-folder plan equals the PLAN: hash in progress.md (881cacd5...); every plan line cited by the report (21,25,31,35,37,53,61,64,66) says what the report says.
- No blocking items: all six report findings are non-blocking (M-001 is MAJOR in the findings-v2 vocabulary but the report states 'Blocking = false either way').
