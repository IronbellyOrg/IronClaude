# R5 — Data Flow Tracer (Garbage-Path Root Causes)

**Author**: Researcher 5 of 7
**Date**: 2026-05-18
**Branch**: feat/hook-sync-and-matcher-fix
**Scope**: Trace each uncommitted garbage path to the source-code path that wrote it, so cleanup follow-ups can FIX the source (not just delete the symptom).

---

## 1. `prd-test-product/` and `prd-dry-run-test/` at REPO ROOT

### Symptom
Two stray directories at repo root, each containing only `execution-log.md`:
- `prd-test-product/execution-log.md` — "Started 2026-05-18T01:53:12.790391+00:00, Task Dir: /config/workspace/IronClaude/prd-test-product"
- `prd-dry-run-test/execution-log.md` — "Started 2026-05-18T01:53:12.808707+00:00, Task Dir: /config/workspace/IronClaude/prd-dry-run-test"

Both started within 18ms of each other, suggesting CI/test-script invocation.

### Root cause (file:line)
**`src/superclaude/cli/prd/config.py:100`**:
```python
output_path = Path(output).resolve() if output else Path(".").resolve()
```
- When `--output` flag is **not** supplied, the PRD pipeline defaults `output_path` to **CWD** (`Path(".").resolve()`).
- Then **`src/superclaude/cli/prd/config.py:107-108`**:
  ```python
  task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
  task_dir = output_path / task_dir_name
  ```
- The PRD invocations that produced these dirs were `--product "test product"` (→ slug `test-product`) and `--product "dry run test"` (→ slug `dry-run-test`), both run with CWD = repo root and no `--output`.
- **`src/superclaude/cli/prd/logging_.py:50-63`** creates `execution-log.md` inside `task_dir` even on dry-run / early failure, which is why these dirs exist with *only* the log file (the pipeline aborted before subdirs `research/`, `synthesis/`, `qa/` were populated by `create_task_dirs` at `src/superclaude/cli/prd/inventory.py:193-199`).

### Fix recommendation (source-level)
Two viable options:
1. **Reject CWD-defaulting under repo root** — in `config.py:100`, after resolving `output_path`, refuse if the resolved path equals a known repo root (presence of `pyproject.toml` + `src/superclaude/`). Force `--output` to be explicit, or default to `.dev/prd/` (sanctioned dev sink per CLAUDE.md).
2. **Default to `.dev/prd-runs/` instead of CWD** — least-intrusive: change `Path(".").resolve()` to a sanctioned default like `Path.cwd() / ".dev" / "prd-runs"` so the side-effect is contained.

Either way, ALSO add `prd-*-test/` to `.gitignore` as a belt-and-braces safeguard.

### Follow-up task priority
**P1** — this is a real source-of-pollution bug. Every dry-run / smoke-test of `superclaude prd` from repo root will plant a stray dir. Worth a dedicated `fix/prd-default-output-path` follow-up.

---

## 2. `0.20` empty file at REPO ROOT

### Symptom
Zero-byte file literally named `0.20` at repo root. Created 2026-05-18T15:26:47 (mtime/ctime/birth all identical).

### Root cause investigation
- **NOT** in git history (`git log -p --all -- 0.20` returns empty).
- **NOT** a pip/uv install constraint artifact — no `pyproject.toml`, Makefile, or scripts/ entry references `0.20` as a version pin.
- **NOT** a coverage `fail_under` artifact — `pyproject.toml` `[tool.coverage.report]` does not set `fail_under = 0.20`.
- **Strongly correlated** with the task-builder-merge release content:
  - `.dev/releases/current/task-builder-merge/artifacts/D-0096/spec.md:81,153,161,226` contains the literal phrase `regression_halt_rate > 0.20` (the OPS-005 threshold).
  - File birth time 15:26:47 falls within the task-builder-merge active window.
