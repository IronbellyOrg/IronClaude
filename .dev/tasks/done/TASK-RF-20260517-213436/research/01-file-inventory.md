# Research: File Inventory — hook-sync-and-matcher-fix
**Topic type:** File Inventory
**Scope:** All files modified or created by the release; reference files for context
**Status:** Complete
**Date:** 2026-05-17
**Verified against:** HEAD (per session context); all line numbers confirmed via `Read`/`wc -l`/`grep -n` on disk at investigation time.

---

## 1. Files to MODIFY

### 1.1 `Makefile` (project root)
- **Path:** `/config/workspace/IronClaude/Makefile`
- **Purpose:** Make targets driving install, test, sync, and verification workflows.
- **Current line count:** 415 lines (`wc -l` -> 415)
- **Relevant targets (line anchors):**
  - Line 1 — `.PHONY: install test test-plugin doctor verify clean lint format build-plugin sync-plugin-repo sync-dev verify-sync lint-architecture eval-skill uninstall-legacy help`
  - Line 108 — `sync-dev:` target start (already handles hooks at lines 136–146; this is reference only — NOT modified by this release)
  - Line 154 — `verify-sync:` target start (THIS is what gets extended)
  - Line 155 — `@echo "Verifying src/superclaude/ <-> .claude/ sync..."`
  - Line 156 — `@drift=0; \`
  - Line 158 — `echo "=== Skills ===";`
  - Line 190 — `echo "=== Agents ===";`
  - Line 216 — `echo "=== Commands ===";`
  - Line 240 — `done; \` (closing the orphan-check for-loop under Commands)
  - Line 241 — `echo ""; \` (last blank echo before final summary)
  - Line 242 — `if [ "$$drift" -eq 0 ]; then \`
  - Line 243 — `echo "✅ All components in sync."; \`
  - Line 244 — `else \`
  - Line 245 — `echo "❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/."; \`
  - Line 246 — `exit 1; \`
  - Line 247 — `fi`
  - Line 248 — blank line
  - Line 249 — `lint-architecture:` (boundary marker after the verify-sync target ends)

**Insertion anchor for new `=== Hooks ===` / `=== Installer Registration ===` / `=== Hooks Cross-Consistency ===` sections:**
- Insert AFTER line 240 (`done; \` — the closing `done` of the `=== Commands ===` orphan loop)
- Insert BEFORE line 241 (`echo ""; \` — last blank-echo before final summary)
- I.e., the new section blocks go between the close of the Commands section and the final `if drift -eq 0` check.
- The pattern to mirror per existing sections is `echo ""; \\` + `echo "=== <Name> ==="; \\` + body loop + `done; \\`.

**Exact current lines bracketing insertion point (verbatim from Read, disk-verified 2026-05-17):**
```
239			fi; \
240		done; \
241		echo ""; \
242		if [ "$$drift" -eq 0 ]; then \
```
(Note: line 239 inside the for-loop is `fi; \` closing the inner if; line 240 is `done; \` closing the orphan-check for loop; line 241 is the blank echo; line 242 starts the final summary block.)

**Imports / dependencies on other project files:**
- `Makefile` references no Python modules from `superclaude.cli.install_hooks` directly.
- It DOES reference paths: `src/superclaude/hooks/scripts/*.sh`, `src/superclaude/scripts/session-init.sh`, `.claude/hooks/`.
- The new `=== Installer Registration ===` section will need to read `_FRESHNESS_SCRIPTS` and `_LEGACY_SCRIPTS` from `src/superclaude/cli/install_hooks.py`. Per design-spec, this should be done via a small Python one-liner (e.g., `python -c "from superclaude.cli.install_hooks import _FRESHNESS_SCRIPTS, _LEGACY_SCRIPTS; ..."`) or by parsing the Python source with grep. (Researcher-02 covers convention choice.)

---

### 1.2 `src/superclaude/hooks/hooks.json`
- **Path:** `/config/workspace/IronClaude/src/superclaude/hooks/hooks.json`
- **Purpose:** Source-of-truth hook registrations merged into `~/.claude/settings.json` by `install_hooks.py`.
- **Current line count:** 95 lines
- **The line to be modified (Part 2 of release):**
  - **Line 60 (verbatim):** `        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",`
  - This is inside the `PostToolUse` array (lines 47–69), in the registration block that points to `auggie-flag-clear.sh` (line 64).
- **Target replacement (per release-spec):** Add `mcp__auggie-mcp__.*` to the alternation, yielding:
  `"matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",`
- **Surrounding context (verbatim, lines 58–67):**
```
        ]
      },
      {
        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/auggie-flag-clear.sh",
            "timeout": 1
          }
```
- **Imports / dependencies:** Pure JSON; no imports. Consumed by `src/superclaude/cli/install_hooks.py` (`_merge_settings`, line 212).

---

### 1.3 `src/superclaude/hooks/scripts/auggie-flag-clear.sh`
- **Path:** `/config/workspace/IronClaude/src/superclaude/hooks/scripts/auggie-flag-clear.sh`
- **Purpose:** PostToolUse hook that clears the auggie-first sticky after any `mcp__auggie__*` tool call.
- **Current line count:** 32 lines
- **The line to be modified (Part 2 of release):**
  - **Line 22 (verbatim):** `    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)`
  - This is the shell `case` pattern at line 22 inside the `case "$TOOL_NAME" in ... esac` block (lines 21–31).
- **Target replacement (per release-spec):** Add `mcp__auggie-mcp__*` to the pattern, yielding:
  `    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)`
- **Comment line at line 2 (also potentially updated for accuracy):**
  - **Line 2 (verbatim):** `# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.`
  - Release-spec calls for widening this comment to reflect the new prefix (e.g., "after any mcp__auggie__*/mcp__auggie-mcp__* tool call").
