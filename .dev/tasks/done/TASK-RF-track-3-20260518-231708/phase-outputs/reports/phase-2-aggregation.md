# Phase 2 Aggregation — rf-qa Input Manifest

**Task:** TASK-RF-track-3-20260518-231708 (FU-003 — PRD CLI default output)
**Gate:** PG-2 `task-integrity`
**Aggregated:** 2026-05-19T02:04:30Z

This file is the L6 aggregation handoff for the rf-qa structural review. It lists the four Phase 2 deliverables, the baseline-vs-current diff sources, and the success criteria extracted from each Phase 2 item's `ensuring …` clause. The reviewer should use `git diff HEAD --` (changes are uncommitted) to inspect each artifact against its pre-patch baseline.

---

## Deliverable 1 — Patched `src/superclaude/cli/prd/config.py` (lines 95-115)

- **Source-fix file:** `src/superclaude/cli/prd/config.py`
- **Baseline reference:** `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/discovery/config-baseline.md`
- **Diff command:** `git diff HEAD -- src/superclaude/cli/prd/config.py`
- **Originating item:** Phase 2 Step 2.1
- **Success criteria (from `ensuring` clause):**
  (a) the `if output:` branch literally preserves the previous `Path(output).resolve()` semantics;
  (b) the new sandbox branch checks `sandbox.parent.exists()` (i.e. `.dev/` must exist before routing);
  (c) the indentation matches the surrounding function (4 spaces per existing style at line 100);
  (d) the explanatory comment ("Default sandbox: .dev/eval-workspaces/ …") is preserved verbatim;
  (e) no other lines in `config.py` are modified;
  (f) lines 107-108 (`task_dir_name` + `task_dir`) remain unchanged.

---

## Deliverable 2 — New `tests/cli/prd/test_config.py`

- **New file:** `tests/cli/prd/test_config.py`
- **Baseline reference:** N/A (file did not exist pre-patch). Reviewer should confirm the file is new via `git status` and `git diff HEAD --` showing it as added.
- **Diff command:** `git diff HEAD -- tests/cli/prd/test_config.py`
- **Originating item:** Phase 2 Step 2.3 (test creation) and Step 2.4 (test run)
- **Success criteria (from `ensuring` clause):**
  (i) imports `resolve_config` from `superclaude.cli.prd.config`;
  (ii) uses pytest's built-in `tmp_path` and `monkeypatch` fixtures;
  (iii) `monkeypatch.chdir(tmp_path)` and creates a `.dev/` directory under `tmp_path`;
  (iv) calls `resolve_config(request="make a PRD", product="test product")` with minimal required args;
  (v) asserts `cfg.task_dir == tmp_path / ".dev" / "eval-workspaces" / "prd-test-product"`;
  (vi) asserts `"prd-test-product"` is NOT in `{p.name for p in tmp_path.iterdir()}` (no stray repo-root dir);
  (vii) includes a module docstring referencing `FU-003 / TASK-RF-track-3-20260518-231708`;
  (viii) the test PASSES when run via `uv run pytest tests/cli/prd/test_config.py -v` (Step 2.4 captured output in `phase-outputs/test-results/regression-test-run.txt` confirms `1 passed`).

---

## Deliverable 3 — Extended `src/superclaude/hooks/scripts/reject-workspace-writes.sh`

- **Source-of-truth file:** `src/superclaude/hooks/scripts/reject-workspace-writes.sh`
- **Baseline reference:** `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/discovery/hook-baseline.md`
- **Diff command:** `git diff HEAD -- src/superclaude/hooks/scripts/reject-workspace-writes.sh`
- **Originating item:** Phase 2 Step 2.5 (Option A defense-in-depth branch)
- **Success criteria (from `ensuring` clause):**
  (i) the existing `.claude/skills/([^/]+)-workspace/(.*)$` branch and its heredoc message are NOT modified;
  (ii) the new branch is anchored at `^(prd-[^/]+)/` so it cannot match `docs/prd-foo/` or `.dev/eval-workspaces/prd-foo/` (only repo-root segments after stripping `CLAUDE_PROJECT_DIR`);
  (iii) shebang `#!/usr/bin/env bash` and `set -u` are preserved;
  (iv) the script still ends with `exit 0` for the no-match case;
  (v) the new branch emits a stderr block naming the bad dir, pointing to `.dev/eval-workspaces/`, and citing `src/superclaude/cli/prd/config.py` (FU-003) + `CLAUDE.md` "Plugin Override";
  (vi) on match the new branch `exit 2`.

---

## Deliverable 4 — Synced mirror `.claude/hooks/reject-workspace-writes.sh`

- **Mirror file:** `.claude/hooks/reject-workspace-writes.sh`
- **Source comparison:** `src/superclaude/hooks/scripts/reject-workspace-writes.sh` (Deliverable 3)
- **Verification command:** `diff src/superclaude/hooks/scripts/reject-workspace-writes.sh .claude/hooks/reject-workspace-writes.sh` (must produce zero diff)
- **Originating item:** Phase 2 Step 2.6 (`make sync-dev`)
- **Success criteria (from `ensuring` clause):**
  - `make sync-dev` exits 0 (captured: `phase-outputs/test-results/sync-dev-output.txt` exit 0, no `error:` lines);
  - `.claude/hooks/reject-workspace-writes.sh` matches `src/superclaude/hooks/scripts/reject-workspace-writes.sh` byte-for-byte (verified post-sync via direct diff returning empty / `FILES_MATCH`).
  - NOTE: Phase 2 Findings entry for Step 2.6 documents that the Makefile's per-file echo behaviour referenced in the original task item was refactored to summary output; the underlying mirror-correctness goal is satisfied and verified by direct diff. Reviewer should treat the `diff` result as the load-bearing evidence, not the absence of a per-file echo in the Make log.

---

## Cross-cutting verification expected from rf-qa

The reviewer should additionally confirm:

- `config.py:100` no longer contains the unconditional `Path(".").resolve()` default (i.e. the ternary was replaced by the `if output: … else: …` block).
- The patched `config.py` still passes ruff (already confirmed in Step 2.2 — `phase-outputs/test-results/ruff-prd-after-patch.txt` exit 0).
- The new regression test passes (already confirmed in Step 2.4 — `phase-outputs/test-results/regression-test-run.txt` exit 0).
- No `_FRESHNESS_SCRIPTS`, `hooks.json`, or `.claude/settings.json` edits were made (Option A zero-registration-delta property). Reviewer can confirm via `git status` showing only the four files above as modified/added.

## Files for rf-qa to read

| Verdict input | Path |
|---|---|
| Aggregation manifest | this file |
| Source-fix baseline | `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/discovery/config-baseline.md` |
| Hook baseline | `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/discovery/hook-baseline.md` |
| Ruff capture | `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/test-results/ruff-prd-after-patch.txt` |
| Regression test capture | `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/test-results/regression-test-run.txt` |
| sync-dev capture | `.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/test-results/sync-dev-output.txt` |
| Modified source 1 | `src/superclaude/cli/prd/config.py` |
| Modified source 2 | `tests/cli/prd/test_config.py` |
| Modified source 3 | `src/superclaude/hooks/scripts/reject-workspace-writes.sh` |
| Modified source 4 (mirror) | `.claude/hooks/reject-workspace-writes.sh` |

## Verdict output path

`.dev/tasks/to-do/TASK-RF-track-3-20260518-231708/phase-outputs/reviews/phase-2-qa-review.md`
