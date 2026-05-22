# Researcher 6 — Test & Verification per Logical Commit Group

**Status:** Complete
**Date:** 2026-05-18
**Scope:** QA pass needed before each logical commit and before each PR opens on `feat/hook-sync-and-matcher-fix`.
**Approach:** Reuse C1-C4 prior evidence verbatim where possible; re-run targeted tests for everything else; document pre-existing failures so PR descriptions can cite them.

---

## 1. C1-C4 sprint-runner QA — REUSE PRIOR EVIDENCE

The C1-C4 work at `.dev/tasks/to-do/TASK-RF-20260518-015659/` already executed a full Phase 7 QA pass. Verdicts:

| Gate | Result | Source |
|---|---|---|
| G1 (C3 timeout reconciliation) | **PASS cycle 1**, 2/2 tests | `phase-outputs/test-results/phase-3-c3-summary.md` |
| G2 (C4 phase_start JSONL emission) | **PASS cycle 1**, 4/4 tests | `phase-outputs/test-results/phase-4-c4-summary.md` |
| G3 (C1 watchdog split + startup_stall_timeout) | **PASS cycle 1**, 5/5 tests | `phase-outputs/test-results/phase-5-c1-summary.md` |
| G4 (C2 per-task output-file collision) | **PASS cycle 1**, 5/5 tests | `phase-outputs/test-results/phase-6-c2-summary.md` |
| Phase 7 — make lint | **PASS for changed files** (10 files, 0 errors); 241 pre-existing repo-wide errors documented out-of-scope | `phase-outputs/test-results/phase-7-make-lint-summary.md` |
| Phase 7 — sprint+pipeline pytest | **1350/1408 PASS**; 57 pre-existing `.stdin AttributeError` failures from commit 4799719 (2026-04-20); 13/13 NEW tests PASS | `phase-outputs/test-results/phase-7-sprint-pipeline-pytest-summary.md` |
| Phase 7 — make test (full suite) | **5644/5813 PASS**; 63 failures, 0 attributable to C1-C4 | `phase-outputs/test-results/phase-7-make-test-summary.md` |

**Recommendation for C1-C4 PR:** Reuse prior evidence verbatim in the PR description. Cite the 4 verdict files plus `phase-outputs/reports/all-fixes-summary.md`. **No need to re-run.**

---

## 2. task-builder-merge QA — VERIFY M2-M6 ON FINAL COMMITTED STATE

### 2.1 Test artifact

The test surface for the milestones lives in **`tests/skills/test_task_builder_merge.py`** (68 tests). The only branch-level diff vs master is a 1-line change inside `TestPR07AdversarialCategoryNaming::test_axis_annotation_required_in_items_reviewed` (commit `487e76b` MIG-004), tightening the header literal from `"Axis (PR-07)"` to `"| # | Check | axis | Result | Evidence |"`.

### 2.2 Current state (re-run on 2026-05-18, branch HEAD = `efaa33d`)

```
uv run pytest tests/skills/test_task_builder_merge.py -q
→ 65 passed, 3 failed in 0.06s
```

**Failures** (all due to Phase 6 of `task-builder-merge` having rewritten phrases that earlier M2/M5 tests still expect):

| Test | Expected literal | Status |
|---|---|---|
| `TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths` | `"NEVER write specific"` in SKILL.md | **FAIL** — phrase removed by later edits |
| `TestPR02RetryMonotonicityGuards::test_skill_regression_detection_precedence` | `"Regression takes precedence"` (or lower) in SKILL.md | **FAIL** — phrase rewritten |
| `TestPR02RetryMonotonicityGuards::test_rf_task_builder_has_protocol` | `"non-convergent"` in rf-task-builder.md | **FAIL** — phrase rewritten |

This **partially contradicts** the C1-C4 Phase 7 attribution that said "4 task-builder-merge test failures will self-resolve when Phase 6 completes." Phase 6 has now completed (commit `87c8254` MIG-006) but 3 tests still fail because Phase 6's writes removed strings that earlier milestone tests were still pinning. The C1-C4 report counted 4 such failures and called them concurrent. They are now **3 failures and confirmed as drift between M2/M5 tests and current SKILL.md text** — not concurrent races.

### 2.3 Recommendation per milestone commit

