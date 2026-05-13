# D-0014 — Test Specification: AC3 `--output` Guard

**Task:** T05.03 — AC3 test: `--output` guard refuses `.claude/` prefixes
**Roadmap Item:** R-014
**Phase:** 5 (Acceptance Validation)
**Date:** 2026-05-13

## Purpose

End-to-end verification that the L3.1 skill-level guard in
`sc-release-split-protocol` SKILL.md Prerequisites step 2a refuses any
`--output` path under the three forbidden prefixes **before** any
artifact is written, and that legitimate `--output` paths proceed
normally.

## Layered defense — L3.1 under test

L1 (PreToolUse hook in `.claude/settings.json`) intercepts `Write|Edit`
tool calls; L2 (`make verify-sync` / `make lint-architecture`) catches
on-disk violations; **L3.1** is the skill-level pre-write refusal
inserted at Prerequisites step 2a in `sc-release-split-protocol`
(landed via T04.01, D-0010). This test exercises L3.1 in isolation:
the guard must trigger before Part 1 begins, before any file is
created in the resolved output directory.

## Invocations under test

| # | `--output` path                                  | Expected outcome |
|---|--------------------------------------------------|------------------|
| 1 | `.claude/skills/foo/`                            | Refuse pre-write |
| 2 | `.claude/agents/foo/`                            | Refuse pre-write |
| 3 | `.claude/commands/foo/`                          | Refuse pre-write |
| 4 | `.dev/releases/current/test-output/` (legitimate)| Proceed normally |

## Acceptance criteria (from phase-5-tasklist.md T05.03)

1. All three forbidden invocations abort pre-write and emit an error
   mentioning `.dev/` as the correct destination.
2. Legitimate invocation proceeds normally and writes its outputs
   under `.dev/`.
3. Post-run directory listing of the three forbidden prefixes shows
   the probe `foo/` directory was NOT created in any of them.
4. All four invocations + post-run directory checks captured in
   `evidence.md`.

## Invocation mode

`sc-release-split-protocol` is a Claude Code skill, **not** a
standalone CLI. It is invoked by Claude via the `Skill` tool when the
`/sc:release-split` slash command is used. Verification is therefore
behavioural: confirm that

1. The SKILL.md text instructs Claude to refuse pre-write for the
   three forbidden prefixes (already confirmed on disk by D-0010 §1
   and §7).
2. The simulated probe path resolves against the guard predicate, the
   refusal message is emitted, and **no artifact** is created on disk
   at the forbidden location.
3. The legitimate path resolves past the guard and the skill proceeds
   to step 3 (`--agents` validation) and onward to Part 1.

This is the same invocation-mode pattern used for D-0010 §5/§6
(the T04.01 verification evidence), now expanded to all three
forbidden prefixes per phase-5 acceptance.

## Trigger source on disk

- `.claude/skills/sc-release-split-protocol/SKILL.md` line 126 —
  Prerequisites step 2a (the refusal clause).
- `.claude/skills/sc-release-split-protocol/SKILL.md` line 416 —
  Error Handling table row.
- `.claude/commands/sc/release-split.md` line 53 — `--output` policy
  entry naming all three forbidden prefixes.

## Test spec used for invocations

A minimal placeholder spec file is referenced solely so that the
invocation form is syntactically complete; the guard fires at
Prerequisites step 2a, **before** Part 1 reads the spec content. The
test does not require a real release spec because the refusal happens
prior to spec-content processing.
