# Reflect report: pre-execution audit of the pr-submit merge guard plan (UC-1, Tier 2, shadow panel)

- Run: pre-TASK-WF-designSpec-20261107-075614-comboE-r1 (eval combo E: SONNET alias claude-haiku-5-5, HAIKU alias gpt-6-luna, OPUS alias claude-gw-tier4)
- Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md
- Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (13 tasks)
- Status: **partial** (7 citations in the three reviewer cards were dropped by the evidence validator; every citation in this report survived)
- Tier reached: 2 (pinned with `--tier 2`; also C=0.60 < 0.85 and `coverage_degraded: parsed-sparse`)
- Mode: pre. Engine: `--t2-engine shadow` (legacy rotation and debate authoritative; panel artifacts under `panel/`)
- Merge: adversarial, convergence 0.8947, judge claude-gw-tier1b (distinct from the three reviewer pins)

## Verdict: REVISE

The plan covers the spec's files, tests and dependencies. Two acceptance-criteria gaps are blocking and four spec points need a decision before an implementer can follow them without guessing.

## Attribution note
This package already executed (commit 0b8a5801d, parent 0e486ab8d). Spec facts F1-F13 were re-read at 0e486ab8d and hold there. The reviewers judged the plan against the spec text, not against the shipped files. HEAD now carries the implementation.

## Findings (merged, validated)
| ID | Severity | Blocking | Summary | Evidence |
|---|---|---|---|---|
| M1 | MAJOR | yes | Task 11 ACs check test names, trace order, crash derivation and forbidden calls only; no AC asserts foreign-toggle continuation, engage failure halting before any edit, validation failure leaving held, or the one-retry release. | plan:168-173, spec:305-322 |
| M2 | MAJOR | yes | One cycle_id shared by guard, push triad and rereview_requested (spec 4.6) has no AC; Task 8 AC only names the minting place. | spec:251, plan:126-127,170 |
| M3 | MAJOR | no | Spec says a draft_guard_unavailable halt reports unavailable, but the first-match guard_status mapping gives released for a halt that wrote no request; Task 3 AC pins released. | spec:112,135, plan:61 |
| M4 | MINOR | no | Fold row for user_override sets DISABLED with no disabled_cause; guard_status needs it. | spec:206,112, plan:60-61 |
| M5 | MAJOR | no | resume_decision row 4 re-enters release_decision, which needs target_sha and applied_edits; the signature carries neither. | spec:166,107-109, plan:70,77 |
| M6 | MAJOR | no | Section 3 says resume reconciles at any ordinal; row 2 returns REPORT_HELD first below ordinal 3 or with mode off; Task 4 AC pins row 2. | spec:58,164, plan:76 |
| M7 | MINOR | no | Wave 0 bullet: "no L3 condition" vs printing the off line at L3. | spec:241, plan:137,140 |
| M8 | MINOR | no | "No file:NNN pointers" rule has no AC. | plan:23,126-130, spec:369 |
| M9 | MINOR | no | No multi-page timeline AC for `gh api --paginate`. | spec:230, plan:108,111-113 |
| M10 | MINOR | no | Idempotency of `--to` tested only for already-draft. | spec:234, plan:111 |
| M11 | MINOR | no | Task 2 AC3 (grep "43") is a judgment call. | plan:49 |
| M12 | MINOR | no | Task 6 "RunConfig unchanged" has no AC. | spec:217, plan:98-102 |
| M13 | MINOR | no | Held report must carry the reason; Task 8 AC omits it. | spec:247, plan:129 |
| M14 | MINOR | no | Unreadable timeline at a later checkpoint has no AC. | spec:67, plan:129,166-173 |
| M15 | MINOR | no | The scenario driver applies the pure decisions itself, so passing it does not show SKILL orchestration follows them. | plan:166-173, spec:257-280 |

Considered and dropped: V1 F7 (pre-push halt uncovered) was refuted in part by plan:150-153 and plan:172; its residual is M15. INV-002 (user docs AC) is advisory.

## Recommended edits
1. M1: add to Task 11 an AC per scenario that names the observable result (for example, foreign toggle: phase DISABLED, run continues, `merge_guard: user_override`).
2. M2: add an AC that the guard events, push_initiated and rereview_requested of one cycle carry the same cycle_id.
3. M3-M6: ask the spec owner to settle the four points (halt vs `released`, `disabled_cause`, `resume_decision` inputs, resume row 2 vs section 3) before Tasks 3 and 4.
4. M8-M13: one-line AC additions in Tasks 2, 6, 7 and 8.

