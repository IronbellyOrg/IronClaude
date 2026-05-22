# Skill Description Calibration

## What was tested

`run_eval.py` measures whether Claude's default judgment, given only the
skill's frontmatter (`name` + `description`), invokes the `Skill` tool for
each query. It does NOT process `.claude/commands/sc/*.md` files — it
bypasses command-file routing entirely.

## Why this matters for sc-auggie-review-protocol

This skill is **explicit-trigger-only**. Activation is owned by the slash
command file `.claude/commands/sc/auggie-review.md`, which deterministically
invokes `Skill sc:auggie-review-protocol`. The skill description is NOT a
trigger surface.

User constraint (verbatim): *"We do not want this thing firing due to
keywords in a conversation."*

So the question the calibration asks is: **does the description avoid
luring the model into firing on conversational mentions of code review,
PR review, anti-patterns, etc., that should be routed through the slash
command?**

## Result

Description tested:
> "Auggie-powered code review protocol for PRs, local diffs, and file
> snapshots — orchestrates Auggie's deep retrieval pass, validates findings
> against real files, posts to PR, and offers a remediation handoff chain"

| Query class | Cases | Triggers | Pass | Verdict |
|---|---|---|---|---|
| Negative (conversational) | 7 | 0/14 | 7/7 | Description does NOT fire on conversational mentions |
| Positive (slash-command text) | 3 | 0/6 | 0/3 (expected) | Description does not claim slash-command keywords — command file owns routing |

**Net**: 7/7 on the constraint that matters. Zero false positives across
queries containing "review", "PR", "code review", "audit", "anti-patterns",
"Auggie", "diff", "quality regressions", and "bugs".

## Decision

**Keep description as-is.**

Tightening it to fire on `/sc:auggie-review` text would also broaden
conversational matching, which contradicts the user's hard constraint. The
two channels are by design:

- **Routing**: slash command file → `Skill` invocation (deterministic).
- **Description**: intentionally inert for trigger purposes; serves as
  documentation for what the skill does after it has been invoked.

Calibration complete. No description rewrite required.
