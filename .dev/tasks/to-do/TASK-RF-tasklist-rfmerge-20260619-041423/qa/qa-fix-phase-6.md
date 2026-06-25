# QA Fix Report — Phase 6 (P5) Tier Calibration Advisory

**Date:** 2026-06-19
**Phase:** fix-cycle (Step 6.G9, cycle 1)
**Agent:** rf-qa (single fix agent, fix_authorization: true)
**Consolidated findings:** qa/qa-consolidated-findings-phase-6.md
**Verdict on fixes:** ALL 8 (C6-01..C6-08) APPLIED — tests green, in sync.

---

## Source-of-truth discipline

- All edits applied to `src/superclaude/skills/sc-tasklist-protocol/` only.
- `.claude/` mirror regenerated via `make sync-dev` (NOT hand-edited). `git status .claude/` shows no tracked changes (gitignored sync output).
- Tests read from `src/` (`_TASKLIST_SKILL_DIR = src/superclaude/skills/sc-tasklist-protocol`), so asserts validate the source of truth directly.

---

## SKILL.md advisory reconciliation (C6-01 .. C6-05)

All within `#### Tier Calibration Advisory (P5 — RETAINED advisory-only)` (SKILL.md ~:866-889).

| ID | Severity | Fix applied |
|----|----------|-------------|
| C6-01 | CRITICAL | Replaced the non-existent `roadmap_item_id`/`task_signature`/`suggested_tier` field names with the EXISTING Feedback Collection Template columns. New **Match + threshold** paragraph: a row matches when its `Task ID` equals the task's `T<PP>.<TT>`; a "matching override" = matched row whose `Override Tier` is non-blank AND differs from the deterministically-scored tier; `Feedback-suggested tier` column ← `Override Tier`; `Scored tier` column ← the task's current scored tier. Explicit mapping note added (`roadmap_item_id`/`task_signature`→`Task ID`, `suggested_tier`→`Override Tier`). |
| C6-02 | IMPORTANT | New **Deterministic emission** paragraph: one advisory row per distinct `(Task ID, Override Tier)` pair, ordered ascending by `T<PP>.<TT>` (i.e. `Task ID`) then `Override Tier` ascending → byte-deterministic for a fixed feedback-log. (Kept the literal ordered-ascending-by-`T<PP>.<TT>` token so the existing PASS assert at test line 589 stays green.) |
| C6-03 | IMPORTANT | Same paragraph defines `Observed count` = number of feedback-log rows for that `(Task ID, Override Tier)` pair (1 for a single row; aggregates repeated/appended feedback). |
| C6-04 | IMPORTANT | New **Malformed / empty / partial handling** paragraph: rows missing `Task ID` or `Override Tier` are ignored (cannot match); malformed/empty/partial log yields fewer matches; <2 matching overrides ⇒ whole section omitted, no error (same fail-soft posture as absent-file). |
| C6-05 | MINOR | Stage-attribution fixed: "emitted at Stage 4" → "**rendered at index assembly (Stage 4/5), after scored tiers are computed**". Added explicit fence-holds clause: the scored-tier COMPUTE never reads the feedback-log; only the advisory RENDER reads it (read-only, never writes scored tiers). §5.3 fence preserved. |

### Index-template mirror (`templates/index-template.md` ~:132-138)

Mirrored the reconciled semantics (abbreviated, consistent): added a Match bullet (`Task ID` == `T<PP>.<TT>`; suggested tier ← `Override Tier`; one row per `(Task ID, Override Tier)` pair; `Observed count` = rows for that pair) and updated the ordering bullet to ordered-ascending-by-`T<PP>.<TT>`-then-`Override Tier`.

---

## Test hardening (C6-06 .. C6-08) — `tests/tasklist/test_tasklist_cli.py` `TestP5TierCalibrationAdvisory`

| ID | Severity | Test added | Asserts (byte-matched to post-fix source) |
|----|----------|------------|-------------------------------------------|
| C6-06 | IMPORTANT | `test_p5_advisory_same_inputs_byte_identical` | `same inputs → byte-identical section`; the `Task ID`/`Override Tier` match clauses; per-`(Task ID, Override Tier)` row; `Observed count` semantics. |
| C6-07 | IMPORTANT | `test_p5_advisory_first_run_omission` | `best-effort and READ-ONLY`; `when absent, the whole section is omitted, no error`; plus C6-04 malformed-handling phrasing (`Rows missing Task ID or Override Tier are ignored`, `yields fewer matches`). |
| C6-08 | MINOR | `test_p5_advisory_index_template_mirror` (uses existing `index_template_text` fixture) | `## Tier Calibration Advisory` present in the template; mirror match/order phrasing. |

---

## Non-regression confirmation

- spec.md:344-350 table — byte-identical, untouched (table-conformance lens PASSed; not in edit scope).
- Non-mutation / advisory-only property — intact: `MUST NOT mutate` (1), `NEVER auto-applies` retained.
- §5.3 pure-function fence — intact: `scored tiers are a **pure function of the roadmap text**` (1), `NO calibration/feedback input` (1), `MUST NOT read feedback-log.md` retained, `same roadmap → same scored tiers` (2).
- Existing PASS asserts (`## Tier Calibration Advisory`, ordered-ascending-by-`T<PP>.<TT>`, exact table-columns line, `Pure-function invariant (P5 fence)`) — all still green.

---

## Sync / verify / test status

| Step | Command | Result |
|------|---------|--------|
| sync-dev | `make sync-dev` | OK (29 skills / 42 agents / 44 commands / 12 hooks / 15 templates) |
| verify-sync | `make verify-sync` | All components in sync |
| pytest | `uv run pytest tests/tasklist/ -v` | **95 passed in 0.24s** (all 5 P5 advisory tests green: 2 existing + 3 new C6-06..C6-08) |

## Verdict: PASS — all 8 findings resolved, no regression, mirror in sync.
