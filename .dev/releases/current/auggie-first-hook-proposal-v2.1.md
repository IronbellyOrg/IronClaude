# Proposal v2.1: auggie-first nag in freshness hooks (src/-only)

**Target project:** `/config/workspace/IronClaude/`
**Drafted:** 2026-05-14 (v1) → revised after spec-panel (v2) → **revised for src/-only distribution (v2.1)**
**Supersedes:** `auggie-first-hook-proposal-v2.md`. Body and design unchanged; only the **deployment surface** moves from `~/.claude/` (direct) to `src/superclaude/` (canonical) + `make sync-dev` + `superclaude install`.

**Why the surface change:** Per project memory `feedback-hooks-source-of-truth`, direct edits to `~/.claude/` or repo-root `.claude/` are forbidden — they get wiped by the next sync/install cycle and cause "fixed-but-not-fixed" drift. The repo's distribution model is:

```
src/superclaude/             canonical                  (this is where edits land)
   └─ hooks/scripts/*.sh
   └─ hooks/hooks.json
   └─ cli/install_hooks.py
       │
       │  make sync-dev
       ▼
.claude/                     dev convenience copy       (regenerated)
   └─ hooks/*.sh
       │
       │  superclaude install
       ▼
~/.claude/                   user installation          (runtime read here)
   └─ hooks/*.sh
   └─ settings.json
```

---

## 0. Changelog vs v2

| # | Change | Reason |
|---|---|---|
| 0.1 | All file paths in §2 retargeted from `~/.claude/...` → `src/superclaude/...`. | Source-of-truth rule. |
| 0.2 | New file `src/superclaude/hooks/scripts/auggie-flag-clear.sh` (was `~/.claude/hooks/...`). | Same. |
| 0.3 | `hooks.json` patch moves to `src/superclaude/hooks/hooks.json`. The user's `~/.claude/settings.json` is updated by `install_hooks.py`'s additive-merge pass — no direct edit. | Same. |
| 0.4 | Seed data file moves from `~/.claude/auggie-projects.txt` to `src/superclaude/hooks/auggie-projects.txt.example`. `install_hooks.py` deploys it as `~/.claude/auggie-projects.txt` **only if absent** (skip-if-exists, preserves user customizations). | Source-of-truth + user-data preservation. |
| 0.5 | `install_hooks.py`'s `_FRESHNESS_SCRIPTS` list gains `auggie-flag-clear.sh`. | The installer needs to know about the new script. |
| 0.6 | `install_hooks.py` extended with a `_deploy_seed_files()` step that copies `.example` files to `~/.claude/<name>` if no existing file. | First-class seed-data mechanism. |
| 0.7 | Acceptance: `make verify-sync` clean after edits. `make test` green (existing test suite must not regress). | Repo CI hygiene. |
| 0.8 | Acceptance: `superclaude install --force` re-deploys hooks correctly without clobbering user's `auggie-projects.txt`. | Reinstallability. |

---

## 1. Locked design (unchanged from v2)

Same Q1–Q10 from v2 §1. No design drift.

---

## 2. Files affected (src/-only)

| # | Action | Path | Sync target |
|---|---|---|---|
| 1 | MODIFY | `src/superclaude/hooks/scripts/freshness-user-prompt.sh` | `.claude/hooks/freshness-user-prompt.sh` → `~/.claude/hooks/...` |
| 2 | MODIFY | `src/superclaude/hooks/scripts/freshness-session-start.sh` | same chain |
| 3 | CREATE | `src/superclaude/hooks/scripts/auggie-flag-clear.sh` | same chain |
| 4 | MODIFY | `src/superclaude/hooks/hooks.json` | merged into `~/.claude/settings.json` by `install_hooks.py` |
| 5 | CREATE | `src/superclaude/hooks/auggie-projects.txt.example` | copied to `~/.claude/auggie-projects.txt` by `install_hooks.py` **if absent** |
| 6 | MODIFY | `src/superclaude/cli/install_hooks.py` | adds the new script to `_FRESHNESS_SCRIPTS`; adds `_deploy_seed_files()` step |
| 7 | (defer) | tests | Phase 2 — see §14 |

**Forbidden surfaces** (never touched directly, ever):
- `~/.claude/hooks/*` (any file)
- `~/.claude/settings.json`
- `~/.claude/auggie-projects.txt`
- `/config/workspace/IronClaude/.claude/*` (repo-root dev copy)

These are regenerated/installed downstream from src/.

---

## 3. State directory layout (runtime, unchanged from v2)

```
~/.claude/state/
├── auggie-first-pending/<session_id>.txt   # GC: mtime>30d on SessionStart=startup
└── auggie-no-warn/<project_key>            # GC: mtime>180d on SessionStart=startup

~/.claude/logs/
└── auggie-first.jsonl                       # event log

~/.claude/auggie-projects.txt                # user-editable allow-list (seeded once at install)
```

---

## 4. Diff 1 — `src/superclaude/hooks/scripts/freshness-user-prompt.sh`

