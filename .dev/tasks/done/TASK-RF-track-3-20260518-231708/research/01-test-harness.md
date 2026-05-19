# Track 3 Research: Test Harness Inventory + Output-Path Origin

**Task:** TASK-RF-track-3-20260518-231708 (FU-003: PRD-skill CWD-default output routing)
**Scope:** `tests/cli/prd/*` — pinpoint creators of `prd-test-product/` and `prd-dry-run-test/` at repo root
**Status:** Complete

---

## Headline finding (verdict on the user's stub hypothesis)

**The user's stub hypothesis is WRONG.** `tests/cli/prd/test_prompts.py` is NOT
the creator of the repo-root `prd-test-product/` and `prd-dry-run-test/` dirs.
The grep that "confirmed" it (`prd-test-product` → `tests/cli/prd/test_prompts.py:44`)
matches `tmp_path / "prd-test-product"` — which is already correctly scoped to
pytest's per-test tmp_path under `/tmp/pytest-of-<user>/...`. That fixture
cannot escape to the repo root.

**The actual creator is a human-run `superclaude prd run` invocation** that
omitted `--output` and relied on the CWD default at
`src/superclaude/cli/prd/config.py:100`:

```python
output_path = Path(output).resolve() if output else Path(".").resolve()
```

Combined with `task_dir_name = f"prd-{product_slug}"` (line 107) and
`task_dir = output_path / task_dir_name` (line 108), running
`superclaude prd run "..." --product "test product"` from the repo root creates
`<repo-root>/prd-test-product/`. Same pattern for `--product "dry run test"` →
`<repo-root>/prd-dry-run-test/`.

Cross-evidence: `.dev/eval-workspaces/prd-test-product/execution-log.md:3-4`
records `Started 2026-05-14T07:12:13`, `Task Dir: /config/workspace/IronClaude/prd-test-product`
— wall-clock + repo-root absolute path = real CLI run, not pytest. Prior research
in `.dev/tasks/to-do/TASK-RF-20260518-181333/research/05-data-flow-tracer.md:213`
independently identified `src/superclaude/cli/prd/config.py:100` as the
source-cause.

**So:** the test harness is NOT the source-fix site. The source-fix is in
`src/superclaude/cli/prd/config.py:100` (the CWD default itself). Tests are
fine. Track 3's framing of "test harness as source-fix" should be revised
upstream of merge.

---

## 1. `tests/cli/prd/` file inventory

| File                  | Lines | 1-line purpose |
|-----------------------|------:|----------------|
| `__init__.py`         |     0 | Empty package marker. |
| `test_cli_smoke.py`   |    79 | Click CLI smoke tests: `--help` surface, dry-run exit codes, tier validation. (`tests/cli/prd/test_cli_smoke.py:1-80`) |
| `test_e2e.py`         |   564 | End-to-end pipeline behavior (uses `tmp_path` fixture `e2e_task_dir`, line 36-38). |
| `test_executor.py`    |   139 | `PrdExecutor` unit tests (uses `prd_config` fixture, line 28-41). |
| `test_filtering.py`   |   137 | Filtering logic unit tests. |
| `test_gates.py`       |   219 | QA-gate logic unit tests. |
| `test_integration.py` |   348 | Pipeline integration (uses `tmp_task_dir` fixture, line 44-46; `tmp_path/.dev/tasks/to-do/TASK-PRD-test-product` at line 122 — still inside tmp_path). |
| `test_inventory.py`   |   126 | Inventory-step unit tests. |
| `test_models.py`      |   121 | `PrdConfig` model unit tests. |
| `test_prompts.py`     |   276 | Prompt-builder unit tests (the file the user flagged). |

Total: 2009 lines across 10 files (incl. empty `__init__.py`).

`wc -l` evidence: ran `wc -l tests/cli/prd/*.py` — counts match table above.

---

## 2. `tests/cli/prd/test_prompts.py` anatomy

**Total: 4 test functions across 4 classes** (matches the module docstring
"Section 8.1 test plan: 4 tests" at line 3).