- **Surrounding context (verbatim, lines 20–31):**
```
# Sentinel guard: never operate on the "unknown" bucket (collision risk per Wh-1/Wh-6).
[ "$SESSION_ID" = "unknown" ] && exit 0
[ -z "$SESSION_ID" ] && exit 0

case "$TOOL_NAME" in
    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
        STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
        if [ -f "$STICKY" ]; then
            rm -f "$STICKY" 2>/dev/null || true
            NOW_ISO=$(date -Iseconds 2>/dev/null || date "+%Y-%m-%dT%H:%M:%S")
            printf '{"ts":"%s","session_id":"%s","event":"sticky_cleared","tool":"%s"}\n' \
```
- **Imports / dependencies (sourced):** No `source` directives. The script uses external commands: `jq`, `date`, `cat`, `printf`, `rm`. Env vars: `AUGGIE_FIRST_DISABLE`, `HOME`.
- **Fail-open semantics:** `set -u` only (no `set -e`). Per line 4 comment: "Fail-open per NFR-3."

---

## 2. Files to CREATE

### 2.1 `tests/cli/test_verify_sync_hooks.py`
- **Target path:** `/config/workspace/IronClaude/tests/cli/test_verify_sync_hooks.py`
- **Status:** Does NOT currently exist; verified via Bash (`ls tests/cli/` returns only `prd/`, `__pycache__/`, `test_install_hooks.py`, `test_tdd_extract_prompt.py`).
- **Note:** `tests/cli/__init__.py` does NOT exist. The directory is a pytest discovery dir without an `__init__.py` — sibling tests rely on pytest's rootdir auto-detection. Confirmed: `ls tests/cli/__init__.py` -> "No such file or directory".
- **Convention to follow:** Sibling `tests/cli/test_install_hooks.py` (465 lines) — researcher-03 covers details; this file should follow the same subprocess-driven pattern for invoking `make verify-sync` and reading exit codes / stdout.
- **Estimated LOC:** ~120 LOC for 7 scenarios (V1–V7), based on similar subprocess test files in the codebase.
- **V1-V7 scenario semantics:** see release-spec.md §9 and
  research-03 §7. Research-01 does not enumerate scenarios — the
  authoritative mapping lives in those two files.

---

## 3. REFERENCE files (read-only context for builder)