Identical body to v2 §4 (constants block, §6.5 block, build_envelope refactor, call-site collapse). Path correction only.

## 5. Diff 2 — `src/superclaude/hooks/scripts/freshness-session-start.sh`

Identical body to v2 §5. Path correction only.

## 6. New file — `src/superclaude/hooks/scripts/auggie-flag-clear.sh`

Identical body to v2 §6. Path correction only.

## 7. Diff 3 — `src/superclaude/hooks/hooks.json`

Add PostToolUse entry. Existing `"PostToolUse"` array contains the `Read` matcher; we append the `mcp__auggie__.*` matcher (synchronous). The installer's `_merge_settings()` will detect "no collision" (matcher differs from `Read`) and additively append.

```json
"PostToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/freshness-post-read.sh", "timeout": 1, "async": true}
    ]
  },
  {
    "matcher": "mcp__auggie__.*",
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/auggie-flag-clear.sh", "timeout": 1}
    ]
  }
]
```

(No `async: true` — synchronous, per Wh-8 fix from spec-panel.)

## 8. New file — `src/superclaude/hooks/auggie-projects.txt.example`

```
/config/workspace/InfraDocs
/config/workspace/IronClaude
```

Conventions:
- One absolute CWD path per line.
- No trailing slash; the hooks normalize via awk regardless.
- No comments. The example file documents conventions in a sibling `auggie-projects.README.md` (optional follow-up; not blocking).
- The installer copies this to `~/.claude/auggie-projects.txt` **only if no such file exists**, mirroring shutil-copy2-skip-if-exists semantics from `_copy_scripts(force=False)`.

## 9. Diff 4 — `src/superclaude/cli/install_hooks.py`

### 9.1. Add the new script to `_FRESHNESS_SCRIPTS`

```diff
 _FRESHNESS_SCRIPTS = [
     "freshness-session-start.sh",
     "freshness-user-prompt.sh",
     "freshness-pre-edit.sh",
     "freshness-post-read.sh",
     "freshness-file-changed.sh",  # v1: NOT registered. Kept on disk for v1.5.
     "freshness-subagent-start.sh",
     "freshness-subagent-stop.sh",
+    "auggie-flag-clear.sh",        # v2.1: PostToolUse for mcp__auggie__.* — sticky clear.
 ]
```

### 9.2. New helper `_deploy_seed_files()` and call into `install_hooks()`

```diff
 def install_hooks(
     target_path: Path | None = None, force: bool = False
 ) -> Tuple[bool, str]:
     ...
     # ===== STEP 2: merge into settings.json =====
     settings_merge_result = _merge_settings(...)
     ...
+
+    # ===== STEP 3: deploy seed data files (skip-if-exists, never overwrite user data) =====
+    seed_copied, seed_skipped = _deploy_seed_files(
+        hooks_source_root=_get_hooks_source_root(),
+        dest_root=target_path.parent,
+    )
+    if seed_copied:
+        messages.append("")
+        messages.append(f"📦 Seeded {len(seed_copied)} data file(s):")
+        for name in seed_copied:
+            messages.append(f"   - {name}")
+    if seed_skipped:
+        messages.append(f"⏭️  Preserved {len(seed_skipped)} existing data file(s):")
+        for name in seed_skipped:
+            messages.append(f"   - {name} (user-edited; not overwritten)")

     overall = success_settings and not failed
     return overall, "\n".join(messages)
```

```python
# Seed data files: shipped as <name>.example in src/superclaude/hooks/, deployed
# to ~/.claude/<name> on install ONLY when no such file exists. This preserves
# user customizations across re-installs.
_SEED_FILES = [
    ("auggie-projects.txt.example", "auggie-projects.txt"),
]


def _deploy_seed_files(
    *, hooks_source_root: Path, dest_root: Path
) -> Tuple[list[str], list[str]]:
    copied: list[str] = []
    skipped: list[str] = []
    for src_name, dest_name in _SEED_FILES:
        src = hooks_source_root / src_name
        dest = dest_root / dest_name
        if not src.exists():
            continue
        if dest.exists():
            skipped.append(dest_name)
            continue
        try:
            shutil.copy2(src, dest)
            copied.append(dest_name)
        except OSError:
            pass  # Best-effort; do not fail the whole install on a data-file miss.
    return copied, skipped


def _get_hooks_source_root() -> Path:
    """Locate src/superclaude/hooks/ (parent of scripts/ and home of hooks.json)."""
    package_root = Path(__file__).resolve().parent.parent
    return package_root / "hooks"
```

