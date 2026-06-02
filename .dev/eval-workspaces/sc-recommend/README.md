# sc-recommend eval workspace

Draft eval set for the rewritten `sc-recommend` skill. This iteration is a **vibe-pass**: no subagent runs, no benchmark.json. The user reviews the SKILL.md + refs/ + command + hook drafts manually and signs off (or sends back feedback) before any benchmark loop is spun up.

## Files

- `evals.json` — the 6 test cases from the build request, with assertions drafted so a future iteration can spawn `with_skill` / `without_skill` subagents without re-authoring.

## When the vibe-pass passes

When the user is happy with the drafts:

1. The skill, hook, command, and refs are committed.
2. Optional next step: a follow-up session can spawn the full iteration loop using these evals (parallel subagents, grader, eval-viewer).

## When the vibe-pass surfaces issues

Common likely issues:

- A test case's `must_appear` set is wrong (e.g., the user disagrees with the expected delegation for eval 2 or 6).
- The R3 hand-off discipline is too aggressive or not aggressive enough.
- The anti-bloat default in eval 4 is too eager — the user may prefer a skill recommendation in some 40-line refactor cases.
- Plugin-mode scope (eval 5) needs adjustment.

Fix in the drafts, then re-present.

## Why eval workspaces live here

Per CLAUDE.md "Plugin Override — Skill-Creator Workspace Destination": skill-creator's default sibling-workspace destination (`.claude/skills/<skill>-workspace/`) is **overridden** in this project. Eval workspaces live under `.dev/eval-workspaces/<skill-name>/` instead. The PreToolUse hook `reject-workspace-writes.sh` enforces this by denying writes to the legacy path with a redirect message.
