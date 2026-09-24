---
title: "Design: Native ccsession install and update"
status: draft
spec: .dev/specs/ccsession-native-install.md
feature_id: CCSESSION-NATIVE
type: component
created: 2026-09-24
branch: feature/ccsession-native-install
worktree: .dev/worktrees/ccsession-native-install
---

# Design: Native ccsession install and update

Implements [ccsession-native-install.md](./ccsession-native-install.md). No new CLI flags. No `settings.json` writes outside `install_hooks`.

## 1. Context

Today:

```
install/update --> install_all_skills  --> ~/.claude/skills/ccsession-tag/**
            \--> install_hooks         --> ~/.claude/hooks + settings.json
            \--> (nothing)             --> ~/.local/bin/ccsession
                                       --> ~/.claude/ccsession.env
                                       --> SessionStart for session-start.sh
```

`install.sh` still does the last three. Native install must do them without calling `install.sh` and without a second JSON merger.

## 2. Component diagram

```
                    superclaude install | update | ./update.sh
                                      |
        +-------------+---------------+----------------+
        v             v               v                v
   install_core  install_commands  install_agents  install_all_skills
                                                       |
                                                       v
                                              wire_ccsession()     NEW
                                              (no settings.json)
                                                       |
                                                       v
                                               install_hooks()
                                               (hooks.json + merge)
                                                       |
                       install only                    v
                                              install_templates
                                                       |
                                                       v
                                               doctor (update.sh)
```

`./update.sh` unchanged: it already runs `superclaude install --force`.

## 3. Module: `install_ccsession.py`

Path: `src/superclaude/cli/install_ccsession.py`

```
wire_ccsession(home: Path | None = None) -> tuple[bool, str]
```

`home` defaults to `Path.home()`. Tests pass a tmp path. No network. No JSON.

### 3.1 Owned paths (relative to `home`)

| Path | Action |
|------|--------|
| `.claude/skills/ccsession-tag` | must already exist (copied by `install_all_skills`); else fail |
| `.claude/skills/ccsession-tag/ccsession` | `chmod 0o755` |
| `.claude/skills/ccsession-tag/hooks/session-start.sh` | `chmod 0o755` |
| `.local/bin/ccsession` | managed symlink or collision (see 3.2) |
| `.claude/ccsession.env` | create from `ccsession.env.example` iff absent; `chmod 0o600`; never overwrite |

### 3.2 Symlink state machine

```
dest = home / ".local/bin/ccsession"
want = home / ".claude/skills/ccsession-tag/ccsession"

missing            -> mkdir -p dest.parent; dest.symlink_to(want)
symlink to want    -> dest.unlink(); dest.symlink_to(want)   # ln -sfn
symlink elsewhere  -> WARN, do not change, success=True (collision)
regular file       -> WARN, do not change, success=True (collision)
```

“Managed” = `dest.is_symlink()` and `dest.resolve() == want.resolve()`. Compare resolved paths so relative vs absolute links both count as owned.

Collision does not fail install (spec FR-3 / NFR-6 exception). Doctor reports it as a finding.

### 3.3 Env seed

Same pattern as `install_hooks._SEED_FILES`: copy only when destination is missing. If the example file is missing, fail (packaging bug). Do not chmod an existing env file (user ownership).

### 3.4 Return contract

Matches other installers: `(success: bool, message: str)`.

- Fail: skill dir missing, example missing, cannot create `.local/bin`, chmod/symlink OSError (other than collision).
- Success with warning text if collision.
- Message must not include env file contents (NFR-1).

## 4. Hook registration (single writer)

`wire_ccsession` does **not** touch `settings.json`.

Add one `SessionStart` registration to `src/superclaude/hooks/hooks.json`:

```json
{
  "matcher": "startup|resume",
  "hooks": [
    {
      "type": "command",
      "command": "~/.claude/skills/ccsession-tag/hooks/session-start.sh",
      "timeout": 5
    }
  ]
}
```

Same shape as existing SessionStart entries (tilde path, no `bash "..."` wrapper). The script already has `#!/bin/bash` and is chmod'd by `wire_ccsession`.

