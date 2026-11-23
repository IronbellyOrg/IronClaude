# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/source.md` (inline prompt, one line). Plan: `.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/TASK-WF-buildRelease1OfT-20261111-164757.md` (14 tasks, 5 phases). Canonical contract the plan cites: `.dev/issues/409/bmad/spec-orca-observer/` (SPEC.md and companions).

## Step 1B.0 requirement extraction

Pass 1 (labelled IDs): zero parsed rows (the prompt has no `<PREFIX>-NNN` tokens). Pass 2 (inferred, each quote from source.md line 1): 23 rows INF-001 to INF-023, below.

| ID | Quote (source.md:1) | Mapped task(s) |
|---|---|---|
| INF-001 | "a standalone Python + Rich command (recommended name `superclaude observe`)" | 12, 13 |
| INF-002 | "R0 offline foundation (fixture replay" | 5, 7, 12 |
| INF-003 | "ledger screen" | 10 |
| INF-004 | "inspector" | 8, 10 |
| INF-005 | "plain-text export at 160/116/80 columns" | 11, 12 |
| INF-006 | "sanitizer" | 2 |
| INF-007 | "cell-width truncation" | 3 |
| INF-008 | "NO_COLOR" | 3 |
| INF-009 | "redacted golden worker-list fixture" | 14 |
| INF-010 | "Rich Live + stdlib key-reader spike" | 1 |
| INF-011 | "R1 live worker-list" | 6, 7, 12 |
| INF-012 | "counts and freshness strips" | 8, 10 |
| INF-013 | "worker ledger with verbatim nextAction.kind" | 8, 10 |
| INF-014 | "capped paging" | 6, 7 |
| INF-015 | "STALE after 45 s" | 8 |
| INF-016 | "UNKNOWN sentinel" | 4, 8 |
| INF-017 | "changes since last look" | 8, 9 |
| INF-018 | "Attention Ledger 'question source UNVERIFIED' notice" | 8, 10 |
| INF-019 | "`export(view)` writing a versioned additive-only JSON snapshot with a schema test" | 11 |
| INF-020 | "One view model, pure render/export functions" | 8, 10, 11 |
| INF-021 | "read-only (no write-back)" | 6, 12 |
| INF-022 | "Out of scope: R2 question ledger, R3 decision desk, R4 remote fleet, write-back, any TUIBBS code" | Constraints |
| INF-023 | "Snapshot fields to freeze: .dev/issues/409/tuibbs-review/architecture-options.md" | 11 |

coverage_pct (parsed-only): null (0 parsed rows). coverage_pct_union: 1.00 (23 of 23 mapped by name containment, hand-checked, not by the deterministic matcher). `coverage_degraded: parsed-sparse` (inferred 23 > parsed 0), so no Tier 1 stop is allowed; route to Tier 2.

## Tier 1 findings (grounded in the plan file)

- F1 (gap): FixtureSource has no defined `source.namespace`; Task 7 and Task 11 need one for row identity and the snapshot envelope, and only the live path derives it (Task 6).
- F2 (risk): Task 14 blocks without a live Orca CLI, and its four `golden-*.json` files feed `test_golden_contract.py`; the release cannot finish its data gate offline.
- F3 (risk): Task 13 acceptance "git diff touches main.py only by two lines" is brittle in a worktree that has other changes.
- F4 (minor): the `--width` option and the "`--once` writes a snapshot only with `--snapshot`" rule are plan-author rules but only some are listed in the Constraints rules paragraph.
- F5 (minor): packaging of `snapshot.schema.json` and `fixtures/` is checked only with `importlib.resources` in a source checkout, not in a built wheel.
- F6 (deviation from spec CAP-1): Attention Ledger and Decision Desk fixture renders (T50) are not built; justified by the owner's staged-direction choice but the owner has not seen R0 renders.

Self-reported confidence: 0.78.