### Fixtures (lines 41-115)

| Fixture     | Lines  | Behavior |
|-------------|-------:|----------|
| `task_dir`  | 41-90  | `tmp_path / "prd-test-product"`, creates subdirs `research/`, `synthesis/`, `qa/`, writes `parsed-request.json`, `scope-discovery-raw.md`, `TASK-PRD-test-product.md`, `research-notes.md`. **All under `tmp_path`** — pytest auto-cleans. |
| `config`    | 93-115 | Builds a `PrdConfig` with `task_dir=task_dir`, `output_path=task_dir/"output.md"`, plus a skill-refs sub-dir. **All under `tmp_path`**. |

### Test functions

| # | Class / Test | Signature | What it does |
|---|---|---|---|
| 1 | `TestInvestigationPromptStalenessProtocol.test_build_investigation_prompt_includes_staleness_protocol` (lines 123-139) | `(self)` — no fixtures | Calls `build_investigation_prompt(...)` with literal string/Path args, asserts staleness-protocol markers in returned prompt text. **No filesystem writes.** |
| 2 | `TestSynthesisPromptTemplateReference.test_build_synthesis_prompt_includes_template_reference` (lines 142-156) | `(self)` — no fixtures | Calls `build_synthesis_prompt(...)`, asserts template-path string appears in output. **No filesystem writes.** |
| 3 | `TestPromptSizeUnder100KB.test_prompt_size_under_100kb` (lines 159-245) | `(self, config: PrdConfig)` — uses `config` fixture (→ `task_dir` → `tmp_path`) | Invokes all 19 prompt builders, asserts each output < 100KB. **All filesystem activity scoped to `tmp_path`.** |
| 4 | `TestReadFileTruncation.test_read_file_truncation_at_50kb` (lines 248-276) | `(self, tmp_path: Path)` — uses `tmp_path` directly | Writes `exact.txt` / `over.txt` / `small.txt` under `tmp_path`, asserts `_read_file()` truncation semantics. **All under `tmp_path`.** |

### `prd-test-product` mentions

Single hit at **line 44**: `td = tmp_path / "prd-test-product"`. This is the
name of a subdirectory under pytest's per-test `tmp_path` (typically
`/tmp/pytest-of-<user>/pytest-<N>/test_<name>0/prd-test-product/`). It does
NOT create anything at the repo root.

### `prd-dry-run-test` mentions

**Zero hits** anywhere in `tests/cli/prd/`. The user's stub hypothesis that this
dir is created by tests is unsupported by source evidence. Grep result:

```
$ grep -rn "prd-dry-run-test" tests/ src/
(no source-file hits — only matches in .dev/tasks/.../research-notes.md and
 .dev/eval-workspaces/prd-dry-run-test/execution-log.md)
```

---

## 3. Output-path argument flow

### `test_prompts.py:44` — `prd-test-product`

