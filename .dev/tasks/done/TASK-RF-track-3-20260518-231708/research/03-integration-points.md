# Research Track 03 — Integration Points (Hook Registration + Sync Model)

**Task:** TASK-RF-track-3-20260518-231708
**Track:** 3 of 3 (FU-003 PRD-skill CWD-default output routing)
**Focus:** Plumbing a new/extended hook must thread through to ship via `superclaude install` and clear `make verify-sync`
**Status:** Complete
**Date:** 2026-05-18

---

## 1. `_FRESHNESS_SCRIPTS` Registry

**Location:** `/config/workspace/IronClaude/src/superclaude/cli/install_hooks.py:43-67`

**Format:** A Python `list[str]` of bare script basenames (no path components, no
metadata). Each string must match a `.sh` file living in
`src/superclaude/hooks/scripts/`.

```python
# src/superclaude/cli/install_hooks.py:43-67
_FRESHNESS_SCRIPTS = [
    "freshness-session-start.sh",
    "freshness-user-prompt.sh",
    "freshness-pre-edit.sh",
    "freshness-post-read.sh",
    "freshness-file-changed.sh",  # v1: NOT registered. Kept on disk for v1.5.
    "freshness-subagent-start.sh",
    "freshness-subagent-stop.sh",
    "auggie-flag-clear.sh",
    # ... (long project-local rationale comment) ...
    "reject-workspace-writes.sh",
]
_LEGACY_SCRIPTS = ["session-init.sh"]  # line 68
```

**What `superclaude install` does with it** (traced from `install_hooks()` at
`install_hooks.py:79-169`):

1. **STEP 1 — Copy scripts (`install_hooks.py:111-137`, `_copy_scripts` at
   `install_hooks.py:177-216`):** For each name in `_FRESHNESS_SCRIPTS`, builds
   `(freshness_dir / name, name)` source/dest tuples (line 189-191). Then
   `shutil.copy2(src, dest_file)` + `os.chmod(dest_file, 0o755)` per entry
   (`install_hooks.py:209-212`). A script that exists on disk but is **not** in
   this list is silently skipped — it never lands at `~/.claude/hooks/`.

2. **STEP 2 — Merge `hooks.json` registrations into `~/.claude/settings.json`**
   (`install_hooks.py:139-149`, `_merge_settings` at `install_hooks.py:224-407`):
   reads `src/superclaude/hooks/hooks.json` (resolved by `_get_hooks_source` at
   `install_hooks.py:453-457`), additively merges its `hooks.<Event>[]` arrays
   into the target settings.json, atomic write via tempfile + `os.replace`
   (line 423-439). Collision detection at `install_hooks.py:326-385`.

3. **STEP 3 — Deploy seed data files** (`install_hooks.py:151-165`,
   `_deploy_seed_files` at `install_hooks.py:472-503`): copies
   `auggie-projects.txt.example` → `auggie-projects.txt` skip-if-exists.

**Key invariants:**
- The list is consulted ONLY in `_copy_scripts`; the matcher/registration side
  is driven entirely by the contents of `src/superclaude/hooks/hooks.json`.
- A script in `_FRESHNESS_SCRIPTS` but absent from `hooks.json` → script lands
  on disk, but no event ever triggers it (dormant). This is the exact pattern
  used by `reject-workspace-writes.sh` (project-local registration only) and by
  `freshness-file-changed.sh` (v1 orphan, kept for v1.5).
- A script in `hooks.json` but absent from `_FRESHNESS_SCRIPTS` → registration
  added to settings.json, but script never deployed → broken hook (`bash:
  command not found`). This is the failure mode the `=== Installer Registration
  ===` check in `make verify-sync` protects against.

---

## 2. Sync Model End-to-End

**Edit happens in `src/`**, mirror gets refreshed by `make sync-dev`:

**Makefile `sync-dev` target — hook fan-out at `Makefile:137-147`:**

```makefile
@mkdir -p .claude/hooks
@for hook in src/superclaude/hooks/scripts/*.sh; do \
    [ -f "$$hook" ] || continue; \
    name=$$(basename "$$hook"); \
    cp "$$hook" ".claude/hooks/$$name"; \
    chmod +x ".claude/hooks/$$name"; \
done
@if [ -f src/superclaude/scripts/session-init.sh ]; then \
    cp src/superclaude/scripts/session-init.sh .claude/hooks/session-init.sh; \
    chmod +x .claude/hooks/session-init.sh; \
fi
```

**Sync chain (single hook, edit-to-deployed):**