### 3.1 `src/superclaude/cli/install_hooks.py`
- **Path:** `/config/workspace/IronClaude/src/superclaude/cli/install_hooks.py`
- **Purpose:** Installs hook scripts to `~/.claude/hooks/` and merges hook registrations into `~/.claude/settings.json` via additive atomic merge.
- **Current line count:** 515 lines
- **Key symbols for cross-consistency check:**
  - **`_FRESHNESS_SCRIPTS` (lines 43–55), verbatim:**
    ```python
    _FRESHNESS_SCRIPTS = [
        "freshness-session-start.sh",
        "freshness-user-prompt.sh",
        "freshness-pre-edit.sh",
        "freshness-post-read.sh",
        "freshness-file-changed.sh",  # v1: NOT registered. Kept on disk for v1.5.
        "freshness-subagent-start.sh",
        "freshness-subagent-stop.sh",
        # auggie-first PostToolUse hook (auggie-first-hook-proposal-v2.1.md).
        # Not strictly a "freshness" hook by lineage, but lives in the same hooks/scripts/
        # directory and shares the install pipeline; kept here to avoid a second list.
        "auggie-flag-clear.sh",
    ]
    ```
    -> 8 entries total.
  - **`_LEGACY_SCRIPTS` (line 56), verbatim:**
    ```python
    _LEGACY_SCRIPTS = ["session-init.sh"]
    ```
    -> 1 entry.
- **`_SEED_FILES` (lines 62–64):** `[("auggie-projects.txt.example", "auggie-projects.txt")]` — not relevant to this release but useful context for "what install_hooks deploys."
- **Source-path resolvers:** `_get_hooks_source()` (line 441), `_get_hooks_scripts_source()` (line 448), `_get_legacy_scripts_source()` (line 494).

### 3.2 Hook scripts in `src/superclaude/hooks/scripts/` (9 files)
Confirmed via `ls -la`:
1. `auggie-flag-clear.sh` (1272 bytes)
2. `freshness-file-changed.sh` (2317 bytes)
3. `freshness-post-read.sh` (2015 bytes)
4. `freshness-pre-edit.sh` (5138 bytes)
5. `freshness-session-start.sh` (5014 bytes)
6. `freshness-subagent-start.sh` (870 bytes)
7. `freshness-subagent-stop.sh` (983 bytes)
8. `freshness-user-prompt.sh` (10122 bytes)
9. `reject-workspace-writes.sh` (2027 bytes) — **NOT in `_FRESHNESS_SCRIPTS` and NOT in `_LEGACY_SCRIPTS`** — installer does NOT deploy this script. It exists in `src/` but is not registered for installation.

### 3.3 Hook scripts in `.claude/hooks/` (11 files)
Confirmed via `ls -la`:
1. `auggie-bash-gate.sh` (2593 bytes) — **ORPHAN: NOT in `src/superclaude/hooks/scripts/`** — confirmed missing from src; the orphan flagged in the release spec.
2. `auggie-flag-clear.sh` (1272 bytes) — matches src
3. `freshness-file-changed.sh` (2317 bytes) — matches src
4. `freshness-post-read.sh` (2015 bytes) — matches src
5. `freshness-pre-edit.sh` (5138 bytes) — matches src
6. `freshness-session-start.sh` (5014 bytes) — matches src
7. `freshness-subagent-start.sh` (870 bytes) — matches src
8. `freshness-subagent-stop.sh` (983 bytes) — matches src
9. `freshness-user-prompt.sh` (10122 bytes) — matches src
10. `reject-workspace-writes.sh` (2027 bytes) — matches src (but not in `_FRESHNESS_SCRIPTS`!)
11. `session-init.sh` (817 bytes) — sourced from `src/superclaude/scripts/session-init.sh` per `_LEGACY_SCRIPTS` + Makefile lines 143–146.

**Cross-cutting orphan summary (critical for V2/V3 test scenarios):**
- `.claude/hooks/auggie-bash-gate.sh` — orphan in `.claude/`, no `src/` counterpart. Will be flagged by new `=== Hooks ===` section's "missing in src" check.
- `src/superclaude/hooks/scripts/reject-workspace-writes.sh` — IS in `src/` AND in `.claude/`, but NOT in `_FRESHNESS_SCRIPTS`/`_LEGACY_SCRIPTS`. Will be flagged by new `=== Installer Registration ===` section as on-disk but absent from installer manifest.