- **Path passed:** `tmp_path / "prd-test-product"` (a fresh, per-test
  tmp directory provided by pytest's built-in `tmp_path` fixture).
- **Computed from:** pytest builtin `tmp_path` (NOT `os.getcwd()`, NOT a
  constant, NOT a project fixture).
- **Existing `tmp_path` alternative NOT being used:** N/A — `tmp_path` IS
  already in use; no fix needed here.
- **Line numbers of `prd-test-product` occurrences:** `tests/cli/prd/test_prompts.py:44` (the only one in the repo's source tree).

### `prd-dry-run-test`

- **No occurrence in any tests/cli/prd/*.py file.** The dir is created by a
  real `superclaude prd run --product "dry run test"` invocation (or similar
  product-name input), via `src/superclaude/cli/prd/config.py:100` (CWD
  default) + `:107-108` (task_dir = output_path / f"prd-{slug}").

### Indirect creators (CLI invocations under test that DO resolve a config but don't write to disk)

| Test | File:Line | Behavior |
|------|-----------|----------|
| `test_prd_run_dry_run_exits_zero` | `test_cli_smoke.py:52-56` | Calls `prd run test --dry-run`. `dry_run=True` short-circuits before `PrdExecutor` instantiation (`commands.py:119-125`). `PrdLogger.__init__` (which contains the only `task_dir.mkdir(...)` at `logging_.py:56`) is NEVER reached. **No filesystem side-effects at repo root.** |
| `test_prd_run_dry_run_validates_config` | `test_cli_smoke.py:63-79` | Same dry-run short-circuit. **No filesystem side-effects.** |
| `test_prd_run_invalid_tier_exits_nonzero` | `test_cli_smoke.py:58-61` | `resolve_config` raises `ValueError`, exits 1 before any dir creation. |
| `test_prd_help_shows_subcommands` / `test_prd_run_help_shows_options` / `test_prd_resume_help_shows_options` | `test_cli_smoke.py:21-50` | `--help` only. No config resolution. |

**Net: zero tests in `tests/cli/prd/` create anything at the repo root.**

### Source-cause chain (the actual one)

```
human types: superclaude prd run "make a PRD" --product "test product"
             (intentionally OR accidentally omits --output)
                          │
                          ▼
src/superclaude/cli/prd/commands.py:104  resolve_config(output=None, ...)
                          │
                          ▼
src/superclaude/cli/prd/config.py:100   output_path = Path(".").resolve()
                                        # → /config/workspace/IronClaude (or wherever CWD is)
                          │
                          ▼
src/superclaude/cli/prd/config.py:104   product_slug = _slugify("test product")  → "test-product"
src/superclaude/cli/prd/config.py:107   task_dir_name = "prd-test-product"
src/superclaude/cli/prd/config.py:108   task_dir = <CWD> / "prd-test-product"
                          │
                          ▼
src/superclaude/cli/prd/executor.py:?   PrdExecutor(config).run()
                          │
                          ▼
src/superclaude/cli/prd/logging_.py:52-56  PrdLogger.__init__ does
                                            task_dir.mkdir(parents=True, exist_ok=True)
                                            → creates <repo-root>/prd-test-product/
                                            → writes execution-log.{md,jsonl}
```

---

## 4. Recommended fix

### Primary fix (source-of-truth) — **NOT the test harness**

The source-fix is `src/superclaude/cli/prd/config.py:100`. Change the CWD
default to a sandboxed, conventional location. Recommended diff:

```diff
--- a/src/superclaude/cli/prd/config.py
+++ b/src/superclaude/cli/prd/config.py
@@ -97,7 +97,17 @@ def resolve_config(
             )

     # -- Path resolution --
-    output_path = Path(output).resolve() if output else Path(".").resolve()
+    if output:
+        output_path = Path(output).resolve()
+    else:
+        # Default sandbox: .dev/eval-workspaces/ when running from a repo that
+        # has one (avoids polluting the repo root with prd-<slug>/ dirs);
+        # fall back to CWD only when no sandbox is available.
+        sandbox = Path(".dev/eval-workspaces").resolve()
+        if sandbox.parent.exists():  # i.e. .dev/ exists → we're in a repo
+            sandbox.mkdir(parents=True, exist_ok=True)
+            output_path = sandbox
+        else:
+            output_path = Path(".").resolve()
```

### Defense-in-depth (hook layer) — already in place per Track 2

`.claude/hooks/reject-workspace-writes.sh` (Track 2 research) rejects
edits/writes that target paths matching `prd-*/` at repo root if a defensive
matcher is added. This catches future regressions even if the source-fix is
reverted or bypassed.

### Test-harness changes — **none required**

`tests/cli/prd/test_prompts.py:44` already uses `tmp_path / "prd-test-product"`.
Pytest's `tmp_path` is per-test and auto-cleaned. No change to test code is
needed for FU-003.

**If Track 3 owners insist on a "test harness fix" deliverable**, the only
honest framing is to *add a regression test* that asserts the new default is
`.dev/eval-workspaces/` (not CWD). Suggested file:
`tests/cli/prd/test_config.py` (does not exist yet) or add a class to
`tests/cli/prd/test_models.py`:

```python
def test_resolve_config_defaults_output_to_dev_eval_workspaces(tmp_path, monkeypatch):
    """FU-003: default output dir is .dev/eval-workspaces/, not CWD."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".dev").mkdir()  # simulate repo with .dev/
    cfg = resolve_config("make a PRD", product="test product")
    assert cfg.task_dir == tmp_path / ".dev" / "eval-workspaces" / "prd-test-product"
    assert "prd-test-product" not in {p.name for p in tmp_path.iterdir()}
```

---

## 5. Other `tests/cli/prd/` files potentially affected

Auditing every file for repo-root escape risk:

| File                  | Risk | Evidence |
|-----------------------|------|----------|
| `test_cli_smoke.py`   | **Low** — dry-run short-circuits before any mkdir. Only risk: if someone removes the `if dry_run: return` guard in `commands.py:119-125`, the test invocations at `test_cli_smoke.py:54`, `:60`, `:66-76` would resolve `output_path = Path(".").resolve()` to *the pytest process's CWD* (typically the repo root). Defense: the recommended `config.py` fix above; tests do not need to chdir to tmp_path because they don't reach the executor. |
| `test_e2e.py`         | **Low** — uses `tmp_path` fixture (line 36-38: `task_dir = tmp_path / "prd-test-e2e"`). No `os.getcwd()` or `Path(".")` usage in grep. |
| `test_executor.py`    | **Low** — uses `prd_config` fixture (line 28-41). Need to spot-check that the fixture sets `task_dir` under `tmp_path` if rigour is required. (Not inspected exhaustively here — out of scope per Track 3 focus on test_prompts.py.) |
| `test_filtering.py`   | **Low** — pure logic tests, no FS evidence in grep. |
| `test_gates.py`       | **Low** — pure logic tests. |
| `test_integration.py` | **Low** — `tmp_task_dir` fixture (line 44-46) + line 115 `config.work_dir = tmp_path` + line 122 `task_root = tmp_path / .dev / tasks / to-do / TASK-PRD-test-product` all under `tmp_path`. |
| `test_inventory.py`   | **Low** — no FS-escape evidence in grep. |
| `test_models.py`      | **Low** — line 109 mentions `"superclaude prd resume research-notes --product MyApp ..."` as a string assertion, not an execution. |
| `test_prompts.py`     | **Already safe** — see Section 2/3 above. |

**Summary of risk surface in tests/:** zero. The repo-root escape is a
production-code defect in `src/superclaude/cli/prd/config.py:100`, not a test
defect. Track 3's source-fix should target `config.py`, with a defensive hook
matcher and a new regression test as the only test-harness work.

---

## Appendix: Evidence index

| Claim | Citation |
|---|---|
| `test_prompts.py:44` is the only `prd-test-product` occurrence in source | `grep -rn prd-test-product tests/ src/` returns 1 hit |
| `prd-dry-run-test` has zero occurrences in tests/ or src/ | `grep -rn prd-dry-run-test tests/ src/` returns 0 hits |
| CWD default lives at `config.py:100` | `src/superclaude/cli/prd/config.py:100` direct quote: `output_path = Path(output).resolve() if output else Path(".").resolve()` |
| `task_dir` shape | `src/superclaude/cli/prd/config.py:107-108`: `task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"`; `task_dir = output_path / task_dir_name` |
| Mkdir happens in PrdLogger | `src/superclaude/cli/prd/logging_.py:52-56` |
| Dry-run short-circuits before executor | `src/superclaude/cli/prd/commands.py:119-125` (no executor call) |
| Real-run timestamp confirms human invocation | `.dev/eval-workspaces/prd-test-product/execution-log.md:3-4` (Started 2026-05-14T07:12:13, Task Dir = /config/workspace/IronClaude/prd-test-product) |
| Prior research independently identified same source-cause | `.dev/tasks/to-do/TASK-RF-20260518-181333/research/05-data-flow-tracer.md:213` |