```
src/superclaude/hooks/scripts/<hook>.sh          (canonical source-of-truth)
  │
  │  make sync-dev    (Makefile:137-143: bare `cp` + chmod +x; no rsync, no diff,
  │                    overwrites unconditionally)
  ▼
.claude/hooks/<hook>.sh                          (dev mirror, read by Claude Code in this repo)
  │
  │  superclaude install  (install_hooks.py:209-212: shutil.copy2 + chmod 0o755
  │                        from src/superclaude/hooks/scripts/, gated by _FRESHNESS_SCRIPTS)
  ▼
~/.claude/hooks/<hook>.sh                        (end-user install destination)
```

Note that `make sync-dev` reads directly from `src/superclaude/hooks/scripts/*.sh`
glob (`Makefile:138`) — it does **NOT** consult `_FRESHNESS_SCRIPTS`. So a new
`.sh` file dropped into `src/superclaude/hooks/scripts/` will sync to `.claude/`
in this repo even before being registered. End-user installs (`superclaude
install`) WILL skip it until it appears in `_FRESHNESS_SCRIPTS`. That asymmetry
is exactly what the verify-sync `=== Installer Registration ===` check exists to
catch.

**Registration mirror (`hooks.json` → settings.json):** Note `make sync-dev` does
**not** sync `hooks.json` — there is no `.claude/hooks/hooks.json` target. The
canonical `hooks.json` is read on-demand by `superclaude install` (via
`_get_hooks_source` at `install_hooks.py:453-457`). Project-local hooks live in
`.claude/settings.json` instead (see `/config/workspace/IronClaude/.claude/settings.json`).

---

## 3. `make verify-sync` Checks

The target is defined inline at **`Makefile:155-315`** — it is a single shell
script (no helper scripts under `src/superclaude/`; `grep -rln "verify.sync\|verify_sync"
Makefile src/superclaude/` confirms the verify-sync logic is entirely
Makefile-resident). Six banner-separated sections, `drift=1` poisons the exit
code, `exit 1` at line 314 if any section reported drift.

| § | Banner | Lines | What it checks | Catches missing PRD-hook? |
|---|---|---|---|---|
| 1 | `=== Skills ===` | 159-189 | `diff -rq` every `src/superclaude/skills/<X>/` ↔ `.claude/skills/<X>/`; bidirectional orphan detection. | No |
| 2 | `=== Agents ===` | 191-215 | `diff -q` every `src/superclaude/agents/*.md` ↔ `.claude/agents/*.md`; bidirectional. | No |
| 3 | `=== Commands ===` | 217-241 | `diff -q` every `src/superclaude/commands/*.md` ↔ `.claude/commands/sc/*.md`; bidirectional. | No |
| 4 | `=== Hooks ===` | 243-267 | `diff -q` every `src/superclaude/hooks/scripts/*.sh` ↔ `.claude/hooks/<same name>.sh`; reverse pass flags `.claude/hooks/*.sh` with no corresponding source (`session-init.sh` exempted, line 262). | **Yes — partially.** Catches "script in `src/` but `make sync-dev` not run". |
| 5 | `=== Installer Registration ===` | 269-288 | Computes `comm -23` of `ls src/superclaude/hooks/scripts/*.sh \| basename` vs `_FRESHNESS_SCRIPTS` (via `uv run python -c ...` at line 271). Reports two failure modes: **MISSING from `_FRESHNESS_SCRIPTS`** (line 274-278) and **STALE in `_FRESHNESS_SCRIPTS`** (line 280-284). | **Yes — this is the gate.** A new `prd-output-route.sh` added to `src/superclaude/hooks/scripts/` but not added to `_FRESHNESS_SCRIPTS` will trip this check. |
| 6 | `=== Hooks Cross-Consistency ===` | 290-308 | Reads matcher prefixes from `hooks.json` (line 291-295) via `jq` and case-body prefixes from `auggie-flag-clear.sh` (line 296-300); confirms the auggie prefix set agrees on both sides. Auggie-specific. | No (only checks auggie-flag-clear, not generic). |

**Concrete failure messages a missing PRD-hook registration would emit (Section
5, `Makefile:274-278`):**

```
  ❌ MISSING from _FRESHNESS_SCRIPTS: <hookname>.sh (end-user 'superclaude install' will skip it)
❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
```

(Note the closing instruction "Run `make sync-dev` to fix" is generic — for a
missing `_FRESHNESS_SCRIPTS` entry, sync-dev does NOT fix it; the fix is an
edit to `install_hooks.py`. Operator must read the specific section banner.)

---

## 4. PR-F `b63cbd7` Reference Diff

**Stat (from `git show b63cbd7 --stat`):**