Do **not** copy the script into `hooks/scripts/` (avoids a second copy and a `verify-sync` `_FRESHNESS_SCRIPTS` entry). Skill dir remains source of truth.

### 4.1 install.sh leftover identity

`install.sh` registers:

```text
bash "/abs/home/.claude/skills/ccsession-tag/hooks/session-start.sh"
```

`install_hooks` currently owns by **exact** `command` string. That leftover would not match the tilde path, so a second SessionStart entry would be appended.

One helper, used in **both** `owns_existing` and the `remaining` filter (exact-string `in managed_commands` today would leave the leftover on `--force` replace). Match **only**:

1. the canonical command `~/.claude/skills/ccsession-tag/hooks/session-start.sh`
2. the `install.sh` leftover shape: `bash "` or `bash '` + absolute path ending in `ccsession-tag/hooks/session-start.sh` + matching quote

Do **not** match arbitrary substring (would steal a user hook that merely mentions the path). Do not generalize to other hooks.

On `--force`: replace leftover with the canonical tilde-path registration.

On install without `--force`: leftover counts as owned → skip add (no duplicate). Doctor accepts either shape. Next `update` canonicalizes.

## 5. Call sites

`src/superclaude/cli/main.py`

**install** — after `install_all_skills`, before `install_hooks`:

```
cc_success, cc_message = wire_ccsession()
```

Include `cc_success` in the existing `sys.exit(1)` conjunction.

**update** — same placement and conjunction. `update` has no templates step; wiring still runs.

**install-skill** — no wiring. Fallback remains `~/.claude/skills/ccsession-tag/install.sh`.

**install --list** — unchanged (no extra row). Doctor is the status surface.

`--target` still only affects slash commands. Wiring always uses `Path.home()`.

## 6. Sequence

### 6.1 Clean install

```
install --force=false
  install_all_skills        -> copies ccsession-tag
  wire_ccsession            -> chmod, symlink, seed env
  install_hooks             -> append SessionStart (canonical command)
```

### 6.2 Re-install, skill already present, symlink missing (G3)

```
install --force=false
  install_all_skills        -> skips ccsession-tag
  wire_ccsession            -> still runs; creates symlink; env untouched if present
  install_hooks             -> add SessionStart if not owned
```

Wiring is **not** gated on whether the skill was copied this run.

### 6.3 update.sh / superclaude update (G2)

```
install --force=true  OR  update (always force=True)
  install_all_skills(force=True) -> rmtree+copytree skill
  wire_ccsession                 -> retarget managed symlink; leave env
  install_hooks(force=True)      -> refresh/canonicalize SessionStart
```

Brief window while skill dir is rmtree'd: symlink may dangle. Wire runs after copy, so the window ends in the same process.

### 6.4 Collision (G4)

```
wire_ccsession -> warn, leave dest, success=True
install_hooks  -> still registers hook
doctor         -> passed=False on collision finding
```

## 7. Doctor

Add `_check_ccsession()` to `run_doctor` in `src/superclaude/cli/doctor.py`.

| Condition | `passed` | Details |
|-----------|----------|---------|
| skill dir or wrapper or hook script missing | False | missing path |
| env file missing | False | seed should exist |
| managed symlink missing | False | not wired |
| unmanaged collision at `.local/bin/ccsession` | False | collision |
| SessionStart command lacks `ccsession-tag/hooks/session-start.sh` | False | hook not registered |
| settings.json missing/malformed | False | cannot verify hook |
| `home/.local/bin` not on `PATH` | True | put the warning in `name` (doctor prints `details` only with `--verbose`; see `main.py` doctor loop) |
| env exists with example placeholders | True | not a failure |
| all owned artifacts present | True | do not print env contents |

Gateway reachability is out of scope.

## 8. Docs

`src/superclaude/skills/ccsession-tag/README.md`

- Primary: `superclaude install` or `./update.sh`
- Fallback: `./install.sh` from the skill folder (unchanged behavior)
- Remove “two-step `install-skill` then `install.sh`” as the default
- One line: macOS/Linux only (NFR-5)

Do not edit Coder #191 in this repo.

## 9. Tests

### 9.1 New: `tests/unit/test_install_ccsession.py`

