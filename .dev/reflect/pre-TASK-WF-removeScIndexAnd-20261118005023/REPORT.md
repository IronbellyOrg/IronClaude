```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 1
confidence_calibrated: 0.85
citations_total: 9
citations_revalidated: 9
citations_dropped: 0
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

# Reflect (pre-execution) report: remove /sc:index and /sc:index-repo

**Verdict: the plan is sound; no blocking finding. Status is `partial` for three stated reasons, none of them a defect in the plan.**

- Spec: `.dev/tasks/to-do/TASK-WF-removeScIndexAnd-20261118-004719/source.md` (one inline prompt). Plan: `.dev/tasks/to-do/TASK-WF-removeScIndexAnd-20261118-004719/TASK-WF-removeScIndexAnd-20261118-004719.md` (4 phases, 13 tasks).
- **WARN, coverage_degraded `parsed-sparse`:** the spec has no labeled requirement ids (0 parsed rows, 9 inferred rows), so the Tier 1 stop is forbidden and the guard routes to Tier 2. The caller pinned `--depth quick`, which overrides it (section 5.1). Tier 2 was not run: the standing session rule bars subagents and extra paid model calls.
- **Inline fallbacks, so status is forced `partial`:** the confidence-calibrator and evidence-validator agents were not used (same rule). Calibration was done inline (`calibration: inline-fallback`); every cited line below was re-read from disk by the orchestrator, and every INF quote was matched verbatim against `source.md:1`. 0 citations dropped.
- Grounded checks that came out clean: the plan's counts match the files. `WORKER-CONTRACT.md:329` says "15 commands converted in P1" and `:334` says "12 commands that are ready with brief constraints" (`.../core/WORKER-CONTRACT.md`, re-read 2026-11-18); `tests/skills/test_worker_contract.py:1400` asserts 15 and `:1606` asserts 27 (so 13 and 25 are the right new values); `tests/recommend/test_routing_refresh.py:39` is the `_POST_REFRESH_REMOVALS` set Task 10 extends; `tests/unit/test_cli_install.py:525` is the `index-repo` assertion Task 13 replaces; `src/superclaude/core/HOW-WE-WORK.md:193` is the row Task 2 deletes and `WORKER-CONTRACT.md:345` the table row Task 4 deletes; `tests/core/test_how_we_work_routing_table.py:1012` is the docstring naming S24 that Task 9 updates. All 22 tracked non-historical files that name the commands are covered by a task (6 deleted in Task 1, 16 edited in Tasks 2 to 13).
- [INFERRED] The three Python test files edited in Tasks 9 to 13 may need `ruff format` after the edits (the plan's acceptance lines for those tasks run pytest only).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote (`source.md:1`) | Citation | Match result |
|---|---|---|---|
| INF-001 | "Remove /sc:index and /sc:index-repo per .dev/cleanup/index/dependency-map.md" | source.md:1 | mapped: Task 1 (and the Constraints) |
| INF-002 | "gone from commands, mirrors" | source.md:1 | mapped: Task 1 |
| INF-003 | "docs, routing guide" | source.md:1 | mapped: Tasks 6, 7, 8 (docs); Tasks 2, 3 (routing guide) |
| INF-004 | "routing guide, worker contract" | source.md:1 | mapped: Task 4 (worker contract) |
| INF-005 | "worker contract and routing tests" | source.md:1 | mapped: Tasks 9, 10, 12 (routing tests) |
| INF-006 | "the routing table checks pass" | source.md:1 | mapped: Task 9 and Task 10 acceptance criteria |
| INF-007 | "no file outside the historical records names them" | source.md:1 | unmapped as a whole: each task greps its own area, no task owns the repo-wide sweep (executor-owned by workflow rule) |
| INF-008 | "0 new test failures and the pass count drops only by the removed tests" | source.md:1 | unmapped: executor-owned full-suite check (only Task 11 states a case-count drop) |
| INF-009 | "lint, format, verify-sync and git diff --check stay green" | source.md:1 | unmapped: partly covered (Task 1 verify-sync, Task 6 git diff --check); lint and format not named |

No INF row was dropped by the validator. Postscript: none.

## Coverage matrix

- `coverage_pct` (parsed rows only): null (0 parsed rows). `coverage_undefined`: false (Pass 2 emitted valid rows).
- `coverage_pct_union`: 6 / 9 = **0.67**. `unmapped_requirements_union`: INF-007, INF-008, INF-009. `S_dev_density` (union): 0.33.
- Why this is not blocking: INF-007 to INF-009 are the plan's whole-run acceptance checks. The plan's Goal states all three in full, and the workflow rules put final whole-plan verification with the executor (no verification-only task). They are named here so nobody mistakes the per-task greps for the repo-wide sweep.
- Domains touched: user docs, tests, shipped guide and contract text (3). Tasks: 13. Dependent order is correct: Task 8 after Task 4, Task 9 and Task 10 after Task 2, Task 12 after Task 4, no task depends on a higher number.

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 9` = 0.11. No WARN (fewer than 21 citations).

## Recommendations

### Recommendation R-001: Run the repo-wide leftover sweep as the last step

- **File:** n/a (whole repository, excluding `.dev/`, `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, `CHANGELOG.md`)
- **Change:** After Task 13, run the sweep for INF-007 and expect only the frozen records: the `commands` entries and `S24` text in `tests/recommend/fixtures/routing_refresh_cases.json` and the `formatting_only` list entry `"index-repo"` in `tests/recommend/test_routing_refresh.py`.
- **Verifier:** `git grep -nE 'sc:index|sc-index|index-repo|index_repo|sc:sc:index' -- . ':!.dev' ':!docs/releases' ':!docs/testing/v5.0.0' ':!docs/designs' ':!CHANGELOG.md'` prints only those frozen-record lines.
- **Linked deviation(s):** none (covers INF-007)
- **Priority:** P1

### Recommendation R-002: Run the full regression gate after the last task

- **File:** n/a
- **Change:** Compare the full suite, `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync` and `git diff --check` against the saved baseline (26703 passed, 178 skipped, 0 failed; all checks green), and run `uv run ruff format` on the edited test files if the format check fails.
- **Verifier:** same commands as `.dev/issues/v6-index/baseline.md`; 0 new failures and the pass count drops only by the deleted test cases (covers INF-008 and INF-009).
- **Linked deviation(s):** none
- **Priority:** P1
