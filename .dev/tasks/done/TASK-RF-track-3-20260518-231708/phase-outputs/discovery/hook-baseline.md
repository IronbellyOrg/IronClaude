# Baseline snapshot — `src/superclaude/hooks/scripts/reject-workspace-writes.sh`

**Captured:** 2026-05-19T02:03:26Z
**Purpose:** Pre-extension reference state for Phase 2 Step 2.5 (Option A defense-in-depth branch).

## Current script (verbatim)

```bash
#!/usr/bin/env bash
# PreToolUse(Write|Edit) — reject-with-redirect for skill-creator sibling-workspace convention.
# Semantics: deny + explanatory message (Claude Code hooks do not transparently rewrite paths).
# Source: phase-3-tasklist.md T03.01, FR-L1.1, R-007.
#
# Decision contract:
#   - exit 0          → allow (path does not match `.claude/skills/*-workspace/<remainder>`)
#   - exit 2 + stderr → block; stderr is surfaced to Claude as the deny reason
#
# Pattern precision (R-01): only `<...>/.claude/skills/<X>-workspace/<remainder>` matches.
# Negative cases (must NOT fire):
#   - `.claude/skills/<X>/file.md`          (directory has no `-workspace` suffix)
#   - `.claude/skills/<X>/workspace.md`     (`workspace.md` is a file, not a `-workspace/` dir)

set -u

INPUT="$(cat 2>/dev/null || true)"

# Extract file_path from tool_input. Write/Edit always use `file_path`.
TARGET="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)"

# No path → cannot enforce → allow (fail-open).
[ -z "${TARGET:-}" ] && exit 0

# Match `.claude/skills/<X>-workspace/<remainder>` anywhere in the path.
# The trailing `/` after `-workspace` is what distinguishes a directory segment
# from a file named `workspace.md` or `something-workspace.md`.
if [[ "$TARGET" =~ \.claude/skills/([^/]+)-workspace/(.*)$ ]]; then
    SKILL_X="${BASH_REMATCH[1]}"
    REMAINDER="${BASH_REMATCH[2]}"
    cat >&2 <<EOF
Workspace path rejected: write to \`.claude/skills/${SKILL_X}-workspace/${REMAINDER}\` blocked. Use \`.dev/eval-workspaces/${SKILL_X}/${REMAINDER}\` instead.

Reason: skill-creator's sibling-workspace convention places eval workspaces next to the skill directory under \`.claude/skills/\`, which mixes throwaway artifacts with the source-of-truth skill packages. This project relocates them under \`.dev/eval-workspaces/<skill-name>/\`. See \`.dev/README.md\` for the published convention, or run \`make eval-skill SKILL=${SKILL_X}\` to create the correct destination.
EOF
    exit 2
fi

exit 0
```

## Key reference points for Phase 2 insertion

- **Total line count:** 40 (matches research 02 inventory)
- **Existing `BASH_REMATCH` regex branch:** L28 — `if [[ "$TARGET" =~ \.claude/skills/([^/]+)-workspace/(.*)$ ]]; then`
- **Existing `exit 2` (deny path):** L36
- **Existing `exit 0` (allow path):** L23 (early-exit on empty TARGET) and L39 (final default-allow)
- **Shebang:** L1 `#!/usr/bin/env bash`
- **Strict mode:** L15 `set -u` (note: `set -e` is intentionally NOT used per fail-open philosophy)
- **Variables already available:** `TARGET` (extracted JSON file_path)

## Option A extension plan (defense-in-depth for FU-003)

Insert ONE additional regex branch IMMEDIATELY AFTER L37 (the closing `fi` of the existing skill-workspace branch) and BEFORE the final `exit 0` on L39. The new branch:

1. Computes `REL="${TARGET#${CLAUDE_PROJECT_DIR:-$(pwd)}/}"` — strips the project-root prefix so the regex anchors at the repo-relative top segment. (`CLAUDE_PROJECT_DIR` is set by Claude Code when invoking hooks; fall back to `$(pwd)` if unset.)
2. Tests `if [[ "$REL" =~ ^(prd-[^/]+)/(.*)$ ]]; then` — anchored at `^` so `docs/prd-foo/` and `.dev/eval-workspaces/prd-foo/` are NOT matched.
3. On match: emits a stderr message naming the bad dir, pointing to `.dev/eval-workspaces/` as the canonical destination, citing `src/superclaude/cli/prd/config.py` (FU-003 source-fix) and `CLAUDE.md` "Plugin Override" as authoritative sources.
4. `exit 2`.

**Constraints preserved:**
- Existing L28 branch + L31-35 heredoc + L36 `exit 2` are UNCHANGED.
- L1 shebang, L15 `set -u`, L17-23 input handling, and L39 final `exit 0` are UNCHANGED.
- No new file is created — Option A is preferred over Option C (new generic hook) per research 02 because it incurs ZERO registration delta to `_FRESHNESS_SCRIPTS`, `hooks.json`, or `.claude/settings.json`.