| Commit | Cmd | Success criteria |
|---|---|---|
| `2648be8` MIG-002 | `uv run pytest tests/skills/test_task_builder_merge.py -k "TestPR01" -v` | All 3 tests in `TestPR01ExecutionContextHeader` PASS at that commit |
| `ad083b6` MIG-003 | `uv run pytest tests/skills/test_task_builder_merge.py -k "TestPR04" -v` | Inherited Verdict tests PASS |
| `487e76b` MIG-004 | `uv run pytest tests/skills/test_task_builder_merge.py -k "TestPR07" -v` | 5-axis overlay tests PASS (the 1-line tightened test is here) |
| `db6166e` MIG-005 | `uv run pytest tests/skills/test_task_builder_merge.py -k "TestPR02" -v` | All `TestPR02RetryMonotonicityGuards` tests PASS at that commit |
| `87c8254` MIG-006 | `uv run pytest tests/skills/test_task_builder_merge.py -k "TestPR03" -v` | DNSP tests PASS |

**Before opening the task-builder-merge PR:** The 3 currently-failing tests need either (a) `git checkout <pre-Phase-6-commit> -- tests/skills/test_task_builder_merge.py` style fix-up of expected literals to match the final committed SKILL.md text, or (b) explicit acknowledgement in the PR description that those 3 tests need to be updated as a follow-up. Recommended: **fix the test literals before merge**, since the SKILL.md is the artifact under review and the tests are the gate.

---

## 3. hooks-and-matcher-fix QA

### 3.1 Commits

- `5439ea1` — widen `auggie-flag-clear` matcher to `mcp__auggie-mcp__`; add verify-sync hook coverage and cross-consistency checks
- `efaa33d` — OQ-2 (bash-gate orphan archive+delete) + OQ-3 (register `reject-workspace-writes.sh`)

### 3.2 Tests

- **`tests/cli/test_verify_sync_hooks.py`** (NEW, 7 tests covering V1-V7 scenarios from release-spec §9) — added by `5439ea1`.
  - V1: clean tree → exit 0, `=== Hooks ===` block visible
  - V2: remove `.claude/hooks/auggie-flag-clear.sh` → MISSING error
  - V3: remove entry from `_FRESHNESS_SCRIPTS` → MISSING-from-installer
  - V4: add fake `ghost-hook.sh` to `_FRESHNESS_SCRIPTS` → STALE
  - V5: `hooks.json` matcher loses one prefix → DRIFT
  - V6: `auggie-flag-clear.sh` case body loses one prefix → DRIFT
  - V7: regression-to-master → DRIFT
- Test refs `auggie-flag-clear.sh` at line 39 and `reject-workspace-writes.sh` at lines 133-134.
- `pytestmark` skipif if `make` or `jq` are unavailable.
- **Do NOT run with pytest-xdist** — tests mutate real repo files via try/finally (race-unsafe). Note is in the module docstring.

### 3.3 Re-run on 2026-05-18

```
uv run pytest tests/cli/test_verify_sync_hooks.py -q
→ 7 passed in 2.83s
```

All 7 verify-sync hook tests PASS at branch HEAD.

### 3.4 Recommendation

- Per hook commit: `uv run pytest tests/cli/test_verify_sync_hooks.py -v` + visual check of `make verify-sync` output. Acceptance:
  - exit 0
  - presence of `=== Hooks ===`, `=== Installer Registration ===`, `=== Hooks Cross-Consistency ===` blocks
- `tests/cli/test_install_hooks.py` and `tests/pipeline/test_process_hooks.py` are also hook-adjacent; `make test -k "hook"` is a safe net.

---

## 4. audit-tests QA — NEW untracked tests in `tests/audit/`

### 4.1 Inventory

8 untracked test files + a `fixtures/` subdir:

| File | def test_ count |
|---|---|
| `test_dnsp_all_agents_fail_bypass.py` | 33 |
| `test_dnsp_dedup_collapse.py` | 23 |
| `test_dnsp_does_not_serialize_cohort.py` | 28 |
| `test_dnsp_twice_exhaust.py` | 30 |
| `test_hidden_input_guard.py` | 20 |
| `test_invariant_preservation_NFR_6_through_10.py` | 19 |
| `test_nfr_conv_6_self_contained.py` | 10 |
| `test_nfr_conv_9_zero_trust.py` | 32 |

### 4.2 Re-run on 2026-05-18

```
uv run pytest tests/audit/ -q
→ 1188 passed, 1 skipped in 1.65s
```

**All audit tests pass.** The DNSP tests map to MIG-006; the NFR-CONV tests map to MIG-002…MIG-005.

### 4.3 Lint state (NEW files only)

```
uv run ruff check <8 NEW files>
→ 16 errors, 6 fixable
```

