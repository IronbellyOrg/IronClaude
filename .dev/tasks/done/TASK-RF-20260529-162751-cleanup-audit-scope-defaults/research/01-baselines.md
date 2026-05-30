# Research: Baselines for sc:cleanup-audit scope-defaults edit

**Topic type:** File Inventory + Patterns & Conventions
**Scope:** 4 target files in `~/.claude/skills/sc-cleanup-audit-protocol/` and `~/.claude/commands/sc/`
**Status:** Complete
**Date:** 2026-05-29

---

## Target file inventory

### 1. `~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh` (134 lines)

POSIX shell script that produces the file inventory consumed by every downstream pass.

Key lines:
- L8: `TARGET="${1:-.}"` — target path (default cwd)
- L9: `BATCH_SIZE="${2:-50}"`
- L20-21: git path → `FILE_LIST=$(git ls-files -- "$TARGET" 2>/dev/null)` — **no filter applied**
- L22-38: find fallback → excludes `node_modules`, `dist`, `build`, `.next`, `vendor`, `.venv`, `.tox`, `.mypy_cache`, `.pytest_cache`, `coverage`, `__pycache__`, `.cache`, `.git` — **does NOT exclude hidden dirs as a class, does NOT exclude BMAD dirs**
- L41: `TOTAL=$(echo "$FILE_LIST" | grep -c .)` — counted from `$FILE_LIST` so any filter applied to FILE_LIST flows downstream

Strategy: a single `apply_scope` filter function applied to BOTH branches at L21 and L38 → all downstream artifacts (type distribution, domain classification, batch assignments, summary) inherit the exclusion automatically.

### 2. `~/.claude/skills/sc-cleanup-audit-protocol/SKILL.md` (155 lines)

Key insertion points:
- L51: `## Behavioral Flow` → `1. **Discover**: Enumerate repository files via shell preprocessing and repo-inventory.sh...` — natural place for "Default scope exclusions" paragraph
- `## Key Patterns` (search for line beginning `- **Conservative Escalation**`) — natural place for a new "Scope Floor" bullet

### 3. `~/.claude/skills/sc-cleanup-audit-protocol/rules/pass1-surface-scan.md` (81 lines)

Read by the `audit-scanner` agent (Haiku). Has `## Goal` at L1, `## Guiding Question` at L7. Insertion point for "Scope rule" section: after `## Goal`, before `## Guiding Question` (or after, doesn't matter — both work for the agent's read order).

### 4. `~/.claude/commands/sc/cleanup-audit.md` (118 lines)

Cosmetic only. The `## Repository Context` block runs `!git ls-files | wc -l` which reports the full tracked count, misleading users about audit scope.

## Default exclusion patterns (final form)

```
^(\.|.*/\.)|^_bmad/|^_bmad-output/|^_planning-input/|^\.claude-audit/
```

Components:
- `^\.|.*/\.` — any leading-dot path segment (covers `.github/`, `.dev/`, `.claude/`, etc., AND nested like `internal/foo/.bar/`)
- `^_bmad/`, `^_bmad-output/`, `^_planning-input/` — BMAD directories
- `^\.claude-audit/` — audit's own output (self-exclusion)

Verified via the TUIBBS audit's enforcement filter (works in `awk` form):
```sh
git ls-files | awk '!(/^\./ || /\/\./ || /^_bmad\// || /^_bmad-output\// || /^_planning-input\//)'
```
That filter produced 389 in-scope paths from 1,100 tracked in TUIBBS.

## Per-project SCOPE.md override convention

The current `SCOPE.md` (at `/config/workspace/TUIBBS/.claude-audit/SCOPE.md`) is human-readable Markdown. For machine consumption, the script will look for lines of the form:

```
EXCLUDE: <regex>
```

inside `SCOPE.md` (or wherever `SCOPE_FILE` env var points). Lines without the `EXCLUDE: ` prefix are ignored (so the human-readable narrative coexists with machine-readable patterns).

The default exclusions are a **floor** — per-project rules ADD to the default set, they don't replace it. The TUIBBS SCOPE.md can stay verbatim; the script picks up its rules automatically if any `EXCLUDE: ...` lines are added.

## Smoke test

Once edits are in place, the verification is:
```sh
cd /config/workspace/TUIBBS
bash ~/.claude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh . 50 | grep "Total files:"
```
Expected output: `Total files: 389` (matches the 2026-05-29 TUIBBS final-scope post-amendment count recorded at `.claude-audit/progress.json:current_scope.in_scope_paths`).

## Rollback strategy

Each edit is self-contained at the file level. To roll back: `git checkout HEAD -- <file>` on the affected file. The skill directory IS under git? — Verify in Phase 1. If not, snapshot each file to `${TASK_DIR}.snapshot/` before editing.
