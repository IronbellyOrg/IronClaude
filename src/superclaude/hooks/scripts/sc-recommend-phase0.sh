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

0. Read the routing guide first: ~/.claude/HOW-WE-WORK.md, else the skill's
   refs/HOW-WE-WORK.md (plugin installs: ${CLAUDE_SKILL_DIR}/refs/ or
   ${CLAUDE_PLUGIN_ROOT}/skills/sc-recommend/refs/), else
   src/superclaude/core/HOW-WE-WORK.md under the repository root
   (`git rev-parse --show-toplevel`). Inside an IronClaude checkout
   (src/superclaude/commands/ exists under `git rev-parse --show-toplevel`)
   read the src/ copy first. If a routing row matches (matched mode), its
   steps decide the answer; still verify each step's command or skill below. If no guide is found, continue without it
   (guide_status: absent). Skip this step with --plugin.

1. Enumerate the live surface (installed, project, plugin, then checkout):
   - $HOME/.claude/commands/sc/*.md, $HOME/.claude/skills/*/SKILL.md,
     $HOME/.claude/agents/*.md, $HOME/.claude/templates/**/*.md
   - .claude/commands/**/*.md, .claude/skills/*/SKILL.md, .claude/agents/*.md
   - ${CLAUDE_PLUGIN_ROOT}/commands, skills, agents (plugin installs only)
   - src/superclaude/commands, skills, agents, templates and
     src/superclaude/examples/*-template.md, under `git rev-parse --show-toplevel`
     (only inside an IronClaude checkout: src/superclaude/commands/ exists there)

2. Issue ONE mcp__auggie__codebase-retrieval query that ranks the enumerated
   surface against the user's verbatim request. Do not iterate file-by-file.
   Exception: in matched mode (step 0 matched a routing row) skip this query
   (auggie_status: skipped) and verify the matched row's steps in step 3.

3. For each ranked candidate (in matched mode, each step's command or skill in
   the matched row), Read its source file before allowing it into the
   recommendation. Ghost candidates (no source file resolves) are dropped silently,
   except a matched row's step, which is kept and marked "not installed: <name>".

If the auggie query fails (auggie unavailable; not matched mode, where the query is
skipped and no notice is emitted), proceed with Glob+Read only AND emit this exact
one-line notice as the first line of the output:
    "Auggie unavailable — ranking falls back to literal Glob+Read; usage nuance may be thin."

Do NOT skip the gate silently. Do NOT use a hand-kept keyword → category mapping; the guide's routing table is the only fixed routing source —
the previous version of this skill failed exactly that way (missed /sc:spec-panel
because the mapping table was stale). Enumeration is dynamic, every invocation.

This block was injected by the Phase-0 PreToolUse hook. It is part of the skill's
contract, not optional guidance.
</sc-recommend-phase0-gate>
EOF

exit 0