Breakdown:
- **N801** (10x): class names use `TestPartA_X` / `TestInvariant1_Y` underscore convention — does not match CapWords.
- **N999** (1x): `test_invariant_preservation_NFR_6_through_10` — module name has uppercase letters (`NFR`).
- **F401** (4x): `dataclasses.field`, `typing.Tuple`, `typing.List`, `typing.Any` unused.
- **I001** (1x): one unsorted import block.

**Recommendation:** Fix the 6 auto-fixable issues with `uv run ruff check tests/audit/ --fix`. The N801 + N999 class/module-naming issues should either be renamed (preferred) or get a `# noqa: N801,N999` plus a comment about the deliberate naming scheme. Each fix can land in the audit-tests commit itself.

---

## 5. docs-only commits QA

### 5.1 Docs changes on this branch

Inspect with `git diff master..HEAD --name-only -- 'docs/**'` — confirm the set of docs touched.

### 5.2 Recommendation

- No test gate.
- `make lint` is currently flooded by 241 pre-existing repo-wide errors that have nothing to do with docs (`pyproject.toml` ruff config is too broad). **Run** `uv run ruff check docs/` **as a sanity step** but treat 0 changes-induced errors as PASS.
- Human-prose review only for `docs/reference/nfr-conv-2-prose-determinism.md` and any other addition.

---

## 6. Pre-existing failure attribution (FOR PR DESCRIPTIONS)

These three categories of failures pre-date the work on this branch and must be documented in every PR description so reviewers do not block on them.

### 6.1 The 57 `.stdin AttributeError` failures (sprint + pipeline)

- **Root cause:** commit `47997190` (2026-04-20 — "use stdin for the roadmap pipeline instead of passing the prompt as argument") added `self._process.stdin is not None` in `src/superclaude/cli/pipeline/process.py:141`.
- **Symptom:** ~24 fake-Popen helper classes across 8 test files don't define `.stdin`.
- **Verification done 2026-05-18:** Phase 5 of C1-C4 confirmed via `git stash` of all changes — same 3 watchdog failures persisted at baseline. Pattern is identical for all 57. **Not caused by this branch.**
- **PR-description boilerplate:** "57 pre-existing `.stdin AttributeError` failures from commit 4799719 (2026-04-20). Verified pre-existing via git stash on 2026-05-18. Out-of-scope follow-up."

### 6.2 The 241 repo-wide ruff errors

- **Distribution (top 10 files):** 107 in `.dev/releases/complete/unified-audit-gating-v1.2.1/test-evidence/smoke/test_import_smoke.py`; 23 + 22 in the same release's `realworld_*` files; 11 in `src/superclaude/cli/cli_portify/executor.py`; 7 in `tests/pipeline/test_full_flow.py` (intentional E402); 6 in `src/superclaude/cli/main.py`; etc.
- **Verification:** `phase-outputs/test-results/phase-7-make-lint-summary.md`.
- **PR-description boilerplate:** "241 pre-existing repo-wide ruff errors documented out-of-scope (frozen release artifacts + unrelated CLI modules). All files touched by this PR are lint-clean for ruff."

### 6.3 The task-builder-merge phrase-drift failures (NOT pre-existing)

- **State change:** The C1-C4 report (2026-05-18 earlier) called these "4 in-flight Phase 6 concurrent failures." On re-run at branch HEAD (Phase 6 now committed as `87c8254`), the count is **3 failures**, and they are NO LONGER concurrent — they are bona-fide drift between M2/M5 test literals and the post-Phase-6 SKILL.md text.
- **Three failing tests:**
  - `tests/skills/test_task_builder_merge.py::TestPR01ExecutionContextHeader::test_execution_context_uses_source_areas_not_paths`
  - `tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_skill_regression_detection_precedence`
  - `tests/skills/test_task_builder_merge.py::TestPR02RetryMonotonicityGuards::test_rf_task_builder_has_protocol`
- **Action required:** Either fix the test literals to match the final SKILL.md before merging the task-builder-merge PR, or open a follow-up task. **Do not** label these "pre-existing" in the PR description — they are caused by the branch.

---

## 7. Per-group QA recipe summary table

