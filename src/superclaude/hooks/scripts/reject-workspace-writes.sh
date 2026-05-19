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

# FU-003 defense-in-depth: reject repo-root `prd-<slug>/` writes.
# The source-of-truth fix lives in `src/superclaude/cli/prd/config.py`
# (default --output now resolves to `.dev/eval-workspaces/` when `.dev/`
# exists). This branch catches any path that bypasses that default and
# attempts to write `<repo-root>/prd-<slug>/<remainder>` directly.
# Anchored at `^` (after stripping the project-root prefix) so it does NOT
# match `docs/prd-foo/`, `.dev/eval-workspaces/prd-foo/`, etc.
REL="${TARGET#${CLAUDE_PROJECT_DIR:-$(pwd)}/}"
if [[ "$REL" =~ ^(prd-[^/]+)/(.*)$ ]]; then
    PRD_DIR="${BASH_REMATCH[1]}"
    PRD_REMAINDER="${BASH_REMATCH[2]}"
    cat >&2 <<EOF
Repo-root PRD path rejected: write to \`${PRD_DIR}/${PRD_REMAINDER}\` blocked. Use \`.dev/eval-workspaces/${PRD_DIR}/${PRD_REMAINDER}\` instead.

Reason: \`superclaude prd run\` outputs belong under \`.dev/eval-workspaces/\`, not at the repository root. The canonical default is set in \`src/superclaude/cli/prd/config.py\` (FU-003 source-fix) and the convention is documented in \`CLAUDE.md\` "Plugin Override — Skill-Creator Workspace Destination". Pass \`--output .dev/eval-workspaces\` explicitly, or omit \`--output\` to use the new default.
EOF
    exit 2
fi

exit 0
