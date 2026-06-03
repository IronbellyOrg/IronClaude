# Research: Tests, Sync, Registration

Status: Complete
Date: 2026-06-03

Scope: Tests conventions + Sync model + Registration surfaces + Gitignore mechanics for the sc-recommend lookup-cache feature.

---

## 1. Tests Conventions

### 1.1 Layout — where a new recommend-cache test goes

- `tests/` top-level has both flat files (e.g. `tests/cli/test_install_hooks.py`) and per-domain subdirs (`tests/cli/`, `tests/roadmap/`, `tests/sprint/`, `tests/tasklist/`, `tests/hooks/`, `tests/skills/`, `tests/pipeline/`).
- **No `tests/recommend/` exists today** (verified: `ls tests/recommend/` -> absent).
- Python CLI modules are tested under `tests/cli/`. Roadmap CLI submodule (`src/superclaude/cli/roadmap/`) is tested under `tests/roadmap/` (a flatter mirror).
- **Recommendation for the new YAML reader/writer module**: if it lands at `src/superclaude/cli/recommend/` (a CLI submodule like `roadmap/`), follow the roadmap precedent and create `tests/recommend/` with its own `conftest.py` + `__init__.py` (roadmap has both — `tests/roadmap/conftest.py`, `tests/roadmap/__init__.py`). If it is a single module `src/superclaude/cli/recommend_cache.py`, a single file `tests/cli/test_recommend_cache.py` fits the flat-file pattern (mirrors `tests/cli/test_install_hooks.py`).
- File naming: `test_<module>.py`; test functions `test_<behavior>` or scenario-ID-prefixed (`test_V1_...`, `test_case_1_...`). Class grouping is used in roadmap tests (`class TestRegistryPersistence:`).

### 1.2 Pytest patterns observed

- **`tmp_path` fixture** is the universal sandbox for file-writing tests. `tests/roadmap/test_convergence.py` `TestRegistryPersistence` uses `path = tmp_path / "registry.json"` then `reg.save()` -> reload (`test_save_and_reload`, line 222). This is the exact template for testing the cache YAML reader/writer.
- **`monkeypatch.setattr`** to redirect source-locator functions (e.g. `tests/cli/test_install_hooks.py:106` patches `superclaude.cli.install_hooks._get_hooks_source`). Use this if the cache module resolves `.claude/cache/` paths via a helper that needs redirecting to `tmp_path` in tests.
- **`unittest.mock.patch`** to simulate crash mid-write: `test_install_hooks.py:366` patches `superclaude.cli.install_hooks.os.replace` with `side_effect=OSError(...)` and asserts the target file is unchanged + temp file cleaned up. **This is the direct template for atomic-write tests of the cache writer.**
- **Click `CliRunner`** for CLI-surface tests: `tests/cli/test_cli_registration.py:55` `runner = CliRunner()`, `runner.invoke(main, ["--help"])`. Used to assert a new command group is registered without spawning a subprocess.
- **`subprocess.run(["make", "verify-sync"], ...)`** for verify-sync integration tests (`tests/cli/test_verify_sync_hooks.py:58`), guarded by `pytest.mark.skipif(not _HAS_MAKE/_HAS_JQ)`.
- **Markers**: auto-markers `@pytest.mark.unit` / `@pytest.mark.integration` applied by path (`/unit/`, `/integration/`) per CLAUDE.md pytest plugin. Custom markers: `confidence_check`, `self_check`, `reflexion`, `complexity(...)`. `test_verify_sync_hooks.py:49` uses module-level `pytestmark = [pytest.mark.skipif(...)]`.
- **WARNING for verify-sync-style tests**: `tests/cli/test_verify_sync_hooks.py:7-15` documents these tests MUST NOT run under pytest-xdist — they mutate real `src/superclaude/` files in `try/finally` and the editable install resolves `_FRESHNESS_SCRIPTS` against the outer repo regardless of subprocess `cwd`. A new recommend-hook verify-sync test that mutates the installer list inherits this constraint.

### 1.3 YAML-roundtrip + atomic-write testing template