```
.../backlog/auggie-first-required/CANCELLED.md     |  31 ++++++
.../auggie-bash-gate-archived-2026-05-18.sh        | 112 +++++++++++++++++++++
src/superclaude/cli/install_hooks.py               |  12 +++
tests/cli/test_verify_sync_hooks.py                |  14 ++-
4 files changed, 165 insertions(+), 4 deletions(-)
```

**Of those 4 files, the canonical OQ-3 registration template is a 2-file
template (the other two files relate to OQ-2 archival and test docstring
updates, not the registration mechanism per se):**

| File | Touch | Purpose |
|---|---|---|
| `src/superclaude/cli/install_hooks.py` | +12 lines | Added `"reject-workspace-writes.sh"` plus an 11-line block comment to `_FRESHNESS_SCRIPTS` (the actual registration). |
| `tests/cli/test_verify_sync_hooks.py` | +14/-4 lines | Updated V1 docstring NOTE — previously documented expected-failure, now passes. |

**The 12-line install_hooks.py hunk (verbatim from `git show b63cbd7 --
src/superclaude/cli/install_hooks.py`):**

```python
# Inserted after `"auggie-flag-clear.sh",` at install_hooks.py:54
    # Project-local workspace-write guard. Registered in the IronClaude
    # project's `<project>/.claude/settings.json` PreToolUse with command
    # `$CLAUDE_PROJECT_DIR/.claude/hooks/reject-workspace-writes.sh` — i.e.,
    # Claude Code resolves it relative to the project directory, NOT
    # `~/.claude/hooks/`. End-user installs that touch unrelated projects
    # therefore have no registration pointing at this script and it sits
    # dormant in their `~/.claude/hooks/` (harmless). It is listed here
    # because (a) the project ships a `.claude/hooks/reject-workspace-writes.sh`
    # mirror via `make sync-dev` and (b) the `=== Installer Registration ===`
    # check in `make verify-sync` requires every entry of
    # `src/superclaude/hooks/scripts/*.sh` to be a member of this list.
    "reject-workspace-writes.sh",
```

**What's NOT in b63cbd7 (because reject-workspace-writes.sh is
project-local-only):**

- No edit to `src/superclaude/hooks/hooks.json` — the script is NOT registered
  in the user-level settings.json template (it's a project-local hook,
  registered in `<project>/.claude/settings.json` instead).
- No edit to `src/superclaude/hooks/scripts/reject-workspace-writes.sh` — the
  script itself landed in an earlier PR (PR #49 / commit 5439ea1 or earlier);
  b63cbd7 is purely a registration-fix follow-up.
- No edit to `.claude/hooks/reject-workspace-writes.sh` — the mirror is
  regenerated by `make sync-dev`, not committed by hand.
- No edit to `Makefile` — the verify-sync logic and sync-dev fan-out already
  handled `.sh` files generically.

**Implication for FU-003:** If the PRD hook is also project-local-only (only
makes sense inside an IronClaude checkout), b63cbd7 is the exact template:
1 line in `_FRESHNESS_SCRIPTS` + 1 line in project `.claude/settings.json`. If
the PRD hook should fire for ALL end-user installs (regardless of project),
then `hooks.json` must also gain a registration.

---

## 5. Recommended Integration Steps for FU-003

**Pre-decision (Track 02 informs this):** If Option A from Track 02 is chosen
— **extending the existing `reject-workspace-writes.sh`** rather than adding a
new hook — then Steps 2–6 below are unnecessary; only the script body changes
in `src/`, plus `make sync-dev` to refresh the `.claude/` mirror. Skip to the
"Option A simplified flow" sub-section.

### Full plumbing (if a new hook script is added — Option B from Track 02)

**Decision tree first:**
- Q1: Should the hook fire for ALL end-user installs (any project), or only
  inside an IronClaude checkout?
  - **ALL installs** → register in `src/superclaude/hooks/hooks.json` (user-level
    template); end users get it via `superclaude install`'s settings.json merge.
  - **Project-local only** → register in `/config/workspace/IronClaude/.claude/settings.json`
    (this repo's settings); follows the `reject-workspace-writes.sh` pattern
    from b63cbd7.

**Ordered checklist:**

1. **Create the script body in src/** (canonical source-of-truth):
   `src/superclaude/hooks/scripts/<new-hook>.sh` with shebang `#!/usr/bin/env
   bash`, set -euo pipefail, and the hook logic. (Track 02 covers the body.)

2. **Decide event + matcher**, edit one of:
   - **User-level (all installs):** Append to `src/superclaude/hooks/hooks.json`
     under the appropriate event key (`PreToolUse` / `PostToolUse` / etc.) with
     `"command": "~/.claude/hooks/<new-hook>.sh"`. Matcher follows hooks.json
     conventions (e.g., `"Edit|Write"` for tool calls).
   - **Project-local:** Append to `/config/workspace/IronClaude/.claude/settings.json`
     under the event key with `"command":
     "$CLAUDE_PROJECT_DIR/.claude/hooks/<new-hook>.sh"`. **Note the
     `$CLAUDE_PROJECT_DIR` prefix** — this is the IronClaude convention for
     project-local hooks (see line 9 of current `.claude/settings.json`).

3. **Register in `_FRESHNESS_SCRIPTS`** (`install_hooks.py:43-67`): add
   `"<new-hook>.sh"` as a new list entry. Include a block comment explaining
   why the script is registered (especially if project-local-only — see the
   `reject-workspace-writes.sh` comment block at install_hooks.py:56-66 as the
   template).

4. **Run `make sync-dev`** to mirror the new script into `.claude/hooks/`. This
   step is what lets you locally test the hook before commit.

5. **Run `make verify-sync`** — must exit 0. Sections that will exercise the new
   hook:
   - `=== Hooks ===` (Makefile:243-267): confirms `src/` ↔ `.claude/` mirror
     matches.
   - `=== Installer Registration ===` (Makefile:269-288): confirms
     `_FRESHNESS_SCRIPTS` membership.

6. **Test:** add a unit test under `tests/cli/test_verify_sync_hooks.py`
   following the V1-V7 pattern; assert at minimum that the new entry survives a
   simulated `superclaude install` round-trip. Run `uv run pytest
   tests/cli/test_verify_sync_hooks.py -v` and confirm 7+ passes.

7. **Commit** with the four-file template stable across PR-F-style follow-ups:
   - `src/superclaude/hooks/scripts/<new-hook>.sh` (NEW)
   - `src/superclaude/cli/install_hooks.py` (+ N lines in `_FRESHNESS_SCRIPTS`)
   - One of: `src/superclaude/hooks/hooks.json` (user-level) OR
     `.claude/settings.json` (project-local)
   - `tests/cli/test_verify_sync_hooks.py` (new test case)

### Option A simplified flow (extending `reject-workspace-writes.sh`)

If Track 02 picks Option A, the plumbing collapses to:

1. Edit `src/superclaude/hooks/scripts/reject-workspace-writes.sh` (body
   changes only — covered by Track 02).
2. `make sync-dev` → `.claude/hooks/reject-workspace-writes.sh` refreshed.
3. `make verify-sync` → all six sections green (no registration delta, so
   `=== Installer Registration ===` and Section 4 still match).
4. No edits to `install_hooks.py`, no edits to `hooks.json`, no edits to
   `.claude/settings.json`. **Zero registration delta** — the cheapest path.

---

## Summary

- **`_FRESHNESS_SCRIPTS` lives at `install_hooks.py:43-67`** as a flat `list[str]` of bare script basenames. `superclaude install` iterates it in `_copy_scripts` (`install_hooks.py:177-216`) to deploy scripts to `~/.claude/hooks/`; the registration side is independent and driven by `hooks.json`.
- **Sync model:** `src/superclaude/hooks/scripts/*.sh` is canonical → `make sync-dev` (Makefile:137-143) cp's all `.sh` files into `.claude/hooks/` and chmod +x; end-user installs route through `_FRESHNESS_SCRIPTS`-gated copies inside `install_hooks()`. `make sync-dev` is glob-based; `superclaude install` is list-gated — the asymmetry is what makes `=== Installer Registration ===` necessary.
- **`make verify-sync` has 6 sections** (Makefile:155-315). The **`=== Installer Registration ===`** section (Makefile:269-288) is THE gate that catches a new script-in-`src/` that wasn't added to `_FRESHNESS_SCRIPTS`. The `=== Hooks ===` section (Makefile:243-267) catches stale `.claude/hooks/` mirrors. No helper scripts under `src/superclaude/`; verify-sync is Makefile-resident.
- **PR-F b63cbd7 reference template:** 4 files touched, of which the registration delta is just `+12 lines` to `install_hooks.py` (`_FRESHNESS_SCRIPTS` entry + comment) plus `+14/-4` to `tests/cli/test_verify_sync_hooks.py`. The `hooks.json` was NOT touched because `reject-workspace-writes.sh` is project-local-only; it's registered in this repo's `.claude/settings.json` instead.
- **FU-003 integration:** If Track 02 picks Option A (extend existing reject-workspace-writes.sh), zero registration plumbing — just script-body edit + `make sync-dev`. If Option B (new hook), follow the 7-step checklist; the b63cbd7 template covers Steps 3 + 6 + 7.

**End of research.**
