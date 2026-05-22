# Research: Surface Verification
**Topic type:** File Inventory + Surface Verification
**Scope:** hooks.json, auggie-flag-clear.sh, Makefile verify-sync, install_hooks.py, src+claude hooks dirs
**Status:** Complete
**Date:** 2026-05-17
---

## Spec Claim 1: hooks.json:60 PostToolUse matcher

**[CODE-VERIFIED]** at `/config/workspace/IronClaude/src/superclaude/hooks/hooks.json:60`

Exact current content:
```json
        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
```

Surrounding context (lines 58-68):
```json
      {
        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/auggie-flag-clear.sh",
            "timeout": 1
          }
        ]
      }
```

File total: 96 lines.

**CORRECTION (post-QA-gate re-verification 2026-05-17):** The earlier assertion that "JSON matcher
is ALREADY at the target state" was **incorrect**. The current matcher contains TWO alternatives
(`mcp__auggie__.*` and `mcp__airis-mcp-gateway__auggie_.*`) but is **MISSING the third middle
alternative `mcp__auggie-mcp__.*`** that the release spec §4.1 mandates adding. The buggy state
shown above matches the spec's "before" diff. Independent verification:
`grep -c "mcp__auggie-mcp__" src/superclaude/hooks/hooks.json` → **0** (the prefix is absent).

**Part 2 patch IS required.** Spec §4.1 target:
```diff
- "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
+ "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",
```

Confusion source: `airis-mcp-gateway__auggie_` (the gateway-routed prefix, present) is a DIFFERENT
prefix from `mcp__auggie-mcp__` (the direct auggie-mcp server prefix, absent). Both must be in the
final matcher per spec §1.1 (the auggie-mcp MCP server installed in this project's SessionStart
registry emits the `mcp__auggie-mcp__*` prefix).

---

## Spec Claim 2: auggie-flag-clear.sh:22 case body

**[CODE-VERIFIED]** at `/config/workspace/IronClaude/src/superclaude/hooks/scripts/auggie-flag-clear.sh:22`

Exact current content (line 22):
```bash
    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
```

Surrounding context (lines 21-31):
```bash
case "$TOOL_NAME" in
    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
        STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
        if [ -f "$STICKY" ]; then
            rm -f "$STICKY" 2>/dev/null || true
            NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
            printf '{"ts":"%s","session_id":"%s","event":"sticky_cleared","tool":"%s"}\n' \
                "$NOW_ISO" "$SESSION_ID" "$TOOL_NAME" >> "$AUGGIE_LOG" 2>/dev/null || true
        fi
        ;;
esac
```

**CORRECTION (post-QA-gate re-verification 2026-05-17):** The earlier assertion that "case-glob
pattern is ALREADY at the target state" was **incorrect**. The current case body contains TWO
alternatives (`mcp__auggie__*` and `mcp__airis-mcp-gateway__auggie_*`) but is **MISSING the third
middle alternative `mcp__auggie-mcp__*`** that the release spec §4.2 mandates adding. Independent
verification: `grep -c "mcp__auggie-mcp__" src/superclaude/hooks/scripts/auggie-flag-clear.sh` →
**0** (the prefix is absent).

**Part 2 patch IS required.** Spec §4.2 target:
```diff
-    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
+    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)
```

Shell case uses globs (not regex) — `auggie_*` is the correct glob form (no `.` prefix). This
glob/regex distinction is also why Part 3's cross-consistency assertion normalizes both forms
before comparison (release-spec §5.1).

---

## Spec Claim 3: auggie-flag-clear.sh:2 header comment

**[CODE-VERIFIED]** at `/config/workspace/IronClaude/src/superclaude/hooks/scripts/auggie-flag-clear.sh:1-4`

Exact current text (lines 1-4):
```bash
#!/usr/bin/env bash
# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.
# auggie-first-hook-proposal-v2.1.md §6 — synchronous (no async:true) per spec-panel Wh-8.
# Fail-open per NFR-3.
```

Line 2 verbatim: `# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.`

File is 32 lines total, 1272 bytes, executable (rwxr-xr-x), mtime May 17 02:54.

**Part 2 patch IS required for line 2 header comment** (release-spec §4.2 lines 159-163). Target:
```diff
-# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.
+# PostToolUse: clear auggie-first sticky after any auggie-prefixed tool call
+# (mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*).
```

This expands line 2 into two lines (lines 2-3 of the post-patch file). The replacement enumerates
all three prefixes the matcher must cover, making the header self-documenting against future
prefix-set drift.

