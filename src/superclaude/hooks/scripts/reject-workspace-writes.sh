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