The merged-requirements §"Storage" says the cache mirrors `convergence.py:DeviationRegistry`. **Important nuance (verified):**

- `convergence.py:DeviationRegistry.save()` (lines 304-317) writes **JSON, not YAML**: `data = {...}; tmp_path = self.path.with_suffix(".tmp"); tmp_path.write_text(json.dumps(data, indent=2)); os.replace(...)`.
- The atomic pattern it models is: **tmp file (`with_suffix(".tmp")`) -> write -> `os.replace()`**. NOTE: `with_suffix(".tmp")` puts the temp file in the SAME directory (atomic-rename-safe) but uses a FIXED name (not a randomized `.tmp.<pid>` suffix) — concurrent writers would collide. `install_hooks.py:_atomic_write_json` uses a randomized temp name (`.{name}.tmp.*` per `test_install_hooks.py:376`). The cache writer should prefer the `install_hooks` randomized-temp variant for the documented worktree-concurrency risk (merged-req Risk #12), though MVP punts to last-write-wins.
- Test template for YAML roundtrip (adapt `test_save_and_reload`): write rows via the cache writer to `tmp_path / "sc-recommend-lookup.yaml"`, reload via the reader, assert row fields survive (`schema_version`, `surface_hash`, `rows[].key`, `best_model`, `eval_history`). YAML uses `pyyaml` (`yaml.safe_load`/`yaml.safe_dump`) — see §5 for the dep.
- Atomic-write crash test (adapt `test_case_8_atomic_write_no_partial`): `patch("superclaude.cli.recommend.<mod>.os.replace", side_effect=OSError(...))`, assert original file unchanged + temp cleaned up.

---

## 2. Sync Model (`make sync-dev` / `make verify-sync`)

Verified from `Makefile` (no external sync script; the logic is inline shell in the targets).

### 2.1 What `sync-dev` copies (Makefile lines 109-163)

`src/superclaude/` -> `.claude/`, per component type:

- **Skills** (112-125): each `src/superclaude/skills/*/` with a `SKILL.md`/`skill.md` -> `.claude/skills/<name>/` (recursive file copy, excludes `__init__.py` + `__pycache__`). `__*` dirs skipped.
- **Agents** (126-130): `src/superclaude/agents/*.md` (except `README.md`) -> `.claude/agents/`.
- **Commands** (131-136): `src/superclaude/commands/*.md` (except `README.md`/`__init__.py`) -> `.claude/commands/sc/`.
- **Hooks** (137-143): `src/superclaude/hooks/scripts/*.sh` -> `.claude/hooks/` + `chmod +x`. (This is how a NEW hook script reaches `.claude/hooks/`.)
- **Legacy** (144-147): `src/superclaude/scripts/session-init.sh` -> `.claude/hooks/session-init.sh`.
- **Templates** (148-157): `src/superclaude/templates/**` -> `.claude/templates/` (excludes `agent-memory/`).

**Implication for the cache feature**: a new hook script (e.g. a cache-warming or cache-related PreToolUse hook) MUST be placed at `src/superclaude/hooks/scripts/<name>.sh` to be synced. The `.claude/cache/*.yaml` lookup tables are NOT a sync-dev artifact — they are runtime/tracked data committed directly, NOT generated from `src/`. So the cache YAMLs live ONLY under `.claude/cache/` (no `src/` mirror), which is consistent with merged-req treating them as shared tracked artifacts.

### 2.2 What `verify-sync` checks (Makefile lines 166-353) — gates the new module/hook must not break

Sections, each setting `drift=1` + `exit 1` on failure:

1. **`=== Skills ===`** (170-200): bidirectional. Every `src/` skill must exist+match in `.claude/`; every `.claude/skills/<X>` must have a `SKILL.md` AND a `src/` counterpart, else `❌ MISSING in src/` or the "no SKILL.md -> move to .dev/eval-workspaces" error.
2. **`=== Agents ===`** (202-226), **`=== Commands ===`** (228-252), **`=== Templates ===`** (280-305): same bidirectional diff pattern.
3. **`=== Hooks ===`** (254-278): every `src/superclaude/hooks/scripts/*.sh` must exist+match `.claude/hooks/<name>.sh`; reverse check — every `.claude/hooks/*.sh` (except `session-init.sh`) must have a `src/` counterpart else `❌ MISSING in src/superclaude/hooks/scripts/`.
4. **`=== Installer Registration ===`** (307-326): **THE GATE FOR A NEW HOOK.** Compares `ls src/superclaude/hooks/scripts/*.sh` (basenames, sorted) against `_FRESHNESS_SCRIPTS` (imported live via `uv run python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS..."`). `comm -23` -> "MISSING from _FRESHNESS_SCRIPTS"; `comm -13` -> "STALE in _FRESHNESS_SCRIPTS". **Therefore: any new `.sh` added to `src/superclaude/hooks/scripts/` MUST also be added to `_FRESHNESS_SCRIPTS` in `install_hooks.py`, or verify-sync fails.** (Matches user instruction "register new hook in install_hooks.py:43".)
5. **`=== Hooks Cross-Consistency ===`** (328-346): jq-based; ONLY checks `hooks.json` PostToolUse auggie matcher prefixes vs `auggie-flag-clear.sh` case body. **Does NOT check the new cache feature unless it adds an auggie-prefixed PostToolUse hook.** A PreToolUse hook (like sc-recommend-phase0.sh) is NOT covered here.

**verify-sync does NOT check**: `.gitignore` contents; `hooks.json` <-> `.claude/settings.json` PreToolUse registration; presence of `.claude/cache/*.yaml`. So the gitignore edit and any settings.json registration are NOT verify-sync-gated — they need their own tests if desired.

### 2.3 SoT discipline (confirmed, per CLAUDE.md)

- `src/superclaude/` is source-of-truth; `.claude/{skills,commands,agents,hooks,templates}/` is generated by `make sync-dev`.
- **NEVER stage `.claude/` except `.claude/settings.json`.** All edits land in `src/`, then `make sync-dev` + `make verify-sync`.
- **EXCEPTION introduced by this feature**: `.claude/cache/*.yaml` + `.claude/cache/eval-runs/**` become TRACKED (committed) artifacts via the gitignore exception (§4). These are NOT sync-dev output and NOT in `src/` — they are user-authorized tracked runtime data. The CLAUDE.md "never stage `.claude/`" rule is for sync-dev mirrors; the cache files are a deliberate, documented exception (merged-req §"Gitignore Exception (R3)").

---

## 3. Registration Surfaces

### 3.1 `src/superclaude/cli/main.py` — command-group registration pattern

Top-level groups are registered at module bottom (lines 400-426) via deferred imports to avoid circular imports. Exact pattern (lines 404-406, roadmap):

```python
from superclaude.cli.roadmap import roadmap_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

main.add_command(roadmap_group, name="roadmap")
```

To wire a `recommend` CLI group (e.g. for `superclaude recommend cache ...` or the `--eval` pipeline), add at the bottom of main.py:

```python
from superclaude.cli.recommend.commands import recommend_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

main.add_command(recommend_group, name="recommend")
```

- `recommend_group` should be a `@click.group()` in `src/superclaude/cli/recommend/commands.py` (mirrors `cli/roadmap/`, `cli/prd/commands.py`, `cli/eval/commands.py`).
- **Regression test obligation**: `tests/cli/test_cli_registration.py:31` `EXPECTED_TOP_LEVEL_COMMANDS` is a frozen snapshot (`cleanup-audit, cli-portify, doctor, eval, install, install-skill, mcp, prd, roadmap, sprint, tasklist, update, version`). Adding `recommend` REQUIRES adding `"recommend"` to that frozenset, or `test_top_level_command_roster_unchanged` fails (`unexpected top-level commands present`). Mirror `tests/cli/test_cli_registration.py` for the new group's own surface test.

### 3.2 `install_hooks.py:43` `_FRESHNESS_SCRIPTS` — new-hook registration

`_FRESHNESS_SCRIPTS` (install_hooks.py lines 43-86) is the list of script basenames deposited to `~/.claude/hooks/` by `superclaude install`. Current members include `sc-recommend-phase0.sh` (lines 76-85) as the template for a project-local sc-recommend hook. A NEW cache-related hook script:

1. Create `src/superclaude/hooks/scripts/<new-hook>.sh`.
2. Add `"<new-hook>.sh"` to `_FRESHNESS_SCRIPTS` (install_hooks.py:43 block).
3. `make sync-dev` copies it to `.claude/hooks/<new-hook>.sh` (+chmod +x).
4. `make verify-sync` `=== Installer Registration ===` gate now passes (script <-> list match).

The verify-sync test mutators in `tests/cli/test_verify_sync_hooks.py:92-118` (`_temporarily_mutate_freshness_list`) regex-parse `_FRESHNESS_SCRIPTS = [...]` — keep the list a simple double-quoted `.sh` literal list so that helper continues to work.

### 3.3 PreToolUse hook registration — `hooks.json` vs `.claude/settings.json`

**Two distinct registration files** (verified):

- `src/superclaude/hooks/hooks.json` — GLOBAL/user hooks installed to `~/.claude/settings.json` by `install_hooks`. Contains freshness + auggie PostToolUse. Commands use `~/.claude/hooks/<name>.sh`. Does NOT contain sc-recommend-phase0.
- `.claude/settings.json` (the ONLY tracked `.claude/` file) — PROJECT-LOCAL hooks. Commands use `$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.sh`. **`sc-recommend-phase0.sh` is registered HERE** (settings.json lines 15-25), matcher `"Skill"`, with a `description`, `timeout: 3`.

**Template for a new project-local PreToolUse hook** (the sc-recommend-phase0 registration, settings.json lines 15-25):

```json
{
  "matcher": "Skill",
  "description": "...what the hook does + Source: src/superclaude/skills/.../SKILL.md ...",
  "hooks": [
    {
      "type": "command",
      "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/<new-hook>.sh",
      "timeout": 3
    }
  ]
}
```

- Add the new object to the `PreToolUse` array in `.claude/settings.json` (lines 3-26). **settings.json IS allowed to be staged/committed** (the single tracked `.claude/` file).
- The hook SCRIPT still goes in `src/superclaude/hooks/scripts/` (synced to `.claude/hooks/`) + registered in `_FRESHNESS_SCRIPTS` (§3.2). settings.json just points at the project-relative path.
- Hook-script template: `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` — fail-open (`set -u`, `exit 0`), cheap stdin prefilter (`case "$INPUT" in *'sc-recommend'*) ;; *) exit 0;;`), then `jq -r '.tool_name'` / `.tool_input.skill` gate, then heredoc context block to stdout. Reuse this exact shape for a cache-related Skill-gate hook.

NOTE: a new PreToolUse object in settings.json is NOT verify-sync-gated; if a regression guard is wanted, add a JSON-parse test (CliRunner not needed — just `json.loads(settings.json)` + assert the matcher/command present), analogous to `test_real_hooks_json_gates_write_in_pre_tool_use` (`tests/cli/test_install_hooks.py:438`).

---

## 4. Gitignore Mechanics

### 4.1 EXACT current state (verified `.gitignore`)

```
# Line 101-104
# Claude Code - only ignore user-specific files
.claude/history/
.claude/cache/          # <- line 103: cache is currently IGNORED
.claude/*.lock

# Line 117-118
.claude/                # <- second, BROAD ignore of all of .claude/
!.claude/settings.json  # <- the existing negation exception
```

**Two separate ignore lines hit `.claude/cache/`**: line 103 (`.claude/cache/` explicit) AND line 117 (`.claude/` broad). Git applies last-match-wins, and a negation (`!`) only re-includes if its parent dir is not excluded by a later pattern. **Both must be neutralized for the cache files to be tracked.**

### 4.2 Required edit per merged-req §"Gitignore Exception (R3)" (lines 81-105, 410)

The merged-req prescribes (companion to existing `!.claude/settings.json`):

```
!.claude/cache/
!.claude/cache/sc-recommend-lookup.yaml
!.claude/cache/sc-recommend-plugin.yaml
!.claude/cache/eval-runs/
!.claude/cache/eval-runs/**
# But re-ignore high-churn telemetry (per-session local data)
.claude/cache/sc-recommend-events.jsonl
```

### 4.3 Ordering rules (CRITICAL — git negation semantics)

Git `.gitignore` rules: (a) later patterns override earlier ones; (b) **you cannot re-include a file if a parent directory of that file is excluded** — so `!.claude/cache/` (re-include the dir) MUST come AFTER the broad `.claude/` ignore at line 117, AND the dir negation must precede file negations inside it.

Therefore the safe placement is **immediately after line 118 (`!.claude/settings.json`)**, NOT after line 103. Resulting block (lines 117+):

```
.claude/
!.claude/settings.json
# (R3) Lookup-cache tracked artifacts — user-authorized exception
!.claude/cache/
!.claude/cache/sc-recommend-lookup.yaml
!.claude/cache/sc-recommend-plugin.yaml
!.claude/cache/eval-runs/
!.claude/cache/eval-runs/**
# Re-ignore high-churn per-session telemetry
.claude/cache/sc-recommend-events.jsonl
```

**Pitfalls verified against current file:**
- The line-103 `.claude/cache/` ignore comes BEFORE the negations, so it is correctly overridden by the later `!.claude/cache/`. It can be left in place (harmless) or removed; removing it is cleaner but not required for correctness. The line-117 broad `.claude/` is the one that MUST precede the negations — it does (negations go after 118).
- `!.claude/cache/` (re-include the directory) is mandatory FIRST — without it, git won't descend into `.claude/cache/` and the per-file negations have no effect (parent-dir-excluded rule).
- The final `.claude/cache/sc-recommend-events.jsonl` re-ignore MUST be the LAST of these lines so it wins over `!.claude/cache/`.
- `!.claude/cache/eval-runs/` (trailing slash, dir) THEN `!.claude/cache/eval-runs/**` (contents) — both needed: the dir negation lets git descend, `**` re-includes nested files.

NOTE: there is no `.gitignore` test in the suite today; if a regression guard is desired, a test could `git check-ignore -v <path>` for `.claude/cache/sc-recommend-lookup.yaml` (expect NOT ignored) and `.claude/cache/sc-recommend-events.jsonl` (expect ignored). "Unverified" whether the builder will add such a test — none exists currently.

---

## 5. pyproject.toml — deps + config relevant to a new module

- **`pyyaml>=6.0`** is ALREADY a hard dependency (pyproject.toml:38, in `dependencies` at line 34). No dep change needed for YAML read/write. Use `import yaml; yaml.safe_load / yaml.safe_dump`.
- **pytest config** (lines 102-136): `testpaths = ["tests"]`, `python_files = ["test_*.py"]`, `python_classes = ["Test*"]`, `python_functions = ["test_*"]`, `addopts = ["-v", "--strict-markers", "--tb=short"]`. `--strict-markers` means any NEW custom marker must be declared in the `markers` list (lines 112-136) or pytest errors. Stick to existing markers (`unit`, `integration`) unless adding a declared one.
- **ruff config** (lines 178-211): `line-length = 88`, `target-version = "py310"`, `select = ["E","F","I","N","W","TID"]` (note `I` = isort import-sorting and `N` = pep8-naming are enforced — new module must have sorted imports and PEP8 names). `extend-exclude` includes `.dev/` (so the research/eval-workspace files are NOT linted). A new module under `src/superclaude/cli/recommend/` IS linted.
- **Banned API** (lines 208-211): `anthropic` SDK imports are globally banned. The `--eval` pipeline must reach Claude via subprocess (PtyDriver / ClaudeProcessAdapter under `cli/eval/`), NOT in-process `import anthropic`. Relevant because merged-req §"--eval Flag" spawns subagents — reuse the existing `cli/eval/` harness, do not import anthropic.
- Test deps (lines 43-54 optional `[dev]`): `pytest-cov`, `pytest-benchmark`, `ruff`, `pytest`. No new test dep needed for YAML/atomic-write tests (stdlib `unittest.mock` + `tmp_path` + `pyyaml` cover it).

---

## Summary

Status: Complete

**Tests**: No `tests/recommend/` exists. Mirror `tests/roadmap/` (subdir + `conftest.py` + `__init__.py`) if the cache is a `cli/recommend/` submodule, or a single `tests/cli/test_recommend_cache.py` if a flat module. YAML-roundtrip test template = `tests/roadmap/test_convergence.py::TestRegistryPersistence::test_save_and_reload` (`tmp_path`, save->reload). Atomic-write crash test template = `tests/cli/test_install_hooks.py::test_case_8_atomic_write_no_partial` (`patch(... .os.replace, side_effect=OSError)`). CLI-surface test template = `tests/cli/test_cli_registration.py` (CliRunner). NOTE: convergence.save() is JSON+fixed-tmp-name; prefer install_hooks' randomized-tmp atomic variant for YAML.

**Sync**: `make sync-dev` copies `src/superclaude/hooks/scripts/*.sh` -> `.claude/hooks/`. `make verify-sync` `=== Installer Registration ===` (Makefile 307-326) imports `_FRESHNESS_SCRIPTS` live and `comm`-diffs it against `src/.../scripts/*.sh` — so a new hook MUST be in BOTH places. verify-sync does NOT check `.gitignore`, settings.json PreToolUse, or `.claude/cache/`. SoT: edit `src/`, `make sync-dev`, `make verify-sync`; never stage `.claude/` EXCEPT `settings.json` and (new, user-authorized) `.claude/cache/*.yaml` + `eval-runs/**`.

**Registration**: (a) main.py bottom (lines 400-426) — `from ...recommend.commands import recommend_group` + `main.add_command(recommend_group, name="recommend")`; MUST add `"recommend"` to `EXPECTED_TOP_LEVEL_COMMANDS` (`tests/cli/test_cli_registration.py:31`). (b) New hook -> `src/superclaude/hooks/scripts/` + `_FRESHNESS_SCRIPTS` (install_hooks.py:43). (c) PreToolUse project hook registered in `.claude/settings.json` (lines 15-25 = sc-recommend-phase0 template, matcher `Skill`, `$CLAUDE_PROJECT_DIR/.claude/hooks/<x>.sh`), NOT hooks.json. settings.json is the one stageable `.claude/` file. Hook-script template = `sc-recommend-phase0.sh` (fail-open, stdin prefilter, jq gate, heredoc).

**Gitignore**: `.claude/cache/` is ignored at line 103 AND `.claude/` broad at line 117 (with `!.claude/settings.json` at 118). Add the R3 negation block IMMEDIATELY AFTER line 118 (after the broad ignore), ordered: `!.claude/cache/` first (dir re-include), then per-file/dir negations, then `.claude/cache/sc-recommend-events.jsonl` re-ignore LAST. The dir-negation-before-contents and re-ignore-last ordering is load-bearing per git parent-exclusion semantics.

**pyproject**: `pyyaml>=6.0` already present (line 38) — no dep change. `--strict-markers` set; ruff enforces `I`+`N` (sorted imports, PEP8 names) on `src/`; `anthropic` SDK globally banned (use `cli/eval/` subprocess harness for `--eval`).

### Cross-references for builder
- `Makefile:307-326` (Installer Registration gate), `Makefile:109-163` (sync-dev)
- `src/superclaude/cli/install_hooks.py:43-86` (_FRESHNESS_SCRIPTS)
- `src/superclaude/cli/main.py:404-426` (group registration pattern)
- `src/superclaude/cli/roadmap/convergence.py:304-317` (atomic save, JSON)
- `.claude/settings.json:15-25` (PreToolUse Skill-gate template)
- `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` (hook-script template)
- `.gitignore:101-118` (cache ignore + broad ignore + settings exception)
- `tests/cli/test_install_hooks.py:359-378` (atomic-write test), `tests/cli/test_cli_registration.py:31-79` (roster test), `tests/roadmap/test_convergence.py:219-247` (save/reload test), `tests/cli/test_verify_sync_hooks.py:92-170` (installer-registration mutation tests)
- `pyproject.toml:34-38` (deps), `:102-136` (pytest), `:178-211` (ruff)