(Implementation note: the existing `_get_hooks_source()` returns `hooks/hooks.json`; the new `_get_hooks_source_root()` returns the directory. They're independent helpers.)

---

## 10. Deployment chain (what the implementer runs)

```bash
# 1. Edit canonical files
$EDITOR src/superclaude/hooks/scripts/freshness-user-prompt.sh
$EDITOR src/superclaude/hooks/scripts/freshness-session-start.sh
$EDITOR src/superclaude/hooks/scripts/auggie-flag-clear.sh   # CREATE
$EDITOR src/superclaude/hooks/hooks.json
$EDITOR src/superclaude/hooks/auggie-projects.txt.example     # CREATE
$EDITOR src/superclaude/cli/install_hooks.py

# 2. Sync to dev copy (.claude/), verify drift-free
make sync-dev
make verify-sync

# 3. Run the test suite (must stay green)
make test

# 4. (Optional) install to ~/.claude/ for runtime testing
# Not done in this session per source-of-truth rule; tested via ./tests.
# End user runs:
#   uv pip install -e ".[dev]"     # or pipx install
#   superclaude install
```

**Critical:** Step 4 is the user's responsibility. This session terminates at step 3.

---

## 11. Acceptance criteria (v2 list + v2.1 additions)

(v2 list, abbreviated)
- ✅ Adding auggie line never breaks envelope.
- ✅ Sync clear hook closes race (Wh-8).
- ✅ SESSION_ID="unknown" never writes sticky (Wh-1/Wh-6).
- ✅ Trailing-slash variance does not demote indexed projects (Wh-2).
- ✅ State directory bounded by GC.
- ✅ `AUGGIE_FIRST_DISABLE=1` is a complete no-op.
- ✅ Telemetry to `~/.claude/logs/auggie-first.jsonl`.

(v2.1 additions)
- ✅ **C-AC-14:** `make sync-dev` produces no errors and reports `Hooks: 8 files` (one more than baseline 7).
- ✅ **C-AC-15:** `make verify-sync` exits 0 — no drift between src/ and .claude/.
- ✅ **C-AC-16:** `make test` exits 0 — no regression in existing test suite. (New tests can be added in a follow-up; this proposal does not add or modify tests.)
- ✅ **C-AC-17:** `install_hooks.py`'s `_FRESHNESS_SCRIPTS` includes `auggie-flag-clear.sh`.
- ✅ **C-AC-18:** `install_hooks.py` deploys `auggie-projects.txt.example` → `~/.claude/auggie-projects.txt` **only if** no existing file at the destination (preserves user state).
- ✅ **C-AC-19:** `hooks.json` PostToolUse array adds the `mcp__auggie__.*` matcher entry; `_merge_settings()` additively appends without colliding with the existing `Read` matcher (different matcher → no collision).
- ✅ **C-AC-20:** No file under `~/.claude/` or `<repo-root>/.claude/` is edited directly by this proposal's implementation.

---

## 12. Failure modes (unchanged from v2)

See v2 §11 (jq missing, malformed JSON, state dir unwritable, etc.). v2.1 adds:

- **Reinstall over user-edited `auggie-projects.txt`:** Skipped by design (C-AC-18). Logged: `⏭️  Preserved 1 existing data file(s): auggie-projects.txt (user-edited; not overwritten)`.
- **`auggie-projects.txt.example` missing from package:** `_deploy_seed_files` silently skips (best-effort). Hooks degrade to warn-mode for all projects — acceptable graceful degradation.

---

## 13. Open questions (v2 set, all resolved)

OQ-1..OQ-4 — see v2 §12. v2.1 adds no new open questions.

---

## 14. Out of scope (deferred)

- **Automated test harness for the new hook path.** v2 promised a stub at `tests/hooks/test_auggie_first.sh`; v2.1 defers it to a follow-up release because the existing `make test` suite already exercises `install_hooks.py` and adding hook-script tests requires a fixture pattern not currently in the repo. Hook-script behavior is verified manually via §9 scenarios T-1..T-25 (per v2).
- **MCP gateway tool-name aliases** (e.g., `mcp__airis-mcp-gateway__auggie_*`). Today the matcher is exact prefix `mcp__auggie__.*`. Gateway users with renamed tools will need a follow-up.
- **`auggie-projects.README.md` companion file.** Documents one-path-per-line/no-trailing-slash conventions. Nice-to-have; not blocking.

---

## 15. Provenance & verification

- Hooks verified live 2026-05-14:
  - `src/superclaude/hooks/scripts/freshness-user-prompt.sh` ↔ `~/.claude/hooks/freshness-user-prompt.sh`: both exist; src/ version is canonical.
  - `src/superclaude/hooks/scripts/freshness-session-start.sh` ↔ `~/.claude/hooks/freshness-session-start.sh`: both exist; src/ is canonical.
  - `src/superclaude/hooks/hooks.json` exists with current PostToolUse → Read entry.
- MCP registry verified: `auggie context7 sequential-thinking serena tavily`.
- `install_hooks.py` reviewed line-by-line; the new `_deploy_seed_files()` follows the same skip-if-exists pattern as `_copy_scripts(force=False)`.
- `make sync-dev` rule confirmed to glob `src/superclaude/hooks/scripts/*.sh` — the new `auggie-flag-clear.sh` is auto-included with no Makefile change. Seed `.example` file does NOT propagate via sync-dev (sync-dev is for .claude/ dev copy; seed file only lands at user-install time).
