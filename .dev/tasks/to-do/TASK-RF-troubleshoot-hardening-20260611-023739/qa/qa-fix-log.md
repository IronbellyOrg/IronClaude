# QA Fix Log (Step 8.10)

Fixes applied by the executor (subagent `src/` writes are intercepted in this environment;
the executor applies fixes directly, consistent with all prior phase gates). Only the two
in-scope actionable findings (C-1, C-2) were fixed; C-3/C-4/C-5 require no change (see
`qa-consolidated-findings.md` dispositions).

## C-1 — MD040 bare fences in `commands/troubleshoot.md` [MINOR, FIXED]

- **File:** `src/superclaude/skills/...` → `src/superclaude/commands/troubleshoot.md`
- **Change:** Tagged the 5 bare ` ``` ` openers in the `## Examples` section as ` ```text ` (the 5 `/sc:troubleshoot ...` example blocks). Content-preserving; same convention as the Phase-6 `remediation-handoff.md` fence fix.
- **Verification:** `npx markdownlint-cli@0.38.0 src/superclaude/commands/troubleshoot.md` → exit 0 (was exit 1 with 5 MD040). `make sync-dev` re-run → exit 0 (`.claude/` mirror current).

## C-2 — H1 card "11-field" label harmonized [IMPORTANT, FIXED]

- **Files:** `tests/troubleshoot/test_hardening_h1.py` (docstring L17 + comment L21); `phase-outputs/reports/qa-input-inventory.md` (L14).
- **Change:** Replaced the contested "11-field" label with the ref's actual structure — "the H1 card (10 §5.6 rows / 12 atomic field tokens)". The shipped ref `runtime-entrypoint-verification.md` was already correct (verbatim 10-row §5.6 table, no missing field — confirmed by lens 8.2); the 12-token assertion loop is correct and was left UNCHANGED so the suite stays green. Pure label/comment harmonization.
- **Verification:** `uv run pytest tests/troubleshoot/ -q` → 18 passed (loop unchanged, suite green).

## Not fixed (dispositioned, no change required)

- **C-3** — stale internal counts in `research/08-...md` ("17" vs 18): frozen prior-stage INPUT, not a deliverable; the shipped deliverables are correct. Modifying a frozen research input mid-execution is out of scope and would corrupt provenance. Documented.
- **C-4** — tests are content-assertion markers, not behavioral gates: BY DESIGN (spec §4.7; `tests/skills/` pattern; behavioral replay deferred to M5/NFR-1). Already disclosed in `pytest-summary.md` + `e2e-backtest-scenarios.md`.
- **C-5** — FR-4 `forbidden_interpretation` "yes when applicable": spec-faithful (reproduces §5.6 / FR-4 verbatim); tightening would deviate from the spec.

## Advisory invariant

Re-confirmed intact after all fixes: none of the touched files (`troubleshoot.md`, `test_hardening_h1.py`, `qa-input-inventory.md`) touches the `pipeline_hardening_verdict` enum. The 4-token `pass | blocked | advisory | not_applicable` and §5.4 rows 5/6 are unchanged (lens 8.8 PASS). pytest 18/18 incl. `test_verdict_aggregation_from_h_statuses` (both advisory rows).
