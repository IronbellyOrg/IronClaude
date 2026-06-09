# Research 01: process.py `_build_file_args` Inventory + Dead-Code Analysis

**Topic:** File Inventory + dead-code analysis for the `--file` removal.
**Scope:** `src/superclaude/cli/prd/process.py` and `src/superclaude/cli/pipeline/process.py` (base).
**Track goal:** Remove BOTH `--file` emissions from `PrdClaudeProcess._build_file_args`; the flag is a cloud-download mechanism requiring `CLAUDE_CODE_SESSION_ACCESS_TOKEN` and must not receive local paths.

Status: Complete

---

## 1. `_build_file_args` — the two `--file` emission branches

File: `src/superclaude/cli/prd/process.py`. Method declared at **:169-206** (decorated `@staticmethod` at :169, `def` at :170).

### Branch A — refs > 50KB (the `--file <ref_path>` branch), :191-199

```python
        for ref_name in _PHASE_ALLOWED_REFS.get(base_step, []):
            ref_path = config.skill_refs_dir / ref_name
            if ref_path.is_file():
                try:
                    size = ref_path.stat().st_size
                except OSError:
                    continue
                if size > _FILE_SIZE_THRESHOLD:
                    file_args.extend(["--file", str(ref_path)])
```

Emission is the **single line :199**: `file_args.extend(["--file", str(ref_path)])`.

### Branch B — the `--spec` / spec-file branch, :201-204

```python
        if base_step in _SPEC_FILE_STEPS:
            for spec_path in getattr(config, "spec_files", None) or []:
                if Path(spec_path).is_file():
                    file_args.extend(["--file", spec_path])
```

Emission is the **single line :204**: `file_args.extend(["--file", spec_path])`.

`return file_args` is at **:206**. These two `.extend([...])` calls (:199, :204) are the ONLY two `--file` emissions in the entire `src/superclaude/cli/prd/` tree (confirmed in §7).

---

## 2. How `file_args` flows into the subprocess

File: `src/superclaude/cli/prd/process.py`, in `PrdClaudeProcess.__init__`.

- **:154-155** — the call:
  ```python
          # Build --file args from phase-allowed refs
          file_args = self._build_file_args(config, step_id)
  ```
- **:157-167** — passed straight into the base constructor as `extra_args`:
  ```python
          super().__init__(
              prompt=prompt,
              output_file=output_file,
              error_file=error_file,
              max_turns=config.max_turns,
              model=config.model,
              permission_flag=config.permission_flag,
              timeout_seconds=timeout_seconds,
              output_format="stream-json",
              extra_args=file_args,
          )
  ```

**What happens if `_build_file_args` returns `[]`:** `extra_args=[]` is passed to the base. In the base `__init__` (`src/superclaude/cli/pipeline/process.py:63`), `self.extra_args = extra_args or []` stores `[]`. In `build_command()` (:94) `cmd.extend(self.extra_args)` extends by an empty list — i.e. a **no-op**, and NO `--file` token is ever emitted. So making `_build_file_args` always return `[]` (or removing it and passing `extra_args=[]`/omitting it) is behaviorally safe: the constructed `claude` command simply has no `--file` flags. This is the target end-state.

---

## 3. Base `ClaudeProcess` confirmation (`src/superclaude/cli/pipeline/process.py`)

- Constructor stores extra_args at **:63**: `self.extra_args = extra_args or []` (param default `extra_args: list[str] | None = None` at :48).
- `build_command()` at **:73-95** builds a fixed `cmd` list (:79-91), conditionally adds `--model` (:92-93), then **:94** `cmd.extend(self.extra_args)`. With empty `extra_args` this extends by nothing → **no `--file` emitted**. CONFIRMED: there is no other place in `build_command` that could emit `--file`; the only source of `--file` is `extra_args`.
- `build_env()` at **:97**+ uses **:107** `env = os.environ.copy()` (then pops `CLAUDECODE` :108 and `CLAUDE_CODE_ENTRYPOINT` :109, optional `env.update(env_vars)` :110-111). CONFIRMED `os.environ.copy()`. Note: nothing here sets `CLAUDE_CODE_SESSION_ACCESS_TOKEN`; it is only inherited if present in the parent environment — which is exactly why feeding local paths to `--file` is broken (it is a cloud-download mechanism).

---

## 4. Constants — dead-code determination after removing `_build_file_args`

Repo-wide grep results (`grep -rn ... --include="*.py" .`):