- **Most likely cause**: a shell command crafted from that spec (e.g., `echo "$regression_halt_rate > 0.20"` rendered without quotes, or an `awk`/`bash` snippet copy-pasted from the spec like `... > 0.20`) caused a literal shell-redirect to a file named `0.20`. The redirect operator `>` with the next-token `0.20` creates exactly this artifact: zero-byte file named `0.20`.

### Fix recommendation (source-level)
There is no specific source file that "writes" `0.20`. It's a one-off shell accident triggered by content from `.dev/releases/current/task-builder-merge/artifacts/D-0096/spec.md`. Cleanup actions:
1. `rm -f 0.20` (one-line delete).
2. Add a narrow gitignore entry — recommend `/0.[0-9]*` anchored at repo root in `.gitignore` so this specific accident pattern (numeric-version-named files at repo root) cannot be committed. Avoid bare `0.*` (catches legitimate dotfiles).
3. Optionally add a pre-commit hook check for zero-byte files at repo root.

### Follow-up task priority
**P3** — symptom-only cleanup. No source bug to fix; it's an operator error. Low priority unless this happens again (then add the gitignore guard).

---

## 3. `docs/memory/solutions_learned.jsonl` — pollution

### Symptom
- File at `docs/memory/solutions_learned.jsonl` is **604 lines** (`wc -l`), tracked in git, with 16+ test-fixture entries appended 2026-05-18.
- All test entries have signatures like `test_database_connection`, `test_reflexion_with_real_exception`, etc.

### Root cause (file:line) — CONFIRMED
**`src/superclaude/pm_agent/reflexion.py:64-69`**:
```python
if memory_dir is None:
    # Default to docs/memory/ in current working directory
    memory_dir = Path.cwd() / "docs" / "memory"

self.memory_dir = memory_dir
self.solutions_file = memory_dir / "solutions_learned.jsonl"
```

**`tests/unit/test_reflexion.py`** instantiates `ReflexionPattern()` with **NO `memory_dir=` argument** at lines:
- Line 17 — `test_initialization`
- Line 25 — `test_record_error_basic`
- Line 39 — `test_record_error_with_solution`
- Line 52 — `test_get_solution_for_known_error` (calls `record_error`)
- Line 73 — `test_error_pattern_matching` (calls `record_error`)
- Line 118 — `test_error_learning_across_sessions` (calls `record_error`)
- Line 165 — `test_reflexion_with_real_exception` (calls `record_error`)

Each `ReflexionPattern()` with no arg → defaults to `Path.cwd() / "docs" / "memory"` → `record_error` at `reflexion.py:122-124` opens `solutions_learned.jsonl` in append mode and writes a JSON line. When pytest runs from repo root, **`Path.cwd()` = repo root**, so every test run pollutes the real tracked file.

Note: `tests/conftest.py:102-121` provides a proper `temp_memory_dir` fixture that uses `tmp_path`, and exactly **one** test uses it correctly — `tests/unit/test_reflexion.py:98 test_reflexion_memory_persistence` passes `memory_dir=temp_memory_dir`. The other 7 instantiations bypass this safety net.

### Fix recommendation (source-level)
**Two-layer fix**:
1. **Tests**: Change every bare `ReflexionPattern()` in `tests/unit/test_reflexion.py` (lines 17, 25, 39, 52, 73, 118, 165) to `ReflexionPattern(memory_dir=tmp_path)` by accepting the pytest built-in `tmp_path` fixture. This is the unambiguous fix.
2. **Defensive (recommended)**: In `src/superclaude/pm_agent/reflexion.py:64-66`, detect "running under pytest" via `os.environ.get("PYTEST_CURRENT_TEST")` and raise `RuntimeError` if `memory_dir` is None inside a pytest run. This prevents the same footgun in future tests.

Also restore `docs/memory/solutions_learned.jsonl` to its pre-pollution state — git history has the clean version.

### Follow-up task priority
**P1** — actively polluting tracked files on every test run. Both the test fix and the defensive guard belong in a dedicated `fix/reflexion-test-pollution` follow-up.

---

## 4. `docs/mistakes/*.md` — per-test fake-mistake files