## Coverage (UC-1)
- Pass 1: 0 labelled IDs in the spec or the plan. Pass 2: 32 inferred rows, every quote verified verbatim.
- `coverage_pct`: null (no parsed rows). `coverage_pct_union`: 0.75 (24 of 32). `coverage_degraded: parsed-sparse`.
- Matcher misses INF-004, INF-014, INF-015, INF-011 are word-overlap noise: a task states each item. INF-026 (M8) and INF-019 (M2) are real gaps.

## Inferred requirements (Pass 2)
| ID | Quote | Citation | Match |
|---|---|---|---|
| INF-001 | engage at the first verified Medium-or-higher finding routed to a fix | source.md:6 | Task 8 |
| INF-002 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | source.md:6 | Task 8 |
| INF-003 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | source.md:6 | Task 8 |
| INF-004 | No `gh` or `git` word on any line, comments included (F6). | source.md:75 | none |
| INF-005 | Never collides with `CONFLICT_CYCLE_PREFIXES`. | source.md:101 | Task 3 |
| INF-006 | It is the only way resume learns that a held cycle's push completed normally (F13). | source.md:108 | Task 8 |
| INF-007 | A halt with reason `draft_guard_unavailable` reports `unavailable`. | source.md:112 | Task 8 |
| INF-008 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | source.md:127 | Task 4 |
| INF-009 | `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) | source.md:133 | Task 4 |
| INF-010 | 43 to 45, update the docstring | source.md:175 | Task 2 |
| INF-011 | It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. | source.md:201 | none |
| INF-012 | `original_is_draft` is never read from GitHub after the first record | source.md:208 | Task 3 |
| INF-013 | Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | none |
| INF-014 | `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated. | source.md:217 | none |
| INF-015 | `--to` is idempotent, so a retry or a resume re-issue is safe. | source.md:234 | none |
| INF-016 | Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | Task 8 |
| INF-017 | No new python fence | source.md:241 | Task 9 |
| INF-018 | A `held` report always carries the reason and | source.md:247 | Task 8 |
| INF-019 | keep exactly one source for it (open item O1) | source.md:251 | none |
| INF-020 | The `read-only` category is not used for these calls | source.md:255 | Task 1 |
| INF-021 | Acceptance trace (must appear in this order in the run log) | source.md:270 | Task 11 |
| INF-022 | Run `make sync-dev` at the end of every task that edits a file under | source.md:301 | Task 8 |
| INF-023 | the run that opens the PR must not enable the feature (`--merge-guard off`) | source.md:326 | Task 1 |
| INF-024 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | source.md:322 | Task 3 |
| INF-025 | Cite tests and constants by symbol name | source.md:362 | Task 1 |
| INF-026 | Protocol prose written by the plan never carries `file:NNN` pointers | source.md:369 | none |
| INF-027 | The L2 line is written into the SKILL.md output table | source.md:374 | Task 9 |
| INF-028 | a settled `not_applied` of either direction returns to `phase_before_request` | source.md:376 | Task 3 |
| INF-029 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | source.md:64 | Task 8 |
| INF-030 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | source.md:65 | Task 8 |
| INF-031 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | source.md:68 | Task 8 |
| INF-032 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | source.md:66 | none |

## Grounding gaps and dropped citations
- Dropped by the evidence validator (reviewer cards only): reviewer-1 F4 spec:151 (the row is at spec:206); reviewer-2 F4 spec:420 (the spec has 378 lines); reviewer-3 F7 (path with a doubled prefix); reviewer-2 F1, F2, F3 and F5 spec citations (resolve but unrelated). Each finding kept at least one resolving citation; the merged findings above use verified citations.
- Zero-drop flag: not set (7 dropped).
- Citation policy: full re-read. citations_total 92 (39 report, 53 card), revalidated 92, dropped 7.

## Process notes (deviations from the skill, recorded)
- The calibrator was in the sonnet class, the same class as reviewer 1 (every class was a reviewer): `calibrator_diversity: degraded`.
- Debate Round 2 ran for advocate 1 only; the merge-executor agent was not dispatched (the orchestrator wrote the merge); dual-pass base-selection scoring was not run.
- Reviewer self-reports differ from the pins for all three cards (identity_source stays requested-pinned): reviewer 1 reported claude-haiku-5-5, reviewer 2 gpt-6-luna, reviewer 3 claude-gw-tier4.
- The input snapshot was rewritten with repo-relative paths before dispatch so citation checks resolve.
