---
title: "Native ccsession install and update"
version: "1.0.0"
status: draft
feature_id: CCSESSION-NATIVE
parent_feature: null
spec_type: infrastructure
complexity_score: 0.45
complexity_class: MEDIUM
target_release: unscheduled
authors: [user, spec-panel]
created: 2026-09-24
sources:
  - https://github.com/IronbellyOrg/Coder/issues/191
  - src/superclaude/skills/ccsession-tag/install.sh
  - src/superclaude/cli/main.py
  - update.sh
quality_scores:
  clarity: 8.5
  completeness: 8.0
  testability: 8.5
  consistency: 8.5
  overall: 8.4
---

# Native ccsession install and update

## 1. Problem Statement

`ccsession` already ships inside IronClaude as the `ccsession-tag` skill, but it is not a native install component. `superclaude install` and `superclaude update` copy the skill directory and stop. The PATH wrapper, env seed, and SessionStart hook still require a second manual `install.sh` (documented in the skill README and in [Coder #191](https://github.com/IronbellyOrg/Coder/issues/191)). `./update.sh` never runs that wiring, so a user who updates IronClaude can get a refreshed skill folder with a stale or missing `ccsession` command.

The product goal: after `superclaude install` or `./update.sh`, `ccsession` is installed, configured for first use, and updated when IronClaude updates — the same class of component as skills, agents, and hooks.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| Install copies skills only (`install_all_skills`); no bin/env/hook wiring | `src/superclaude/cli/main.py` install/update | `ccsession` not on PATH after install |
| Skill README documents a two-step install | `src/superclaude/skills/ccsession-tag/README.md` | Native-component claim is false today |
| `update.sh` is `pipx install --force` + `superclaude install --force` + doctor | `update.sh` | Updates refresh the skill tree, not the launcher |
| Coder #191 still tells users to clone IronClaude and run `install.sh` | issue body | Duplicate installer, moving `HEAD`, not release-pinned |
| `install_hooks` already merges `~/.claude/settings.json`; `install.sh` has a second, weaker merger | `install_hooks.py` vs `install.sh` | Dual writers, `.bak` clobber, invalid JSON silently skipped |

### 1.2 Scope Boundary

**In scope**: IronClaude `superclaude install`, `superclaude update`, `./update.sh`, `superclaude doctor`, and docs so ccsession is wired as a first-class component (skill files + PATH command + env seed + SessionStart hook). Update refreshes packaged files without destroying user secrets.

**Out of scope**: Coder template provisioning, admin-map credential injection, LiteLLM gateway setup, the model shim's runtime behavior, `lsof` stand-ins, Windows, opt-in/opt-out flags, changing named-session semantics, writing real API keys, cloning a second repo.

Related but separate: Coder #191's workspace onboarding can consume this once IronClaude install is complete; it is not this spec.

## 2. Solution Overview

Reuse the existing skill copy. Add one native wiring step owned by the Python installer (not a second JSON merger):

1. Skill files continue to install via `install_all_skills` (`ccsession-tag` is not `sc-*`, so it already copies).
2. After skills install, wire ccsession: symlink `~/.local/bin/ccsession`, seed `~/.claude/ccsession.env` only if missing, chmod +x packaged scripts.
3. Register the SessionStart hook through `install_hooks` / `hooks.json` (single writer of `settings.json`).
4. `superclaude update` and `./update.sh` inherit the same path; no extra shell step.
5. `superclaude doctor` reports whether the launcher, skill, hook, and env seed are present (not whether a gateway works).

Keep `install.sh` as a standalone fallback for people who copy only the skill folder. Native install must not *require* it.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| How to wire | Python installer step + `hooks.json` | Call `install.sh` from `main.py` | One `settings.json` writer; `install.sh` merge is weaker and backs up to a single `.bak` |
| Env file | Seed-once, never overwrite (same pattern as `_SEED_FILES`) | Always refresh from example | File holds credentials |
| PATH binary | `ln -sfn` equivalent onto `~/.local/bin/ccsession` | Copy the script; pipx entry point | Matches today's install.sh; pipx entry point would duplicate the skill copy |
| Hook script location | Keep in skill dir; `hooks.json` command points at `~/.claude/skills/ccsession-tag/hooks/session-start.sh` | Move into `src/superclaude/hooks/scripts/` | Skill stays self-contained; fallback `install.sh` still works |
| Gateway | Not configured by install | Write `ccsession.env` from env vars | Install must succeed without LiteLLM; naming works without a gateway |
| Opt-out | None in v1 | `--skip-ccsession` | User asked for a native component, same as other skills |

### 2.2 Workflow / Data Flow

```
superclaude install / update / ./update.sh
  --> install_core
  --> install_commands
  --> install_agents
  --> install_all_skills          # copies ccsession-tag (N files)
  --> wire_ccsession              # symlink 1, env 0|1, chmod
  --> install_hooks               # merges SessionStart for session-start.sh
  --> (install only) templates
  --> doctor (update.sh only)

Count notes:
  skill copy N --> wiring always 1 symlink target
  env created 0 if exists, 1 if missing   (N != M is expected)
  hook added 0 if already owned, 1 if new (N != M is expected)
  Consumer `ccsession` on PATH must not assume env was created this run
```

## 3. Functional Requirements

### FR-1: Install wires ccsession

**Description**: `superclaude install` (with or without `--force`) leaves a working `ccsession` launcher after a successful run, without the user running `install.sh` or cloning the repo.

**Acceptance Criteria**:

- [ ] After install into a clean home, `~/.claude/skills/ccsession-tag/SKILL.md` exists
- [ ] `~/.local/bin/ccsession` is a symlink to `~/.claude/skills/ccsession-tag/ccsession`
- [ ] that target is executable
- [ ] `~/.claude/ccsession.env` exists with mode `0600` (created from `ccsession.env.example` if it did not exist)
- [ ] `~/.claude/settings.json` SessionStart includes a command referencing `ccsession-tag/hooks/session-start.sh`
- [ ] install does not print or write API keys
- [ ] install succeeds if no LiteLLM gateway is configured

**Dependencies**: `install_all_skills`, `install_hooks`

### FR-2: Update refreshes packaged files, not secrets

**Description**: `superclaude update` and `./update.sh` refresh the skill tree, symlink, and hook registration to the packaged version. They never overwrite an existing `~/.claude/ccsession.env`.

**Acceptance Criteria**:

- [ ] `./update.sh` does not gain a new ad-hoc `install.sh` call; it inherits wiring from `superclaude install --force`
- [ ] `superclaude update` runs the same wiring as install
- [ ] an existing env file is byte-identical after update
- [ ] skill files (wrapper, proxy, hook script, SKILL.md) match the installed package after update
- [ ] symlink is re-pointed with `ln -sfn` semantics if it was missing or pointed elsewhere under installer ownership

**Dependencies**: FR-1

### FR-3: Idempotence and ownership

**Description**: Re-running install/update is safe. User Claude settings that are not the ccsession SessionStart command are preserved. Installer-owned symlink is refreshed; unmanaged collisions are not silently destroyed.

**Acceptance Criteria**:

- [ ] second install with `--force` succeeds and still satisfies FR-1
- [ ] second install without `--force` still ensures symlink + hook + env seed (wiring is not skipped just because the skill dir already exists)
- [ ] if `~/.local/bin/ccsession` is a regular file or a symlink to a path outside the managed skill dir, install does not overwrite it; it warns and continues; doctor reports the collision
- [ ] malformed `settings.json` fails `install_hooks` with an explicit error (no silent skip, no `.bak` clobber of the install_hooks backup scheme)

**Dependencies**: FR-1, existing `install_hooks` refuse-malformed behavior

### FR-4: Doctor reports native status

**Description**: `superclaude doctor` reports ccsession as a native component: skill present, launcher resolvable, hook registered, env file present. Gateway reachability is not a doctor failure.

**Acceptance Criteria**:

- [ ] missing skill dir, missing managed symlink, or missing hook is a doctor finding
- [ ] missing env file is a doctor finding (seed should have been created)
- [ ] empty/unedited example values in env are not a failure
- [ ] `~/.local/bin` absent from `PATH` is a warning, not an install failure
- [ ] doctor never prints env file contents

**Dependencies**: FR-1

### FR-5: Docs and fallback

**Description**: User-facing install docs describe ccsession as installed by `superclaude install` / `./update.sh`. The skill README two-step flow is demoted to a fallback for copying the skill folder alone.

**Acceptance Criteria**:

- [ ] skill README primary path is `superclaude install` (or `update.sh` in a checkout)
- [ ] Coder-facing clone-and-run-install.sh is not the IronClaude documented path
- [ ] `install.sh` remains and remains idempotent for fallback use

**Dependencies**: FR-1

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|--------------|
| `src/superclaude/cli/install_ccsession.py` | Wire symlink, env seed, chmod; no settings.json writes | pathlib, os |
| `tests/unit/test_install_ccsession.py` | Isolated wiring tests against tmp HOME | existing pytest |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/cli/main.py` | Call wiring after skills on `install` and `update` | Entry points named by the user |
| `src/superclaude/hooks/hooks.json` | Add SessionStart matcher `startup\|resume` command to the skill hook path | Single writer |
| `src/superclaude/cli/doctor.py` | Component checks in FR-4 | Native status is observable |
| `src/superclaude/skills/ccsession-tag/README.md` | Primary vs fallback install | Docs match behavior |
| `tests/unit/test_cli_install.py` (or equivalent) | Install/update include wiring | Regression |

`update.sh` is unchanged if `superclaude install --force` wires ccsession.

### 4.3 Removed Files

None. Keep `install.sh`.

### 4.4 Module Dependency Graph

```
main.install / main.update
  -> install_all_skills (existing)
  -> install_ccsession.wire()     # NEW; no settings.json
  -> install_hooks (existing + hooks.json entry)
doctor
  -> inspect skill, symlink, hook, env presence
```

### 4.5 Data Models

No new persisted schema. Owned paths:

| Path | Owner | Create | Update --force | Never |
|------|-------|--------|----------------|-------|
| `~/.claude/skills/ccsession-tag/**` | installer | copy | replace | user secrets |
| `~/.local/bin/ccsession` | installer if managed | symlink | retarget | overwrite unmanaged file |
| `~/.claude/ccsession.env` | user | seed from example | leave | overwrite |
| SessionStart command for `session-start.sh` | installer | merge | refresh by command identity | other hooks |

### 4.6 Implementation Order

```
1. install_ccsession.wire() + unit tests     -- no settings.json; smallest seam
2. hooks.json SessionStart entry             -- parallel with 1
3. main.py install + update call site        -- depends on 1
4. doctor checks                             -- depends on 3
5. README                                    -- depends on 3
6. keep install.sh compatible                -- fallback still skip-copy when source==target
```

## 5. Interface Contracts

### 5.1 CLI Surface

No new commands or flags.

```
superclaude install
superclaude install --force
superclaude update
./update.sh
superclaude doctor
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| (none new) | | | Wiring always runs; not gated on `--force` of the skill copy |

`--target` continues to affect slash-command destination only. ccsession wiring is user-global (`~/.claude`, `~/.local/bin`).

### 5.3 Phase Contracts

```yaml
wire_ccsession:
  inputs:
    skill_dir: ~/.claude/skills/ccsession-tag
  outputs:
    symlink: ~/.local/bin/ccsession
    env: ~/.claude/ccsession.env   # created iff absent
  must_not:
    - write settings.json
    - overwrite existing env
    - require network
    - require lsof
  on_missing_skill_dir: fail this step (install already failed to copy the skill)
```

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Credentials never in logs, git, or doctor output | zero secret bytes | tests assert env contents not in captured stdout |
| NFR-2 | Install/update work offline | no network calls in wiring | unit tests with no socket |
| NFR-3 | settings.json has one writer | only `install_hooks` | grep: `install_ccsession.py` does not load JSON settings |
| NFR-4 | Idempotent | 2× install == 1× install for owned paths | tmp-HOME test |
| NFR-5 | macOS/Linux only | documented | no Windows path in this spec |
| NFR-6 | Failure of wiring fails install/update (except unmanaged-symlink warning) | non-zero exit | CLI test |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dual settings.json writers if someone still calls install.sh after native install | med | med | Idempotent hook detection by script path; document fallback as optional |
| Unmanaged `~/.local/bin/ccsession` collision | low | med | warn, do not overwrite, doctor finding |
| `--force` skill rmtree briefly breaks symlink target | low | low | retarget after copy; same dest path |
| Coder templates keep cloning HEAD | med | low | this spec does not change Coder; README stops recommending clone |
| PATH missing `~/.local/bin` | med | low | doctor warning; install still succeeds |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_wire_creates_symlink_and_env` | `tests/unit/test_install_ccsession.py` | FR-1 |
| `test_wire_leaves_existing_env` | same | FR-2 |
| `test_wire_refreshes_after_skill_already_present` | same | FR-3 skip-skill still wires |
| `test_wire_refuses_unmanaged_binary` | same | FR-3 collision |
| `test_wire_does_not_touch_settings_json` | same | NFR-3 |
| `test_hooks_json_registers_session_start` | existing hooks install tests | FR-1 hook |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `superclaude install` against tmp HOME then `ccsession --help` via the symlink | FR-1 |
| `superclaude update` after a mutated skill file restores packaged wrapper | FR-2 |
| doctor flags missing symlink | FR-4 |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| Clean machine | `./update.sh` or `superclaude install` | `ccsession --list` runs; no `install.sh` |
| Existing env | edit env, update | env unchanged; skill files new |
| No gateway | install, `ccsession testname` without `--shim` | naming works; shim not required |

## 9. Migration & Rollout

- **Breaking changes**: no. Additive wiring. Existing two-step users keep working.
- **Backwards compatibility**: `install.sh` stays. Users with a hand-written env are preserved. Users with an unmanaged `ccsession` binary are warned, not overwritten.
- **Rollback plan**: remove `~/.local/bin/ccsession` and the SessionStart registration; skill dir can remain. No data migration.

## 10. Downstream Inputs

- `/sc:design` or `/sc:implement` for the wiring module.
- `/sc:roadmap` can consume this spec as `spec_type: infrastructure`.
- Coder #191 should switch from clone-and-install.sh to "IronClaude install includes ccsession" once this ships — not in this repo.

## 11. Examples

### Given / When / Then

**G1. Clean install**
Given a home with no `~/.claude` and `~/.local/bin` on PATH
When the user runs `superclaude install`
Then `ccsession --help` works and `~/.claude/ccsession.env` exists and no gateway was required

**G2. Update preserves secrets**
Given an existing `ccsession.env` containing a token
When the user runs `./update.sh`
Then the env file is unchanged and the skill files match the new package

**G3. Skill already copied, wiring missing**
Given `~/.claude/skills/ccsession-tag` exists and `~/.local/bin/ccsession` does not
When the user runs `superclaude install` without `--force`
Then the symlink and hook are still created

**G4. Unmanaged collision**
Given `~/.local/bin/ccsession` is a regular file
When the user runs `superclaude install`
Then that file is unchanged, install warns, doctor reports collision

**G5. Degenerate empty HOME dirs**
Given `HOME` is writable but `~/.local/bin` does not exist
When wiring runs
Then the directory is created and the symlink is placed