### Symptom
- `docs/mistakes/` contains 17 `test_database_connection-*.md` files dated **2025-11-11 through 2026-03-26** (i.e., this has been happening for *six months*, not just today).
- Tonight's additions per the orchestrator brief: `test_database_connection-2026-05-18.md`, `test_reflexion_with_real_exception-2026-05-18.md`, `unknown-2026-05-18.md`.

### Root cause (file:line) — SAME source as #3
**`src/superclaude/pm_agent/reflexion.py:70`**:
```python
self.mistakes_dir = memory_dir.parent / "mistakes"
```
- When `memory_dir = Path.cwd() / "docs" / "memory"`, then `mistakes_dir = Path.cwd() / "docs" / "mistakes"` — the *real* tracked directory.
- **`src/superclaude/pm_agent/reflexion.py:73-74`** then calls `self.mistakes_dir.mkdir(parents=True, exist_ok=True)` on import (in `__init__`).
- **`src/superclaude/pm_agent/reflexion.py:127-128`**: `record_error` calls `_create_mistake_doc(error_info)` whenever `root_cause` or `solution` is set.
- **`src/superclaude/pm_agent/reflexion.py:242-259`**: `_create_mistake_doc` writes `docs/mistakes/[feature]-YYYY-MM-DD.md`.

The 6-month accumulation proves this leak has been in CI / dev test runs since at least 2025-11-11.

### Fix recommendation
**Same fix as #3** — fixing the bare `ReflexionPattern()` calls in `tests/unit/test_reflexion.py` automatically fixes BOTH `solutions_learned.jsonl` pollution AND `docs/mistakes/*.md` pollution, because both targets derive from `memory_dir`.

Cleanup actions:
1. Delete all `docs/mistakes/test_*.md` files (they are test artifacts, not real mistakes).
2. Add `docs/mistakes/test_*.md` to `.gitignore` as a defensive guard.
3. Consider deleting the entire `docs/mistakes/` directory if it has never contained real human-authored mistake docs (verify via `git log --all -- docs/mistakes/`).

### Follow-up task priority
**P1** — same root cause as #3, fix together.

---

## 5. `.dev/eval-runs/research/` (untracked)

### Symptom
- `.dev/eval-runs/research/` contains:
  - `2026-05-18-fork-candidate-research.md`
  - `2026-05-18-cli-extensibility-analysis.md`

### Root cause analysis
- **NOT** a skill-creator workspace violation. The skill-creator override (CLAUDE.md, `src/superclaude/hooks/scripts/reject-workspace-writes.sh:32-34`) targets writes under `.claude/skills/*-workspace/**`, redirecting to `.dev/eval-workspaces/<skill-name>/`. That hook does not fire for `.dev/eval-runs/`.
- **NOT** a sanctioned source location either. Grep confirms `eval-runs` / `eval_runs` does NOT appear in `src/superclaude/`, `.claude/skills/`, any hook, or any settings file. It is **NOT** referenced by any code path or skill convention.
- These two files are **ad-hoc research artifacts** dropped by a Claude Code session (or a human operator) using an invented path. The path is plausible-looking and adjacent to the sanctioned `.dev/eval-workspaces/`, suggesting confused-but-good-intent placement.

### Fix recommendation
1. **Relocate** the two files to the proper destination per `.dev/README.md` (the canonical "where things go" guide):
   - If session-scoped research → `.dev/eval-workspaces/<skill-name>/` or `.dev/research/<YYYY-MM-DD-topic>/`.
   - Look at content to determine the proper home (`fork-candidate-research.md` and `cli-extensibility-analysis.md` sound like `.dev/research/` material).
2. **Delete** `.dev/eval-runs/` once relocated.
3. **No source-code fix needed** — there is no source-code path emitting to `.dev/eval-runs/`. This is a one-off operator slip-up.
4. Optionally add `.dev/eval-runs/` to `.gitignore` as a permanent guard, but since `.dev/` is largely uncommitted-by-convention, this may be unnecessary.

