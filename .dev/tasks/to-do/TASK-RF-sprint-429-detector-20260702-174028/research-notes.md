# Research Notes: Sprint 429 Detector Hardening

**Date:** 2026-07-02
**Scenario:** A (explicit — driven by a complete adversarial-merged design spec)
**Depth Tier:** Quick (spec eliminates discovery; <5 modified files, single concern)
**Track Count:** 1
**Spec:** .dev/brainstorms/20260702-165220-sprint-429-detector-hardening/merged-requirements.md

---

## EXISTING_FILES

**Modified (small surface):**
- `src/superclaude/cli/sprint/monitor.py` — `_provider_failure_from_text` (lines ~291-345); entry
  predicate at `:323` (`if is_error and api_error_status == 429:`); `_RE_ALL_ACCOUNT` regex at
  `:41-43`; `429-with-neither-body → SINGLE_ACCOUNT_LIMIT` default at `:332-333`; operation-timeout
  branch at `:335-338`. THE two hunks land here.
- `tests/sprint/test_monitor.py` — existing `detect_provider_failure` assertions over the 6 fixtures;
  the shared-inner parity assert at `:339-343`. New contract-table + parity tests land here.
- `tests/sprint/fixtures/exhaustion/` — 6 existing Shape-1 fixtures (all_account_cooldown,
  single_account_429, api_retry_maxed, operation_timeout, clean_pass, task_failure_real). 3 new
  fixtures added here.

**Read-only reference (MUST stay untouched — confirm the spec's claims hold):**
- `src/superclaude/cli/sprint/rerun_tasks.py` — offline `_classify_transcript` at `:552`, calls the
  shared `_provider_failure_from_text` at `:592`; maps a 429 signal to `FAIL_PROVIDER_EXHAUSTED`.
- `src/superclaude/cli/sprint/recovery_policy.py` — `SessionResetPolicy.decide` (`:76-96`) truth table.
- `src/superclaude/cli/sprint/executor.py` — consumer call sites `:1085` (K>1) and `:2283` (K=1).
- `src/superclaude/cli/sprint/models.py` — `TaskStatus.FAIL_PROVIDER_EXHAUSTED` (`:53`, is_failure `:66`);
  `resume_command` (`:880`).
- `src/superclaude/cli/sprint/aienv.py` — `suggest_alternate_model` (`:81`).
- `tests/sprint/test_recovery_policy.py` — the decide() truth table (MUST NOT be duplicated in the
  detector suite; C3 applies to tests).
- Ground truth: `.dev/troubleshoot/429-signature-ground-truth.md` (Shape 1); the July raw logs
  (Shape 2) captured in the spec §3.

## PATTERNS_AND_CONVENTIONS

- UV-only (`uv run pytest`); source-of-truth is `src/superclaude/` (no `.claude/` edits — but this
  task touches `cli/` + `tests/` only, no skills/agents/commands, so no sync-dev involved).
- Fixtures are NDJSON `.jsonl`; detection keys on the LAST `{"type":"result"}` line.
- Existing tests use `detect_provider_failure(_FIXTURES / "<name>.jsonl")` and assert `.kind` /
  `.resolved_model`; a parametrized table is the natural extension.
- `ruff check` (make lint) + `ruff format --check src/ tests/` (CI) + `make verify-sync` gate the PR.

## GAPS_AND_QUESTIONS

- OQ2: no verbatim Shape-2 SINGLE-account transcript exists → the spec ships a clearly-named
  `_SYNTHESIZED` breakpoint fixture. Researchers confirm the assumed phrasing against ground truth.
- Confirm the exact current expression text at `monitor.py:323` and `:41-43` so the builder writes a
  precise, surgical Edit (freshness check — the spec was authored this session; nothing changed
  monitor.py, but verify).

## RECOMMENDED_OUTPUTS

- `research/01-detector-change-surface.md` — exact monitor.py expressions to change + read-only
  consumer/offline-mirror confirmation.
- `research/02-test-and-fixture-conventions.md` — test_monitor.py structure, fixture format, the
  verbatim Shape-2 result line, how to add a parametrized contract table + `_classify_transcript`
  parity, and how the existing 6 fixtures are asserted.
- `research/03-template-examples.md` — MDTM template 02 PART 1 rules (A3/B2/M3/M4/I19, Execution
  Context, POST reflect wrapper item) + a prior TASK-RF example for structure.

## SUGGESTED_PHASES

- R1 (File Inventory / change-surface): monitor.py exact expressions + read-only chain confirmation.
  Other researchers cover tests (R2) and template (R3).
- R2 (Test & Verification): test_monitor.py + fixtures + Shape-2 verbatim line + contract-table +
  parity design. Other researchers cover the source change (R1) and template (R3).
- R3 (Template & Examples): MDTM 02 rules + prior TASK-RF example. Other researchers cover source (R1)
  and tests (R2).

## TEMPLATE_NOTES

Template 02 (complex: implement → fixtures → tests → regression/lint/verify + QA gate). Quick tier
(confirmatory research only — the spec is the design). QA gate: FINAL_ONLY is sufficient (narrow,
single-file production change); the generated task's final QA gate must still meet the 6-agent floor.

## AMBIGUITIES_FOR_USER

None blocking — intent is fully specified by the merged-requirements spec (R1-R7, SC1-SC6, AC1-AC6,
the ~12-row contract table, and the 9-item "CHANGES NOT MAKING" ledger). OQ2 (Shape-2 single-account)
is handled deterministically by the synthesized-breakpoint-fixture decision already made in the spec.
