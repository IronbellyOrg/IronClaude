#!/usr/bin/env bash
# PreToolUse(Skill) — advisory Phase 0 reminder for sc:recommend.
#
# When Claude invokes the `sc-recommend` skill, this hook injects a short
# reminder of the skill's routing and verification steps. It is advisory and
# fail-open (always exit 0): it never blocks the skill, prints nothing when it
# cannot parse the payload (e.g. jq missing), and proves nothing about which
# steps ran. The skill's SKILL.md is the authority; keep this text in step with it.
#
# Hook contract:
#   - stdin:  JSON { tool_name, tool_input, ... }
#   - exit 0: pass-through; stdout (if non-empty) is injected as additional context
#   - exit 2: block (NOT used here — the hook is a reminder, not enforcement)
#
# Match conditions:
#   - tool_name == "Skill"
#   - tool_input.skill in { "sc-recommend", "sc:recommend", "sc-recommend-protocol" }
#     (the third is recognized for compatibility with callers that still use the
#      old skill name; it is not the current protocol name)

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
<sc-recommend-phase0-reminder source="pre-skill-hook">
Advisory reminder from a fail-open hook. The sc-recommend skill file is the
authority; this block summarizes it and does not prove any step ran.

With --plugin: skip steps 0-4 below and run the skill's ecosystem search
(Phase 3); local candidates never mix into plugin results.

Local mode, before emitting any recommendation:

0. Read the routing guide first: ~/.claude/HOW-WE-WORK.md, else the skill's
   refs/HOW-WE-WORK.md (plugin installs: ${CLAUDE_SKILL_DIR}/refs/ or
   ${CLAUDE_PLUGIN_ROOT}/skills/sc-recommend/refs/), else
   src/superclaude/core/HOW-WE-WORK.md under the repository root
   (`git rev-parse --show-toplevel`). Inside an IronClaude checkout
   (src/superclaude/commands/ exists under `git rev-parse --show-toplevel`)
   read the src/ copy first. Match the whole requested outcome (deliverable,
   explicit command or artifact, compatible choices, authority ceiling) to
   one routing row, not any single phrase.
   - matched: no cache, no auggie query (auggie_status: skipped). Resolve the
     row's conditions, keep only applicable steps and one alternative, stop at
     the requested deliverable, and verify each selected step in step 4.
   - no_match: continue with step 1.
   - absent (no guide found): no cache helpers; go to step 2 and keep the
     direct-change limit and workflow-first planning rules.

1. Cache (no_match, inside an IronClaude checkout only): a hit is a hint,
   not an answer. Verify its candidate in step 4 and rebuild the handoff from
   this request's own inputs; never emit the cached text or its paths
   verbatim. Reject an incompatible, retired or unavailable hint and continue
   live. A supported miss runs the cold path; recheck its result before
   emitting it. A budget-exceeded miss never reuses the cached row.

2. Enumerate the live surface (installed, project, plugin, then checkout):
   - $HOME/.claude/commands/sc/*.md, $HOME/.claude/skills/*/SKILL.md,
     $HOME/.claude/agents/*.md, $HOME/.claude/templates/**/*.md
   - .claude/commands/**/*.md, .claude/skills/*/SKILL.md, .claude/agents/*.md
   - ${CLAUDE_PLUGIN_ROOT}/commands, skills, agents (plugin installs only)
   - src/superclaude/commands, skills, agents, templates and
     src/superclaude/examples/*-template.md, under `git rev-parse --show-toplevel`
     (only inside an IronClaude checkout: src/superclaude/commands/ exists there)

3. Unless matched, issue ONE mcp__auggie__codebase-retrieval query that ranks
   the enumerated surface against the user's verbatim request. Do not iterate
   file-by-file.

4. Before any candidate enters the recommendation (each selected step when
   matched, and every accepted cache hint), read the copy that would actually
   run, its declared interface, its backing skill and the references relevant
   to the advertised behavior, and current lifecycle guidance. A missing
   matched step stays visible as "not installed: <name>"; other unresolved
   candidates are dropped. A material disagreement between sources is a
   contract gap, never a runnable command.

If the auggie query fails (auggie unavailable; not matched mode, where the query is
skipped and no notice is emitted), proceed with Glob+Read only AND emit this exact
one-line notice as the first line of the output:
    "Auggie unavailable — ranking falls back to literal Glob+Read; usage nuance may be thin."

Do NOT use a hand-kept keyword → category mapping; the guide's routing table is the only fixed routing source —
the previous version of this skill failed exactly that way (missed /sc:spec-panel
because the mapping table was stale). Enumeration is dynamic, every invocation.
</sc-recommend-phase0-reminder>
EOF

exit 0