---

## Spec Claim 4: Makefile verify-sync iterates skills/agents/commands only, NO hooks

**[CODE-VERIFIED]** at `/config/workspace/IronClaude/Makefile:154-247`

The verify-sync target spans lines 154-247 (94 lines). Section structure confirmed by `echo`'d
banners:

- Line 158: `echo "=== Skills ==="` — iterates `src/superclaude/skills/*/` then `.claude/skills/*/`
- Line 190: `echo "=== Agents ==="` — iterates `src/superclaude/agents/*.md` then `.claude/agents/*.md`
- Line 216: `echo "=== Commands ==="` — iterates `src/superclaude/commands/*.md` then `.claude/commands/sc/*.md`
- Lines 241-247: drift footer

**No `=== Hooks ===` section exists. No iteration over `src/superclaude/hooks/scripts/` or
`.claude/hooks/`. Confirmed: verify-sync has NO hooks coverage.** Spec claim 4 verified.

Final closing lines for context (lines 242-247):
```makefile
		if [ "$$drift" -eq 0 ]; then \
			echo "✅ All components in sync."; \
		else \
			echo "❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/."; \
			exit 1; \
		fi
```

Note the indentation: every Makefile recipe line uses a leading TAB, and inside the multi-line
shell block lines use TAB + spaces. The new `=== Hooks ===`, `=== Installer Registration ===`,
and `=== Hooks Cross-Consistency ===` sections must follow the same conventions: TAB indent,
backslash line-continuations, `$$` for shell vars, `\` ; closers between commands.

---

## Spec Claim 5: auggie-bash-gate.sh exists in .claude/hooks/ but NOT in src/superclaude/hooks/scripts/

**[CODE-VERIFIED]** by `ls` of both directories.

### `src/superclaude/hooks/scripts/` (9 files, all .sh):
| File | Lines | Bytes | Mtime |
|------|-------|-------|-------|
| auggie-flag-clear.sh         |  32 |  1272 | May 17 02:54 |
| freshness-file-changed.sh    |  55 |  2317 | May 13 03:04 |
| freshness-post-read.sh       |  48 |  2015 | May 13 03:04 |
| freshness-pre-edit.sh        | 136 |  5138 | May 16 01:37 |
| freshness-session-start.sh   | 122 |  5014 | May 16 01:37 |
| freshness-subagent-start.sh  |  26 |   870 | May 13 03:04 |
| freshness-subagent-stop.sh   |  30 |   983 | May 13 03:04 |
| freshness-user-prompt.sh     | 266 | 10122 | May 16 01:37 |
| reject-workspace-writes.sh   |  39 |  2027 | May 16 01:37 |

**Total: 9 files, 754 lines.**

### `.claude/hooks/` (11 files, all .sh):
| File | Lines | Bytes | Mtime |
|------|-------|-------|-------|
| **auggie-bash-gate.sh**      |  61 |  2593 | May 17 17:58 |  ← ORPHAN
| auggie-flag-clear.sh         |  32 |  1272 | May 17 18:40 |
| freshness-file-changed.sh    |  55 |  2317 | May 17 18:40 |
| freshness-post-read.sh       |  48 |  2015 | May 17 18:40 |
| freshness-pre-edit.sh        | 136 |  5138 | May 17 18:40 |
| freshness-session-start.sh   | 122 |  5014 | May 17 18:40 |
| freshness-subagent-start.sh  |  26 |   870 | May 17 18:40 |
| freshness-subagent-stop.sh   |  30 |   983 | May 17 18:40 |
| freshness-user-prompt.sh     | 266 | 10122 | May 17 18:40 |
| reject-workspace-writes.sh   |  39 |  2027 | May 17 18:40 |
| session-init.sh              |  30 |   817 | May 17 18:40 |

**Total: 11 files, 845 lines.**

### Diff analysis:
- `auggie-bash-gate.sh` (61 lines, 2593 bytes) **exists in `.claude/hooks/` but NOT in
  `src/superclaude/hooks/scripts/`.** This is the **orphan** the spec calls out.
- `session-init.sh` (30 lines, 817 bytes) exists in `.claude/hooks/` but NOT in
  `src/superclaude/hooks/scripts/`. It IS present in `src/superclaude/scripts/` (legacy path
  per install_hooks.py:494-500 `_get_legacy_scripts_source()`), so this is NOT an orphan —
  it's a documented legacy-source script. The verify-sync update must whitelist it.

### Orphan content snapshot (so builder can craft "move to src/" diff):
`.claude/hooks/auggie-bash-gate.sh` is a PreToolUse Bash gate referencing `auggie-bash-gate-spec.md`.
Header lines 1-9:
```bash
#!/usr/bin/env bash
# PreToolUse on Bash: block a small set of actionable verbs when the
# auggie-first sticky is present and no env-var disable is set.
#
# Reads JSON tool-call payload on stdin. Exits 0 (allow) or 2 (block + stderr).
# Fail-open on any parse error per the v2.1 NFR-3 convention.
#
# See auggie-bash-gate-spec.md.
set -u
```

The orphan is referenced by NO entry in `src/superclaude/hooks/hooks.json` (hooks.json has no
PreToolUse Bash registration for auggie-bash-gate.sh — verified by reading the full hooks.json).
The script exists in `.claude/hooks/` but has no install pipeline path. **Resolution per spec:
copy `.claude/hooks/auggie-bash-gate.sh` → `src/superclaude/hooks/scripts/auggie-bash-gate.sh`,
then add to `_FRESHNESS_SCRIPTS` in install_hooks.py.**

---

## Spec Claim 6: install_hooks.py:43 _FRESHNESS_SCRIPTS, :178 iteration site

**[CODE-VERIFIED]** at `/config/workspace/IronClaude/src/superclaude/cli/install_hooks.py`

### Line 43 — list declaration start:
```python
_FRESHNESS_SCRIPTS = [
    "freshness-session-start.sh",          # line 44
    "freshness-user-prompt.sh",            # line 45
    "freshness-pre-edit.sh",               # line 46
    "freshness-post-read.sh",              # line 47
    "freshness-file-changed.sh",  # v1: NOT registered. Kept on disk for v1.5.  (line 48)
    "freshness-subagent-start.sh",         # line 49
    "freshness-subagent-stop.sh",          # line 50
    # auggie-first PostToolUse hook (auggie-first-hook-proposal-v2.1.md).
    # Not strictly a "freshness" hook by lineage, but lives in the same hooks/scripts/
    # directory and shares the install pipeline; kept here to avoid a second list.
    "auggie-flag-clear.sh",                # line 54
]
_LEGACY_SCRIPTS = ["session-init.sh"]      # line 56
```

The list ends at line 55 with `]`. Note: `reject-workspace-writes.sh` is present in
`src/superclaude/hooks/scripts/` but **NOT** listed in `_FRESHNESS_SCRIPTS` — it does not get
installed by `install_hooks()`. Spec should note this if it intends to install it. (Sibling
finding — may or may not be in scope.)

### Line 178 — iteration site:
```python
    # Build (source_path, dest_name) list
    sources: list[Tuple[Path, str]] = []
    for name in _FRESHNESS_SCRIPTS:                            # line 178
        sources.append((freshness_dir / name, name))           # line 179
    if legacy_dir is not None:                                 # line 180
        for name in _LEGACY_SCRIPTS:                           # line 181
            src = legacy_dir / name                            # line 182
            if src.exists():                                   # line 183
                sources.append((src, name))                    # line 184
