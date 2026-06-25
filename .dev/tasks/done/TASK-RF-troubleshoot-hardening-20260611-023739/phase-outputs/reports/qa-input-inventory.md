# QA Input Inventory (Step 8.1)

Consolidated inventory of every deliverable for the FINAL_ONLY QA gate (Steps 8.2–8.8).
All 7 lens agents review this same enumerated set. Paths are repo-relative to
`/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening`. All deliverables
confirmed present on disk (no missing items).

## New refs (6 — CREATE, net-new)

| Path | Lines | Contents |
|------|-------|----------|
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/pipeline-hardening-closure.md` | 63 | Mode skeleton: trigger (topology, no flag), H0 applicability gate (FR-1) + 6-field boundary-scan schema (9-value boundary_type enum), H0 mechanism statement (FR-2), H5 off-path-reviewer rule + waiver standard (FR-11); 4-token verdict; wave sequence. |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md` | 71 | THE advisory ref: §5.5 11-field schema, §5.4 7-row verdict truth table (rows 5/6 = advisory), H5 decision-to-status mapping (4 rows), backtest-status-vs-verdict (3 rows), downstream no-override + `success_with_hardening_*`, one-way waiver latch + FR-12 anti-inflation. |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/runtime-entrypoint-verification.md` | 47 | H1 (FR-3 FAIL rule, §5.6 card [10 rows / 12 field tokens], FR-4 negative+positive witness, forbidden-interpretation examples, 4 substitute-witness classes w/ OI-3 deferral). |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md` | 30 | H2 (§5.6 6-field ledger w/ OI-2 open-enum deferral, FR-5 empty-ledger/unclassified/generic-proof FAIL, FR-6 sibling sweep). |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/unmask-and-sweep.md` | 52 | H3 (§5.7 4-rule allow-list grammar, FR-8 word-boundary + 5 near-miss negatives, FR-7 4 required controls, FR-9 unmask-sweep + K_true/K_swept, §5.6 10-field card). |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/effective-input-proof.md` | 27 | H4 (FR-10 fail-closed incl. wrong-surface / `|E ∩ true_runtime_surface|` proof / F-D1, §5.6 8-field manifest). |

## Modified files (4 — MODIFY, additive)

| Path | Lines | Change |
|------|-------|--------|
| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` | 587 | Wave 4.5 trigger (after Wave 1.7, before Wave 5) + 11 additive Output Contract fields + Wave 5 report bullet + Wave-Structure overview + Refs index rows. |
| `src/superclaude/commands/troubleshoot.md` | 202 | One advertise sentence (Behavioral Summary step 4) + one Boundaries→Will line; NO new CLI flag (NFR-5). |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` | 305 | In-template `## Pipeline Hardening Closure` section (4-token verdict + NOT PROVEN/ADVISORY blockers) + post-template `## Pipeline Hardening Closure rule`. |
| `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md` | 139 | BUILD_REQUEST carries verdict+waiver_status; user-offer surfaces verdict; `## Pipeline hardening verdict gating` reconciles §5.4 no-override (+4 MD040 fences fixed). |

## Test suite (`tests/troubleshoot/` — net-new)

| Path | Lines | Contents |
|------|-------|----------|
| `tests/troubleshoot/__init__.py` | 4 | Package marker + convention note. |
| `tests/troubleshoot/test_hardening_h0.py` | 54 | 2 unit (FR-1 / §5.6 H0 boundary scan). |
| `tests/troubleshoot/test_hardening_h1.py` | 46 | 1 unit (FR-3/FR-4 / §5.6 H1 card, neg+pos witness). |
| `tests/troubleshoot/test_hardening_h2.py` | 44 | 2 unit (FR-5 empty-ledger; FR-6 sibling sweep — NEW G-PRE-1). |
| `tests/troubleshoot/test_hardening_h3.py` | 55 | 3 unit (FR-8 word-boundary; §5.7 grammar; FR-9 sweep card). |
| `tests/troubleshoot/test_hardening_h4.py` | 44 | 2 unit (FR-10 wrong-surface; §5.6 manifest intersection_proof). |
| `tests/troubleshoot/test_hardening_verdict.py` | 94 | 3 unit (waiver latch, H5 mapping, anti-inflation) + 2 integration (7-row aggregation incl. advisory 5/6; downstream no-re-green FR-12↔NFR-4). |
| `tests/troubleshoot/test_hardening_output_contract.py` | 96 | 3 integration (backward-compat NFR-6; backtest advisory-until-complete NFR-1; report NOT PROVEN closure FR-13 AC3). |
| `tests/troubleshoot/e2e-backtest-scenarios.md` | 50 | 6 documented E2E backtests (E1–E5 + Waiver re-green); not pytest-collected (M5). |

## Totals

- 6 new refs + 4 modified files + 9 test-dir files (= 7 test modules + `__init__.py` + e2e scenarios) = **20 deliverables, all present.**
- Test functions: **13 unit + 5 integration = 18** (pytest 18/18 PASS) + 6 documented E2E scenarios.
- All 9 src skill markdown files markdownlint-clean; `make sync-dev` + `make verify-sync` clean.