Tmp `home`. Call `wire_ccsession(home=...)`.

| Test | Spec |
|------|------|
| creates symlink + env 0600 from example | FR-1 |
| leaves existing env bytes unchanged | FR-2 |
| wires when skill dir already present | FR-3 / G3 |
| refuses unmanaged file; dest unchanged | FR-3 / G4 |
| refuses unmanaged foreign symlink | FR-3 |
| retargets managed symlink | FR-2 |
| fails if skill dir missing | phase contract |
| does not create/modify `home/.claude/settings.json` | NFR-3 |
| captured message has no env contents | NFR-1 |
| creates `.local/bin` if missing | G5 |

### 9.2 Extend: `tests/cli/test_install_hooks.py`

- Canonical SessionStart command is merged
- Existing `bash "/.../ccsession-tag/hooks/session-start.sh"` is treated as owned; `--force` replaces with tilde path; without `--force` no duplicate

### 9.3 Extend: `tests/cli/test_update_command.py` and install orchestration

`_INSTALLERS` gains `superclaude.cli.install_ccsession.wire_ccsession` between skills and hooks. Order:

```
install_core_files
install_commands
install_agents
install_all_skills
wire_ccsession
install_hooks
```

Add the same stub-order test for `superclaude install` (today only `update` is asserted). Add `test_install_and_update_wire_failure_exit_nonzero` (NFR-6): stub `wire_ccsession` → `(False, "wire failed")`, expect exit 1. Stub every installer in `_INSTALLERS` so tests never touch real HOME.

### 9.4 Doctor — extend `tests/unit/test_cli_doctor.py`

`_check_ccsession(home=...)`. Cases: missing skill / symlink / hook / env → `passed is False`; collision → False; PATH warning in `name`, `passed is True`; placeholder env → True; details/name never contain env file bytes.

### 9.5 One tmp-HOME launcher check (spec §8.2)

`test_wire_symlink_runs_help`: after `wire_ccsession(home=tmp)`, `PATH=tmp/.local/bin`, run the symlink with `--help` (or `--list`). Fake `CLAUDE_BIN` if the wrapper execs claude. Do **not** add a separate `./update.sh` e2e; `install --force` is the inheritance path.

## 10. Files touched

| File | Change |
|------|--------|
| `src/superclaude/cli/install_ccsession.py` | new |
| `src/superclaude/cli/main.py` | call wire on install + update |
| `src/superclaude/cli/install_hooks.py` | script-path identity for ccsession hook |
| `src/superclaude/hooks/hooks.json` | SessionStart entry |
| `src/superclaude/cli/doctor.py` | `_check_ccsession` |
| `src/superclaude/skills/ccsession-tag/README.md` | primary vs fallback |
| `tests/unit/test_install_ccsession.py` | new |
| `tests/cli/test_install_hooks.py` | identity cases |
| `tests/cli/test_update_command.py` | call order |
| `update.sh` | none |
| `install.sh` | none (fallback) |

## 11. Non-goals (design)

- pipx console_script
- `--skip-ccsession`
- Wiring `superclaude install-skill ccsession-tag`
- Windows
- Gateway / shim / `lsof`
- Moving the hook script into `hooks/scripts/`

## 12. Implementation order

```
1. install_ccsession.wire_ccsession + unit tests
2. hooks.json entry + install_hooks identity helper + tests   [parallel with 1]
3. main.py install + update call sites + test_update_command
4. doctor check + tests
5. README
```

## 13. Validation vs spec

| FR | Design coverage |
|----|-----------------|
| FR-1 | §3 + §4 + §5 install |
| FR-2 | §3.3 env + §6.3 update; `update.sh` inherits |
| FR-3 | §3.2 collision; §6.2 skip-copy still wires; malformed JSON already refused by `install_hooks` |
| FR-4 | §7 |
| FR-5 | §8 |
| NFR-3 | `wire_ccsession` never opens settings.json |
| NFR-6 | §9.3 wire-failure CLI exit |
| G1 | §9.5 `--help` via symlink |

**Next:** `/sc:implement` against this design in `.dev/worktrees/ccsession-native-install`.
