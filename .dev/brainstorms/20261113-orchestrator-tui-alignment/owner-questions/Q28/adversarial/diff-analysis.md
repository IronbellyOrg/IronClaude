# Diff Analysis: owner-answer proposal comparison (Q28, what `/sc:pr-submit` may do on PR #539)

## Metadata
- Generated: 2026-11-14T01:20Z
- Variants compared: 3 (V1 = proposal-A, nothing before the ruling then level 3 with `--merge-guard off`; V2 = proposal-B, nothing before the ruling then level 2 with hand pushes; V3 = proposal-C, never)
- Total differences found: 16
- Categories: structural (1), content (4), contradictions (4), unique (3), shared assumptions (4: UNSTATED 2, STATED 2)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Section set | five sections, 4 steps | five sections, 4 steps | five sections, 4 steps | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Tool level after the ruling lands | 3 (fix, commit, push, reply, resolve) | 2 (fix and validate locally, stop) | none | High |
| C-002 | Tool level before the ruling | none, or level 1 if the grant row says so | none | none | Medium |
| C-003 | Who pushes, replies and resolves after the ruling | the tool, under one grant row | the #539 author by hand, each under its own grant | the #539 author by hand | Medium |
| C-004 | Draft toggle | `--merge-guard off` | not applicable (level 2 never toggles) | not applicable | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | How a new finding that needs an owner ruling is stopped (spec SW-05 (6), `merged-requirements.md:194`) | by the session's judgment while the tool runs autonomously | structurally: level 2 cannot commit, push, reply or resolve | a person handles every finding | High |
| X-002 | Project standard review loop (`/sc:pr-submit --monitor 3`, project `CLAUDE.md`) | followed after the ruling | partly (verification and fixes, no push) | not used | Medium |
| X-003 | Sessions in the #539 checkout | one PR session (the spec makes the #539 author that session, `merged-requirements.md:965`) | PR session and #539 author alternate unless they are the same session | one (the author) | Medium |
| X-004 | Level 1 before the ruling vs "no tool designs or pushes an INV-008 fix" (`merged-requirements.md:191`) | allowed if the grant row says so; level 1 still sends the verified Codex INV-008 finding to `sc:troubleshoot` for diagnosis, which designs a fix proposal (`sc-pr-submit-protocol/SKILL.md:306`) | not allowed | not allowed | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Full grant-row list for #539 (attach, fix commits, troubleshoot artifacts, push, replies, resolves, re-trigger comment, `--merge-guard off`, resume effects; never merge) | Medium |
| U-002 | V2 | Removes the draft-toggle decision entirely | Low |
| U-003 | V3 | No tool grant row needed | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | Once the Codex INV-008 thread is resolved, the tool ignores it. Verified 2026-11-14: for Codex findings "Resolved threads are excluded; older unresolved Codex roots stay visible" (`~/.claude/skills/sc-pr-submit-protocol/refs/detection-contract.md:132-136`). Note: the thread must be marked resolved; a reply alone leaves it unresolved and selectable | V1 and V2 gate on "the Codex thread is closed by the owner's reply" | High | STATED (verified), not promoted; the reply-versus-resolve detail is carried into the debate |
| A-002 | No new git-configuration finding arrives after SW-02's push. Codex re-reviews new pushes, and a security review can land after a clean code review (owner memory `pr-submit-check-pr-open-before-push.md`). At level 3 a verified Medium-or-higher Codex finding is fixed, pushed and resolved by the tool | V1 and V2 assume the ruling closes the INV-008 topic | High (guard, L3) | UNSTATED, promoted |
| A-003 | The #539 author's hand pushes after the ruling stay safe without the tool's pre-push checks (PR still open, head unchanged; the tool's own guard misses a merged PR, owner memory) | V2 and V3 rely on hand pushes | Medium (state, L3) | UNSTATED, promoted |
| A-004 | The tool runs only in a top-level session, never in a worker or the coordinator (`merged-requirements.md:975`) | all | Low | STATED, not promoted |

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 4
- Total unique contributions: 3
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001, A-002
- Taxonomy tags: S-001 L1; C-001, C-002, C-003, X-002 L2; C-004 L2; X-001, X-003, X-004, A-002, A-003 L3
- Diff points debated: S-001, C-001 to C-004, X-001 to X-004, A-002, A-003 (11)