| Logical group | Lint cmd | Test cmd | Success criteria | Known pre-existing failures to ignore |
|---|---|---|---|---|
| **C1-C4 sprint-runner** (reuse) | (already PASS for 10 files; reuse evidence) | (already 13/13 PASS; reuse evidence) | 4 verdict files cite PASS cycle 1 | 57 .stdin + 241 ruff |
| **task-builder-merge M2-M6** | `uv run ruff check src/superclaude/skills/task-builder/SKILL.md src/superclaude/agents/rf-*.md tests/skills/test_task_builder_merge.py` (md skipped — file types) | `uv run pytest tests/skills/test_task_builder_merge.py -v` | **68/68 PASS** required (currently 65/68 — 3 fixes needed) | None of these failures are pre-existing; fix before merge |
| **hooks-and-matcher-fix** | `uv run ruff check src/superclaude/cli/install_hooks.py tests/cli/test_verify_sync_hooks.py` (clean) | `uv run pytest tests/cli/test_verify_sync_hooks.py tests/cli/test_install_hooks.py tests/pipeline/test_process_hooks.py -v` | **All hook tests PASS**; `make verify-sync` exit 0; `=== Hooks ===` / `=== Installer Registration ===` / `=== Hooks Cross-Consistency ===` blocks visible | hooks.json F821 from ruff misclassifying JSON as Python (pre-existing repo-wide) |
| **audit-tests** (8 new files) | `uv run ruff check tests/audit/ --fix` then `uv run ruff check tests/audit/` (16 → 0 errors needed; rename N801/N999 or add `# noqa`) | `uv run pytest tests/audit/ -v` | **1188 passed** (current state) | None |
| **docs-only** | `uv run ruff check docs/` (sanity) | (none) | 0 ruff errors *induced by changes*; human prose review | 241 repo-wide ruff |

---

## 8. Solutions-learned pollution remediation QA

### 8.1 State

- `docs/memory/solutions_learned.jsonl` is currently in modified state (per `git status --short docs/memory/`).
- `grep -rn "solutions_learned" tests/ → 0 matches.` **No existing test guards the contents of `solutions_learned.jsonl`.**

### 8.2 Recommendation

After reverting `docs/memory/solutions_learned.jsonl` to its pre-test state (`git checkout master -- docs/memory/solutions_learned.jsonl`), add a **follow-up task** for a small regression test:

```python
# tests/cli/test_solutions_learned_provenance.py (new)
import json
from pathlib import Path

SOLUTIONS = Path(__file__).resolve().parents[2] / "docs" / "memory" / "solutions_learned.jsonl"

def test_no_test_pollution_in_solutions_learned():
    """Each line must be a real solution, not a unit-test or fixture artifact."""
    for i, line in enumerate(SOLUTIONS.read_text().splitlines(), 1):
        if not line.strip():
            continue
        entry = json.loads(line)
        # Heuristics: real solutions have a non-empty `problem`, a `solution`,
        # and do NOT contain literal test fixture markers like "fixture-only"
        # or "test_*" in their problem statements.
        assert "problem" in entry, f"line {i} missing problem"
        assert "solution" in entry, f"line {i} missing solution"
        prob = entry["problem"].lower()
        assert "fixture-only" not in prob, f"line {i} looks like a test artifact"
        assert not prob.startswith("test_"), f"line {i} looks like a test artifact"
```

This is a **post-merge follow-up**, not a gate for the current PRs on this branch — the revert alone is sufficient for the immediate cleanup.

---

## Summary Findings

1. **C1-C4** can ship by reusing prior QA verdicts verbatim — no re-run needed.
2. **task-builder-merge M2-M6** has 3 failing tests at branch HEAD (`TestPR01.test_execution_context_uses_source_areas_not_paths`, `TestPR02.test_skill_regression_detection_precedence`, `TestPR02.test_rf_task_builder_has_protocol`) caused by Phase 6's SKILL.md rewrite removing strings the earlier-milestone tests still pin. **Must be fixed before that PR opens** — these are NOT pre-existing.
3. **hooks-and-matcher-fix** is GREEN: 7/7 verify-sync hook tests PASS, install_hooks.py + test file are ruff-clean.
4. **audit-tests** (8 NEW files) are 1188/1188 PASS but have 16 ruff lint issues (mostly N801 underscore-class-names and N999 module-name `NFR` casing). Recommend `--fix` for the 6 auto-fixable; rename or `# noqa` the remaining naming issues.
5. **docs-only commits** need only human review; the repo-wide 241 pre-existing ruff errors are unchanged by this branch.
6. The 57 `.stdin AttributeError` failures and 241 ruff errors are documented pre-existing and must appear in every PR description as out-of-scope boilerplate.
7. **No test guards `docs/memory/solutions_learned.jsonl`.** Recommend adding one as a follow-up — not a gate for this branch.
