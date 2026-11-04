# Round 2 — Variant 1 Advocate rebuttal

## Response to criticisms
- V2, R1-3 only a labelling issue: partly conceded. Plan :89 keeps the entry on purpose, so nothing breaks; but Task 1 says "Use exactly these classes and assignments" (plan :33) and plan :35 lists the entry under "rewrite to Orca's default location", so the inventory would record an action Task 4 never takes. Stays a low necessary deviation needing a one-line label fix.
- V2, SKILL.md:267 left as inferred: conceded on form, rejected on substance. The fallback runs "only if origin has no URL", says "never prefer it, because gh picks an `upstream` remote", and every script passes `--repo "$REPO"`; same guard in the scripts (e.g. poll-augment-review.sh:22). Informational, outside Task 3, already guarded.
- V3, R1-6 "authorized": conceded for fetch and pull (literal reading of source.md:1; C-005 goes to V2). The dated Orca project-id bullet (plan :76) remains an authorized expansion backed by the MEMORY.md "no ... Orca link" entry.
- V3, grep treated as full scope: conceded (eval_runner.py:143).
- V3, vacuous test run: conceded; test_git_replay_integration.py:56-68 skips on shallow clones, test_implement_retry_revert.py:357 skips as root; fix: run with `-rs` and require zero SKIPPED lines in the saved artifact.

## Updated assessment of other variants
- V3: R3-F1 is still the most valuable single finding. Its check-1 fix is sound, but it leaves CLAUDE.md:66 "close it immediately and reopen", and its AC passes with that line in place.
- V2: R2-F4 withdrawn by its own advocate; R2-F3 equals R1-4 in substance with a useful fixture citation (:613); misses C-001.

## New evidence
- sc-pr-submit SKILL.md:267 fallback guarded; same guard at poll-ci-checks.sh:35, reply-resolve-thread.sh:57, retrigger-review.sh:50, poll-augment-review.sh:22. U-007 real but low.
- Re-confirmed CLAUDE.md:66 "If it shows the wrong owner, close it immediately and reopen" — only V1 names it.

## Final per-point positions
| Point | Superior | Reason |
|---|---|---|
| S-001 | 2 | Only explicit missing-requirements audit |
| S-002 | 1 | Mixed labels fit the taxonomy (R1-6 partly mislabelled) |
| S-003 | 1 | Engages F1-F4 with verified corrections |
| C-001 | 1 | Only card covering CLAUDE.md:64 and :66 |
| C-002 | tie | All three demand a decision on :251 |
| C-003 | 1 | Necessary class plus Blocked-status correction |
| C-004 | tie (changed from 1) | Same three tests; both need a zero-skip guard |
| C-005 | 2 | Literal reading, not an expansion |
| X-001 | 2 | Plan :73 "no ... link" covers a static URL |
| X-002 | 3 | eval_runner.py:143 list arguments, never removed |
| A-001 | tie (changed from 1) | Cards silent; advocates agree only routing_table.py:352 reads root CLAUDE.md |
| A-002 | tie | Holds on this host only |
| A-003 | 3 | skipif at test_git_replay_integration.py:56 |