### `_build_file_args`
| file:line | context |
|---|---|
| `src/superclaude/cli/prd/process.py:170` | definition |
| `src/superclaude/cli/prd/process.py:155` | the only production call site (inside `__init__`) |
| `tests/cli/prd/test_spec_flag.py:461` | comment |
| `tests/cli/prd/test_spec_flag.py:485` | test call `PrdClaudeProcess._build_file_args(cfg, "scope-discovery")` |
| `tests/cli/prd/test_spec_flag.py:495` | test call `..._build_file_args(cfg, "investigation-3")` |
| `tests/cli/prd/test_spec_flag.py:506` | test call `..._build_file_args(cfg, "parse-request")` |
| `tests/cli/prd/test_spec_flag.py:510` | test call `..._build_file_args(cfg, "scope-discovery")` |
| `tests/cli/prd/test_spec_flag.py:515` | test call `..._build_file_args(cfg, "scope-discovery")` |

No references to `_build_file_args` exist outside `process.py` and `test_spec_flag.py`. The only production usage is the self-call at :155.

### `_PHASE_ALLOWED_REFS` (defined :95-113)
| file:line | context |
|---|---|
| `src/superclaude/cli/prd/process.py:95` | definition |
| `src/superclaude/cli/prd/process.py:191` | `_PHASE_ALLOWED_REFS.get(base_step, [])` — sole use, inside `_build_file_args` |

**DEAD if `_build_file_args` removed: YES — safe to delete.** Its only reference (:191) is inside the method being removed. No tests reference it (constant-in-tests grep returned empty).

### `_FILE_SIZE_THRESHOLD` (defined :115)
| file:line | context |
|---|---|
| `src/superclaude/cli/prd/process.py:115` | definition |
| `src/superclaude/cli/prd/process.py:198` | `if size > _FILE_SIZE_THRESHOLD:` — sole use, inside `_build_file_args` |

**DEAD if `_build_file_args` removed: YES — safe to delete.** Only reference is :198 inside the removed method. No tests reference it.

### `_SPEC_FILE_STEPS` (defined :121)
| file:line | context |
|---|---|
| `src/superclaude/cli/prd/process.py:121` | definition |
| `src/superclaude/cli/prd/process.py:180` | docstring mention (inside `_build_file_args` docstring) |
| `src/superclaude/cli/prd/process.py:201` | `if base_step in _SPEC_FILE_STEPS:` — sole code use, inside `_build_file_args` |

**DEAD if `_build_file_args` removed: YES — safe to delete.** Only code reference (:201) and only docstring reference (:180) are inside the removed method. No tests reference it.

**Summary:** All three constants become dead once `_build_file_args` is removed. The `base_step` normalization local (`base_step = step_id.rsplit("-", 1)[0] ...` at :187) is also local to the method and disappears with it. Removing the method + all three constants leaves no dangling references in production code.

---

## 5. Docstrings advertising `--file` (text to update)

### Module docstring (`src/superclaude/cli/prd/process.py:1-12`) — relevant lines:
- **:3-5**:
  ```
  Extends the base ``ClaudeProcess`` with PRD-specific prompt construction,
  phase-aware ``--file`` arg scoping, subprocess timeout enforcement via
  external watchdog, and launch retry with exponential backoff.
  ```
  (the phrase "phase-aware ``--file`` arg scoping" on :4 must go.)
- **:11**: `GAP-003: Phase-aware ``--file`` arg scoping.`

### Class docstring (`PrdClaudeProcess`, :130-136) — relevant line:
- **:133**: `    - Phase-aware ``--file`` arg construction (GAP-003)`

(Full class docstring block :132-135:)
```
    Adds:
    - Phase-aware ``--file`` arg construction (GAP-003)
    - Subprocess timeout enforcement via Popen watchdog (NFR-PRD.13/F-004)
    - Launch retry with exponential backoff (NFR-PRD.12/GAP-011)
```

### Other in-method comment/docstring text that disappears with the method:
- :94 comment `# Files > 50KB are passed as --file args; files < 50KB are inlined in prompt.` (sits above `_PHASE_ALLOWED_REFS`, :93-94 comment block)
- :115 trailing comment `# 50KB: inline vs --file cutoff`
- :119 comment `# prompts._authoritative_specs_block); attaching the spec via --file delivers`
- :154 comment `# Build --file args from phase-allowed refs`
- :171-185 the `_build_file_args` docstring (entirely removed with the method)

---

## 6. Existing test coverage

**Only `tests/cli/prd/test_spec_flag.py` asserts on `_build_file_args` output.** Class `TestSpecFileAttach` (starts :477). Helper `_spec_config` at :465-474 builds a `PrdConfig` with `skill_refs_dir=tmp_path / "refs"` (intentionally absent so no ref args fire) and `spec_files=...`.

Tests that will BREAK / need updating once the `--file` emission is removed (expected post-fix behavior is `_build_file_args` gone or always `[]`):