```

The iteration is **at line 178**, inside `_copy_scripts()` (defined at line 165). Pattern:
each name in the list maps to `freshness_dir / name` where `freshness_dir = _get_hooks_scripts_source() = src/superclaude/hooks/scripts/`.

**To add `auggie-bash-gate.sh`: insert the string into `_FRESHNESS_SCRIPTS` (e.g., after
`"auggie-flag-clear.sh"` at line 54). The iteration site needs no change.**

---

## Summary of [CODE-VERIFIED] Claims

| # | Spec Claim | Status | Notes |
|---|------------|--------|-------|
| 1 | `hooks.json:60` matcher reads `"mcp__auggie__.*\|mcp__airis-mcp-gateway__auggie_.*"` (MISSING `mcp__auggie-mcp__.*`) | **[CODE-VERIFIED]** | Matches spec's BUGGY before-state. **Part 2 patch §4.1 REQUIRED** — add `mcp__auggie-mcp__.*` as middle alternative. |
| 2 | `auggie-flag-clear.sh:22` case body reads `mcp__auggie__*\|mcp__airis-mcp-gateway__auggie_*)` (MISSING `mcp__auggie-mcp__*`) | **[CODE-VERIFIED]** | Matches spec's BUGGY before-state. **Part 2 patch §4.2 REQUIRED** — add `mcp__auggie-mcp__*` as middle alternative. |
| 3 | `auggie-flag-clear.sh:2` header comment text | **[CODE-VERIFIED]** | Exact text: `# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.` **Part 2 patch §4.2 REQUIRED** — replace with 2-line form enumerating all 3 prefixes. |
| 4 | Makefile verify-sync (lines 154-247) has Skills/Agents/Commands sections, no Hooks | **[CODE-VERIFIED]** | 94-line target, banners at L158/L190/L216. **Part 1 + Part 3 sections to be inserted before L241.** |
| 5 | `.claude/hooks/auggie-bash-gate.sh` exists; `src/superclaude/hooks/scripts/auggie-bash-gate.sh` does NOT | **[CODE-VERIFIED]** | Orphan: 61 lines, 2593 bytes, mtime May 17 17:58. **Detection in scope (Part 1); resolution out of scope (user decision after merge — release-spec §6).** |
| 6 | `install_hooks.py:43` declares `_FRESHNESS_SCRIPTS` list; `:178` iterates it via `for name in _FRESHNESS_SCRIPTS:` | **[CODE-VERIFIED]** | List spans L43-L55 (8 entries); iteration at L178 inside `_copy_scripts()`. **Part 1's `=== Installer Registration ===` section asserts every src/hooks/scripts/*.sh appears in this list.** |

