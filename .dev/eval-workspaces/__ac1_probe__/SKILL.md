---
name: __ac1_probe__
description: AC1 probe workspace (T05.01) — relocated per CLAUDE.md addendum + PreToolUse hook
---

# AC1 Probe Workspace

This file demonstrates that after the PreToolUse hook rejected the sibling-workspace
write at `.claude/skills/__ac1_probe__-workspace/SKILL.md`, the retry against
`.dev/eval-workspaces/__ac1_probe__/SKILL.md` succeeded.

Outcome: **B** (hook fired with redirect; retry at correct destination succeeded).
