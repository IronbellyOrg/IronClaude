#!/usr/bin/env bash
# PreToolUse(Skill) — Phase 0 gate for sc:recommend.
#
# When Claude invokes the `sc-recommend` skill, this hook injects a context block
# reminding the model that Phase 0 (live surface enumeration + auggie sweep) is
# mandatory before any recommendation is emitted. The hook does NOT block the
# skill (it is fail-open / exit 0); its job is to make the Phase 0 requirement
# unmissable at the moment of invocation, even under context pressure.
#
# Hook contract:
#   - stdin:  JSON { tool_name, tool_input, ... }
#   - exit 0: pass-through; stdout (if non-empty) is injected as additional context
#   - exit 2: block (NOT used here — Phase 0 enforcement is procedural, not blocking)
#
# Match conditions:
#   - tool_name == "Skill"
#   - tool_input.skill in { "sc-recommend", "sc:recommend", "sc-recommend-protocol" }
#     (the third covers any leftover invocation pointing at the old skill name
#      during the transition window)

set -u

INPUT="$(cat 2>/dev/null || true)"

# Cheap prefilter: bail out immediately if payload doesn't even mention sc-recommend.
case "$INPUT" in *'sc-recommend'*|*'sc:recommend'*) ;; *) exit 0;; esac

TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)"
[ "$TOOL_NAME" = "Skill" ] || exit 0

SKILL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_input.skill // .tool_input.name // empty' 2>/dev/null)"

case "$SKILL_NAME" in
    sc-recommend|sc:recommend|sc-recommend-protocol) ;;
    *) exit 0;;
esac

cat <<'EOF'
<sc-recommend-phase0-gate source="pre-skill-hook">
Phase 0 is MANDATORY for sc:recommend. Before emitting any recommendation:

1. Enumerate the live project surface via Glob in parallel:
   - src/superclaude/commands/*.md
   - src/superclaude/skills/*/SKILL.md
   - src/superclaude/agents/*.md  (and .claude/agents/*.md)
   - src/superclaude/templates/**/*.md  (and examples/*-template.md)

2. Issue ONE mcp__auggie__codebase-retrieval query that ranks the enumerated
   surface against the user's verbatim request. Do not iterate file-by-file.

3. For each ranked candidate, Read its source file before allowing it into the
   recommendation. Ghost candidates (no source file resolves) are dropped silently.

If auggie is unavailable, proceed with Glob+Read only AND emit this exact one-line
notice as the first line of the output:
    "Auggie unavailable — ranking falls back to literal Glob+Read; usage nuance may be thin."

Do NOT skip the gate silently. Do NOT use a static keyword → category mapping —
the previous version of this skill failed exactly that way (missed /sc:spec-panel
because the mapping table was stale). Enumeration is dynamic, every invocation.

This block was injected by the Phase-0 PreToolUse hook. It is part of the skill's
contract, not optional guidance.
</sc-recommend-phase0-gate>
EOF

exit 0