### Part 2 patch summary (all THREE diffs required, not zero)

| # | File | Line | Change |
|---|------|------|--------|
| P2.1 | `src/superclaude/hooks/hooks.json` | 60 | Add `mcp__auggie-mcp__.*\|` as middle alternative |
| P2.2 | `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 22 | Add `mcp__auggie-mcp__*\|` as middle alternative |
| P2.3 | `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | 2 | Expand to 2-line form enumerating all 3 prefixes |

After patches, `make sync-dev` propagates the .sh changes to `.claude/hooks/auggie-flag-clear.sh`.
The .json file is only read at install time (no .claude/hooks/ counterpart for the .json itself —
hooks.json is consumed by the installer which writes to `~/.claude/settings.json`).

## Additional findings (sibling context for builder)

- **Part 2 patches ARE required (release-spec §4.1 + §4.2).** The matcher at `hooks.json:60` and
  the case body at `auggie-flag-clear.sh:22` BOTH currently contain only `mcp__auggie__.*` and
  `mcp__airis-mcp-gateway__auggie_.*` — they are MISSING the `mcp__auggie-mcp__.*` middle
  alternative that the auggie-mcp MCP server (registered in SessionStart) actually emits. The
  header comment at `auggie-flag-clear.sh:2` must also be rewritten to enumerate all 3 prefixes.
  Independent grep verification: `grep -rn "mcp__auggie-mcp__" src/superclaude/hooks/` → **0
  hits**. Builder MUST apply all three Part 2 diffs verbatim per spec §4.1 / §4.2.
- **`reject-workspace-writes.sh` is in `src/superclaude/hooks/scripts/` but NOT in
  `_FRESHNESS_SCRIPTS`.** Likely intentional (it's an env-based PreToolUse hook registered via
  the project-local `.claude/settings.json`, not user-global). The new `=== Hooks ===` verify-sync
  section will flag it as a diff between src and .claude — both copies are identical (39 lines
  each, 2027 bytes) so a content-diff will pass, but a "must be in `_FRESHNESS_SCRIPTS`" check
  would fail. Spec author should clarify.
- **`session-init.sh` lives in `src/superclaude/scripts/` (NOT under hooks/scripts).** The new
  verify-sync Hooks section must NOT flag `session-init.sh` as orphan-in-.claude. The Makefile
  iteration logic needs whitelist handling or per-source-dir comparison.
- All `.claude/hooks/` files except `auggie-bash-gate.sh` have mtime `May 17 18:40` (same `make
  sync-dev` run), suggesting recent sync. The orphan's mtime (`May 17 17:58`) predates the sync —
  consistent with it being manually placed.

## File paths (absolute) for builder reference

- `/config/workspace/IronClaude/src/superclaude/hooks/hooks.json`
- `/config/workspace/IronClaude/src/superclaude/hooks/scripts/auggie-flag-clear.sh`
- `/config/workspace/IronClaude/.claude/hooks/auggie-bash-gate.sh` (orphan source)
- `/config/workspace/IronClaude/src/superclaude/hooks/scripts/auggie-bash-gate.sh` (orphan target — does NOT exist)
- `/config/workspace/IronClaude/src/superclaude/cli/install_hooks.py`
- `/config/workspace/IronClaude/Makefile` (verify-sync target: L154-L247)