### Follow-up task priority
**P3** — cleanup-only, no source bug.

---

## 6. task-builder-merge `manifest.json` TASKLIST_ROOT placeholder bug — CRITICAL

### Symptom
- `.dev/releases/current/task-builder-merge/manifest.json` reports **"21 missing / 21 total"** with every `expected_path` containing the literal string `TASKLIST_ROOT/`:
  - e.g., `/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md`
- Actual checkpoints exist at `.dev/releases/current/task-builder-merge/checkpoints/CP-P0[1-7]-*.md` (verified — `CP-P04-END.md`, `CP-P05-END.md`, `CP-P05-T01-T05.md`, `CP-P05-T07-T11.md` are all present).
- The "21 missing" report is a false negative caused by the manifest searching for paths that include a literal placeholder.

### Root cause (file:line)
This is a **multi-layer bug** — the manifest extractor faithfully copies what's in the source tasklists, and the source tasklists contain unsubstituted `TASKLIST_ROOT` placeholders.

**Where the placeholder lives in the source tasklist**:
- `.dev/releases/current/task-builder-merge/phase-1-tasklist.md:277`: ``**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` ``
- Same file, line 579, line 295, etc. — 21 such lines across `phase-{1..7}-tasklist.md`.

**Where the extractor reads it**:
- `src/superclaude/cli/sprint/checkpoints.py:36-86` — `extract_checkpoint_paths()`:
  - Line 74: `candidate = Path(raw_path)` — reads `TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md` as a literal Path.
  - Line 75: `if candidate.is_absolute()` — fails (no leading `/`).
  - Line 77: `elif candidate.exists()` — fails (no such file relative to CWD).
  - Line 82: `resolved = (release_dir / candidate).resolve()` — **joins `release_dir` with the literal `TASKLIST_ROOT/...` path**, producing the bogus `.../task-builder-merge/TASKLIST_ROOT/checkpoints/CP-P01-T01-T05.md`.

**Where the placeholder should have been substituted (the upstream bug)**:
- `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md:100`: ``**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/<deterministic-name>.md` ``
- `src/superclaude/commands/tasklist.md:38,40-46` documents that `TASKLIST_ROOT` is **auto-derived** by the tasklist generator command (3-step priority: explicit `.dev/releases/current/<seg>/` substring → version-token fallback → `v0.0-unknown`).
- The bug: the **substitution step never ran** (or ran on the index file but not on the phase files), so the template's literal `TASKLIST_ROOT` token survived into the emitted `phase-N-tasklist.md` files.

### Fix recommendation (source-level)
This is a real, high-impact bug in the tasklist generation pipeline. Two-pronged fix:

1. **Generator-side (PRIMARY)**: In whatever step performs the `TASKLIST_ROOT` placeholder substitution during tasklist generation (per `src/superclaude/commands/tasklist.md:40-46`), ensure substitution applies to **all** emitted phase-N-tasklist.md files, not just the index. Verify by grep-asserting no literal `TASKLIST_ROOT` remains in emitted outputs as a post-emission gate (`src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` is the place to add this rule).

2. **Extractor-side (DEFENSIVE)**: In `src/superclaude/cli/sprint/checkpoints.py:74-82`, after computing `candidate`, raise or warn loudly if `raw_path` contains the literal substring `TASKLIST_ROOT`. This converts a silent false-negative into a noisy fail-fast, which is the right ergonomic for unresolved-placeholder bugs.

3. **One-shot repair of the affected release** (not a long-term fix, but unblocks the current branch): run a sed-rewrite over `.dev/releases/current/task-builder-merge/phase-*-tasklist.md` substituting `TASKLIST_ROOT` → `.dev/releases/current/task-builder-merge` and regenerate the manifest with `superclaude sprint manifest <index>`. Confirm `summary.found` ≥ 17 (matching the checkpoint files actually present in `.dev/releases/current/task-builder-merge/checkpoints/`).