### 3.4 `src/superclaude/scripts/session-init.sh`
- Confirmed present at `/config/workspace/IronClaude/src/superclaude/scripts/session-init.sh`. Contents match `.claude/hooks/session-init.sh` (verified via `diff -q`).
- This is the only legacy script and is handled separately from `src/superclaude/hooks/scripts/` by both Makefile (line 143) and `install_hooks.py` (via `_get_legacy_scripts_source()` line 494).

### 3.5 Test reference files (deferred to researcher-03)
- `/config/workspace/IronClaude/tests/hooks/test_auggie_first.py` — 123 lines.
- `/config/workspace/IronClaude/tests/cli/test_install_hooks.py` — 465 lines.
- `/config/workspace/IronClaude/tests/cli/__init__.py` — DOES NOT EXIST (no init in tests/cli/).
- `/config/workspace/IronClaude/tests/hooks/__init__.py` — DOES EXIST (empty marker).

---

## 4. Summary Table

| Path | Action | Key anchors | Size delta est. |
|---|---|---|---|
| `Makefile` | MODIFY | Insert 3 sections between line 240 (`done; \\`) and line 241 (`echo ""; \\`) | +~80 LOC |
| `src/superclaude/hooks/hooks.json` | MODIFY | Line 60 matcher widening | +0 LOC (replace string in place) |
| `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | MODIFY | Line 22 case pattern; line 2 comment | +0 LOC (string widening) |
| `tests/cli/test_verify_sync_hooks.py` | CREATE | New file, mirror `test_install_hooks.py` pattern | +~120 LOC |
| `src/superclaude/cli/install_hooks.py` | REFERENCE | `_FRESHNESS_SCRIPTS` lines 43–55, `_LEGACY_SCRIPTS` line 56 | n/a |
| `src/superclaude/hooks/scripts/*.sh` (9 files) | REFERENCE | Inventory; `reject-workspace-writes.sh` is an installer-orphan | n/a |
| `.claude/hooks/*.sh` (11 files) | REFERENCE | `auggie-bash-gate.sh` is a sync-orphan (confirmed) | n/a |
| `src/superclaude/scripts/session-init.sh` | REFERENCE | Legacy single-script path | n/a |

**Total surface estimate:** ~200 LOC across 4 files (release-spec said ~155 LOC; my estimate is ~45 LOC higher mainly because the cross-consistency `=== Hooks Cross-Consistency ===` Makefile section needs a comparator block + the test file scenarios V1–V7 are each ~15 LOC of subprocess+assert).

---

## 5. Critical Findings for Task Builder

1. **No `tests/cli/__init__.py` exists** — the new test file must not assume package init. Use `conftest.py` patterns if needed (researcher-03 covers).
2. **`reject-workspace-writes.sh` is an installer-orphan**: present in `src/` and `.claude/` but NOT in `_FRESHNESS_SCRIPTS`. The new `=== Installer Registration ===` section will flag this on first run, which may be intentional (good — exposes existing drift) or require pre-cleanup. Builder should call this out as a follow-up consideration.
3. **`auggie-bash-gate.sh` is a confirmed sync-orphan** in `.claude/` only — this is the test fixture the release-spec mentions. The new `=== Hooks ===` section's "missing in src" check will catch it on first run.
4. **Makefile insertion point is unambiguous**: between line 240 (closing `done; \`) and line 241 (`echo "";`). Pattern to follow: same `echo "=== Name ===";` + loop + `done;` structure as existing sections (Skills lines 158–188, Agents 190–214, Commands 216–240).
5. **`hooks.json` line 60 and `auggie-flag-clear.sh` line 22 are the EXACT verbatim lines confirmed on disk** — release spec's claimed line numbers are accurate as of this research timestamp.
6. **Cross-consistency challenge:** The new `=== Hooks Cross-Consistency ===` section must extract two facts: (a) the matcher alternation from `hooks.json` line 60 (or a stable JQ query), and (b) the `case` pattern from `auggie-flag-clear.sh` line 22. Both use different syntax (regex `.*` vs shell glob `*`) — comparator must normalize prefixes (e.g., extract `mcp__auggie__`, `mcp__auggie-mcp__`, `mcp__airis-mcp-gateway__auggie_` from each, sort, and diff sets). Builder should plan a Python helper or shell pipeline for this.
