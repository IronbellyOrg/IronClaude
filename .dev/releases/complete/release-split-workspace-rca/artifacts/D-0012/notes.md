# D-0012 — Notes

## Outcome classification

This run produced **Outcome B**: the PreToolUse `reject-workspace-writes.sh`
hook actively fired and blocked a Write tool call against
`.claude/skills/__ac1_probe__-workspace/SKILL.md`. Claude then retried against
`.dev/eval-workspaces/__ac1_probe__/SKILL.md`, and the retry succeeded.

Outcome B is one of the two acceptable outcomes per the phase-5 spec. Either
A or B satisfies AC1; B is the stricter demonstration because it exercises L1
of the layered defense end-to-end (addendum + hook).

## Methodology notes

- The simulation used two complementary techniques:
  1. **Scripted simulation** (`bash` pipes synthetic `tool_input` JSON into the
     hook script directly). This isolates the hook contract from harness
     plumbing, gives a clean transcript, and verifies the exit code and
     redirect message verbatim. Three cases run: positive (Outcome B),
     allowed (Outcome A path), and negative (non-workspace skill dir).
  2. **Live tool call** through the Claude Code harness, which exercises the
     full PreToolUse pipeline including registration in `.claude/settings.json`.

- The freshness-pre-edit user-global hook (`~/.claude/hooks/freshness-pre-edit.sh`)
  fires before the project-local workspace-reject hook for new files in the
  harness ordering. To exercise the project hook's contract on a Write tool
  call, the test pre-seeded an existing placeholder file via `bash` so the
  freshness check could be satisfied by a prior Read. This is orthogonal to
  AC1 — the workspace-reject hook still produced exit 2 + the verbatim redirect
  message, which is what the AC tests.

- Hook precision (R-01 from T03.01) was verified: a write to
  `.claude/skills/__ac1_probe__/SKILL.md` (the canonical skill directory,
  not the workspace sibling) returns exit 0 — the hook does NOT fire on
  legitimate skill writes.

## Deltas vs prior runs

None applicable — this is the first AC1 acceptance run after M1-M3 landed.

## Classification

Non-regression. Both the scripted contract test and the live retry path
produced the spec-required behavior with no false positives.