### Follow-up task priority
**P0** — this bug invalidates every checkpoint-completion report for the task-builder-merge release and likely affects ANY release whose tasklist was generated by this version of the protocol. Should be either (a) a dedicated `fix/tasklist-root-substitution` follow-up before merging the current branch, or (b) explicitly called out as a known issue in the PR notes for `feat/hook-sync-and-matcher-fix` and tracked in a follow-up.

---

## Cross-cutting observation: source-vs-symptom matrix

| Garbage path | Source-code bug? | Symptom-only cleanup? | Fix priority |
|---|---|---|---|
| `prd-test-product/`, `prd-dry-run-test/` | **YES** — `src/superclaude/cli/prd/config.py:100` defaults to CWD | Add to `.gitignore` | P1 |
| `0.20` | NO — operator shell-redirect accident | `rm` + narrow `.gitignore` | P3 |
| `docs/memory/solutions_learned.jsonl` pollution | **YES** — `tests/unit/test_reflexion.py:17,25,39,52,73,118,165` use bare `ReflexionPattern()` | Restore from git | P1 |
| `docs/mistakes/test_*.md` (17 files, 6mo history) | **YES** — same as above (`reflexion.py:70` derives `mistakes_dir` from `memory_dir`) | Delete + `.gitignore` | P1 |
| `.dev/eval-runs/research/*` | NO — operator path slip | Relocate per `.dev/README.md` | P3 |
| `task-builder-merge/manifest.json` 21-missing | **YES** — tasklist generator does not substitute `TASKLIST_ROOT` placeholder in phase files (`src/superclaude/commands/tasklist.md:40-46` defines substitution but generator skips phase files); extractor at `src/superclaude/cli/sprint/checkpoints.py:74-82` silently joins literal placeholder to `release_dir` | Sed-rewrite phase files + regenerate manifest | P0 |

---

## Recommended follow-up tasks (for the cleanup plan)

1. **P0 — `fix/tasklist-root-substitution`** (separate from `feat/hook-sync-and-matcher-fix`):
   - Add post-emission gate in `src/superclaude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` rejecting any emitted file containing literal `TASKLIST_ROOT`.
   - Defensive fail-fast in `src/superclaude/cli/sprint/checkpoints.py:74-82` for unresolved placeholders.
   - Sed-repair task-builder-merge phase files + regenerate manifest.

2. **P1 — `fix/reflexion-test-pollution`**:
   - Update all bare `ReflexionPattern()` calls in `tests/unit/test_reflexion.py` (7 sites) to pass `memory_dir=tmp_path`.
   - Add PYTEST_CURRENT_TEST guard in `src/superclaude/pm_agent/reflexion.py:64-66`.
   - Restore `docs/memory/solutions_learned.jsonl` from git.
   - Delete `docs/mistakes/test_*.md` (17+ files).
   - Add `docs/mistakes/test_*.md` to `.gitignore`.

3. **P1 — `fix/prd-default-output-path`**:
   - Change `src/superclaude/cli/prd/config.py:100` to refuse repo-root CWD or default to `.dev/prd-runs/`.
   - Add `prd-*-test/` to `.gitignore`.

4. **P3 — symptom-only cleanup** (bundle into the current `feat/hook-sync-and-matcher-fix` cleanup pass):
   - `rm 0.20` + `.gitignore` entry `/0.[0-9]*`.
   - Relocate `.dev/eval-runs/research/*.md` to a sanctioned `.dev/` subpath, then `rm -rf .dev/eval-runs/`.

---

**Status**: Complete.

**Summary**: 6 garbage-path areas traced to root cause. 4 have genuine source-code bugs (PRD CWD default, reflexion test pollution affecting two output dirs, tasklist-root substitution gap) and 2 are operator slip-ups (`0.20`, `.dev/eval-runs/`). The tasklist-root bug is P0 because it produces a false "21 missing checkpoints" report on the current branch's release. The reflexion test pollution is P1 with 6 months of accumulated debris and ongoing on every test run. All source locations cited with file:line.