| test | file:line | current assertion |
|---|---|---|
| `TestSpecFileAttach.test_scope_discovery_attaches_each_spec` | :478-487 | `assert args == ["--file", str(a), "--file", str(b)]` (:487) — **will fail** |
| `TestSpecFileAttach.test_investigation_numbered_step_attaches_specs` | :489-498 | `assert "--file" in args` (:497) + `assert str(spec) in args` (:498) — **will fail** |
| `TestSpecFileAttach.test_parse_request_does_not_attach_specs` | :500-506 | `assert ..._build_file_args(cfg, "parse-request") == []` (:506) — still passes (empty), but calls removed method |
| `TestSpecFileAttach.test_no_specs_no_args` | :508-510 | `assert ..._build_file_args(cfg, "scope-discovery") == []` (:510) — still passes, but calls removed method |
| `TestSpecFileAttach.test_missing_spec_file_skipped` | :512-515 | `assert ..._build_file_args(cfg, "scope-discovery") == []` (:515) — still passes, but calls removed method |

The comment block at :459-462 ("spec content delivered via the existing --file mechanism / reuses PrdClaudeProcess._build_file_args") also becomes stale.

**Builder guidance:** the entire `TestSpecFileAttach` class (and its `_spec_config` helper if unused elsewhere) targets a method that is being deleted. If `_build_file_args` is removed outright, this class must be deleted or rewritten to assert the NEW delivery mechanism (R2 covers prompts.py delivery, which is where spec content now flows). The 2 hard-asserting tests (:487, :497-498) are the ones that change behavior; the 3 `== []` tests would still pass but reference a removed symbol and would raise `AttributeError`, so they must be removed/updated too. `_spec_config` is defined only here (no other refs in this file — it is local to `TestSpecFileAttach` usage).

**`tests/cli/prd/test_e2e.py`** patches `superclaude.cli.prd.executor.PrdClaudeProcess` (mock, see :11, :229, and every `@patch(...PrdClaudeProcess)` at :261/323/366/437/519/582/652/718/763/828/859/904/959) — it never constructs a real `PrdClaudeProcess` nor asserts on `extra_args`/`file_args`/`--file`. **No e2e changes needed** for the arg-construction removal.

Grep for `extra_args` in `tests/cli/prd/` and `tests/cli/pipeline/`: **no hits** — no test asserts on the base `extra_args` plumbing directly. Grep for the three constants in `tests/`: **no hits**.

---

## 7. Acceptance grep — `grep -rn '"--file"' src/superclaude/cli/prd/`

Current result (must be 0 after fix):
```
src/superclaude/cli/prd/process.py:199:                    file_args.extend(["--file", str(ref_path)])
src/superclaude/cli/prd/process.py:204:                    file_args.extend(["--file", spec_path])
```
Two hits, both inside `_build_file_args`. Removing the method (and the two constants + docstrings) drops this to **0**, satisfying acceptance.

(For context — sibling pipelines already treat `--file` as broken/cloud-only and inline file content instead: `src/superclaude/cli/roadmap/executor.py:8-9,1107-1108`, `src/superclaude/cli/roadmap/validate_executor.py:11`, `src/superclaude/cli/tasklist/executor.py:10`, `src/superclaude/cli/cli_portify/prompts.py:47`. R2 owns deep sibling-pipeline coverage; noted here only as corroboration that 0 `--file` emissions is the intended convention.)

---

## Summary

- The two `--file` emissions are `process.py:199` (refs>50KB branch, :191-199) and `process.py:204` (spec branch, :201-204), both inside `_build_file_args` (:169-206). Acceptance grep `grep -rn '"--file"' src/superclaude/cli/prd/` currently returns exactly these 2 lines.
- `file_args` flows `__init__:155 → super().__init__(extra_args=file_args):166`; base `process.py:63` stores it, `:94 cmd.extend(self.extra_args)` is a no-op on `[]`, so an empty/removed builder emits NO `--file`. Base `build_env` uses `os.environ.copy()` (`:107`) and never injects `CLAUDE_CODE_SESSION_ACCESS_TOKEN`.
- Constants `_PHASE_ALLOWED_REFS` (:95), `_FILE_SIZE_THRESHOLD` (:115), `_SPEC_FILE_STEPS` (:121) are ALL dead-and-safe-to-delete once `_build_file_args` is removed — their only references are inside that method; zero test references. Docstrings to update: module :4 & :11, class :133. Tests to fix: `TestSpecFileAttach` in `tests/cli/prd/test_spec_flag.py` (hard asserts at :487 and :497-498 break; the 3 `== []` tests at :506/:510/:515 reference the removed symbol). `test_e2e.py` mocks `PrdClaudeProcess` and needs no change.
