# Refactoring Plan (Q01)

## Overview
- Base variant: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/adversarial/adversarial/variant-1-original.md`
- Incorporated variant: Variant 2 (CLAY), `variant-2-original.md` in the same folder
- Planned changes: 8 (7 additions or edits from V2 and the debate, 1 correction pair counted as one)
- Rejected alternatives: 6
- Overall risk: Low to Medium (text changes only; no code, no GitHub writes)
- Output of the merge: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q01/adversarial/merged-hybrid-position.md`

## Planned Changes

### Change 1: Widen the claim to the three consents the topic names
- Source: V2 cited fact 8 (D13 and D04 verdicts), V1 base lacks requirement R-2
- Target: `## Claim` and a new short `## Scope` section in the base
- Approach: insert
- Rationale: both scorers found V1 missing the cleanup-design approval (R-2) and only brushing `--apply` (base-selection C1, RC 0.75). Debate points C-001, C-002.
- Risk: Low

### Change 2: State which record governs, and mark owner intent as the one open point
- Source: base (V1) facts 1 to 5, debate points X-001 (V1 won, 85%), A-001 (agreed, 78%)
- Target: `## Claim`
- Approach: replace
- Rationale: V2's best attack on V1 was that it lists the line-57 conflict as a risk and never rules (V2 weakness 1). The ruling: the owner's 2026-11-17 chat rule governs the mechanics; "written by the owner" in Decision 8 is read as "owner-sourced, never agent-created". Whether the owner's "narrow d2" at 04:46 meant to restore an owner-written row is UNVERIFIED (order and timezone not shown); one chat confirmation by the owner settles it.
- Risk: Medium (it asserts a reading of the owner's words; mitigated by the UNVERIFIED label and the single confirmation)

### Change 3: Add checks on the recorded go, adopted from `answer-check`
- Source: V2 mechanism step 4 (D:694, D:598), debate points C-001 (hybrid, 78%), C-003
- Target: `## Mechanism`, new step 4
- Approach: append
- Rationale: V2 showed a gap in V1: nothing checks an agent-recorded go (V1 admits it). Adopt the four tests as requirements for the recorded go: typed by a person in their own session, never relayed by an agent; names the entry or issue; newer than the entry's last edit; question key matches. Parameterise the owner identity (D:694 names Clay). Until a script exists the agent records the owner's quoted words, date and exact scope, and a go without those fields is refused.
- Risk: Medium (designed in D:694, not built; stated as such)

### Change 4: Give a recorded go an end and a revocation path
- Source: V2 key binding (`merge_safety:<PR>:<head sha>`), V1 precedent "ends at that Task's `worker_done`" (contract line 245), debate point A-003, shared assumption A-003
- Target: `## Mechanism`, new step 5
- Approach: append
- Rationale: both papers were silent on how a go ends. A go ends at the named action, ends for a merge when the PR head moves, and ends when the owner revokes it in chat.
- Risk: Low

### Change 5: Add fail-closed default and a use log
- Source: V2 cited facts 3 and 4 (D:696, `repos.py:295`), debate point C-006
- Target: `## Mechanism`, new step 6
- Approach: append
- Rationale: separable, cheap benefit that both advocates accepted. No recorded go means no write; each use names the go it relied on.
- Risk: Low

### Change 6: Say which consents are standing and which are per action, without deciding the unresolved point
- Source: D04 verdict (four standing, merge and close per PR), V2 D:116, debate points C-002 (unresolved), C-005 (V1 won, 95%), A-002
- Target: new `## Scope` section
- Approach: insert
- Rationale: the old per-issue row has no reader in master since PR 682 (A-002). Writes the old row covered (plan reply, marker, mention, label, Status) are covered, per D04, by four standing low-stakes grants; merge, close, `--apply` and the cleanup-design approval are per-action chat goes. C-002 stayed unresolved in debate, so the text cites D04 as the source and does not claim a debate win.
- Risk: Medium

### Change 7: Add V2's separable risks
- Source: V2 risks (U37 D:1295, `grants` file inside the orchestrator's write reach D:688, `E-NO-GRANT` covers at most two of six entries)
- Target: `## What it risks`
- Approach: append
- Rationale: cheap, verified by both scorers (D:688, D:696, D:1295), and apply to V1's own mechanism (the same-host terminal problem applies to any chat go).
- Risk: Low

### Change 8: Correct two statements in the base
- Source: both scorers (K1), orchestrator verification
- Target: `## Cited facts` items 7 and 8
- Approach: replace
- Rationale: fact 7 says a search of master for "grant row" finds only `WORKER-CONTRACT.md:57` and `issue-pipeline-fu1.md:24,26`; it also finds `docs/designs/orchestrator.md:116`. Fact 8 and the Strengths text say contract lines 241 and 245 refuse bulk standing grants; they say only that an outward action needs the user's instruction naming it (line 241) and that no pre-authorization waives a push (line 245). The "no standing merge and close" conclusion comes from the D04 verdict.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach was kept |
|---|---|---|
| C-005 | Standing `pr.merge` and `issue.close` on the `grants` list | V2 conceded; D04 verdict and contract lines 241 and 245 |
| C-003 | Present `E-NO-GRANT` as the main control | It covers at most two of six entries (V2 concession; D:696) |
| C-001 | "No record at all": drop the recorded go entirely | A person still needs a durable, per-scope record of the go; the checks are added instead |
| S-001, S-003 | Reorder the paper to V2's fact order | Order only; no value to a reader |
| A-002 | Declare the per-issue row question moot | Line 57 still names the row and issue 687's approvals are the same kind of consent; the question is reframed, not dropped |
| X-001 | Restore an owner-written file row (reading line 57 literally) | Against the owner's chat rule; owner intent on "narrow d2" stays one open chat confirmation |

## Risk Summary

| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 1 | Low | Scope reads wider than the topic | Delete the section |
| 2 | Medium | Misstates the owner's intent | The owner's one chat answer replaces it |
| 3 | Medium | Cites an unbuilt check as a requirement | Marked "designed, not built" |
| 4, 5, 7 | Low | Extra text | Delete the step |
| 6 | Medium | Conflicts with a later D04 revision | Re-read D04 |
| 8 | Low | None (corrections) | n/a |

## Review Status
Auto-approved (non-interactive run, `--unattended`).
