# Refactoring Plan: Q2

## Overview
- Base variant: Variant 2 (proposal-B), used as the frame (highest document score)
- Incorporated from: Variant 3 (core answer), Variant 1 (A-002 wording, U-001 feasibility note), debate consensus (FU-1 preconditions)
- Planned changes: 6
- Overall risk: High (Change 1 replaces the base's core answer, as the debate decided 3 of 3)
- Rule carried: the watcher-to-orchestrator handoff is unbuilt; nothing may claim it exists.

## Planned Changes

### Change 1: replace the core answer with claim-only and a one-issue acceptance
- Source: Variant 3, "Answer" (won C-001, C-002, X-002, X-003, 3 of 3)
- Target: base "Answer" and title
- Approach: replace
- Rationale: `--pipeline none` matches recorded design decision D2 (`docs/designs/issue-watcher.md:44`); the default is a confirmed accident (ADJ line 372, X-001, 91 percent); one permission-free session instead of two.
- Risk: High

### Change 2: replace the next steps with Variant 3's, keeping the base's precondition style
- Source: Variant 3 "What happens next" steps 1 to 4; base step 2 (gates as preconditions)
- Target: base "What happens next"
- Approach: restructure
- Rationale: WA-01 small PR, WA-02 edits, WA-04 record; FU-1 runs only after its preconditions hold (won X-001 for the base).
- Risk: Medium

### Change 3: list every FU-1 precondition
- Source: debate consensus (all three advocates); `merged-requirements.md:331`, `:719`, `:604`, `:811`; `src/superclaude/skills/sc-issue-protocol/refs/claim.md:131`; `docs/designs/sc-issue-launch-level-hook.md:625`
- Target: base "What happens next", new step before FU-1
- Approach: insert
- Rationale: OB-H1 item 5 (required before a claim at any level, recorded "Pending, none run"), the `GRANT(WA-04,live-test)` row, Orca answering a read verb, and Q20 (who owns the watcher worktree agent) bind FU-1 under every option.
- Risk: Low

### Change 4: word the acceptance to cover what the session could do
- Source: Variant 1, A-002 (all three advocates REJECT the assumption)
- Target: base "What it costs or risks"
- Approach: replace the first risk bullet
- Rationale: the FU-1 write list is the intended set, not a limit; permission checks are off (TB-PERM) and the session reads untrusted issue text (TB-UNTRUSTED). The owner can write the test issue's text to shrink that risk.
- Risk: Low

### Change 5: record permission-on feasibility during FU-1
- Source: Variant 1, U-001
- Target: base "What stays unresolved"
- Approach: append
- Rationale: gives a later, non-test decision real data; no new run, only an added note to the FU-1 record.
- Risk: Low

### Change 6: unlocks and unresolved rewritten for claim-only
- Source: Variant 3 "What it unlocks" and "What stays unresolved"
- Target: base "What it unlocks", "What stays unresolved"
- Approach: replace
- Rationale: follows from Change 1; the base's "ready plan" and "second agent data" unlocks no longer apply.
- Risk: Medium

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, X-002 | Base: keep the default `worktree` level | Lost 3 of 3: ratifies an accident against recorded decision D2; doubles the permission-free surface; unowned per-claim worktrees and agents. |
| C-002 | Variant 1: decline the acceptance now | Lost 3 of 3: blocks all downstream learning with no end condition; kept only as the stated fallback if a precondition cannot be met. |
| C-006 | Base: amend the design to match the code | Lost 3 of 3: the code should follow the owner's recorded decision. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1, 2, 6 | High/Medium | changes the answer the frame carried, as the debate decided | revert to `variant-3-original.md` plus Changes 3 to 5 |
| 3 to 5 | Low | added preconditions and wording | remove the inserted lines |

## Review Status
- Approval: auto-approved (non-interactive), 2026-11-14
