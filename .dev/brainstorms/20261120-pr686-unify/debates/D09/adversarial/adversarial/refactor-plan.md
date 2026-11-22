# Refactoring Plan (Step 4)

## Overview

- Base: Variant 2 (CLAY paper) at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/adversarial/variant-2-original.md`
- Incorporated: Variant 1 (OURS paper) `variant-1-original.md`, plus debate results in `debate-transcript.md` and the probe in `invariant-probe.md` (same folder)
- Planned changes: 9. Rejected alternatives: 4. Overall risk: Low to Medium (a document merge; no code is touched)
- The merged output is a single position paper, "the hybrid", whose last section is the rule text the spec must say. Output path: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D09/adversarial/merged-output.md`

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|-------|--------|----------------|----------|-----------------------------|------|
| 1 | Rewrite the claim as the agreed hybrid | V1 Claim and Concession; V2 Claim; Round 2 final positions | `## Claim` | replace | Both advocates agreed after Round 2: adopt read-only `plan_check` plus `held_incomplete` now; the only poll write ever allowed is add or remove `hold:plan` behind the `issue.hold` grant, off until a dry-run and a label-write-under-cron test pass; NG-2 amended to name exactly that; D2 unchanged (confidence 92% on C-001, 62% on C-002) | Low |
| 2 | Add the governing write rule: least privilege by actor | V1 Cited facts 4 and 6 (R24, WC-9, `claim.md:9`) | new section `## Who may write what` | insert | U-001: the owner's chain keeps workers read-only and puts every other write behind a grant row; the poll gets the single exception | Medium |
| 3 | Correct the human-gate statement | Probe INV-002 (moderator verified, `cycle.py:883`, `:998` on master; 0 references in the PR 686 head), C-007, X-001 | CLAY Fact 9 | replace | The tree with no human gate is the PR 686 head and design 681, not master; master's poll still needs the approver's label | Low |
| 4 | Fix the write count and the stateless wording | Diff X-002 and C9 findings; Round 2 (poll must not create labels, init does, R11) | Claim, Mechanism, Costs | replace | The paper says one write but lists three calls (create, add, remove); create moves to the per-repo init; "stateless-ish" contradicts the `holds` map | Low |
| 5 | Add the cost side honestly | V1 Cited fact 8 (corrected: `state` has 2 values, `plan_request` has 5, `orchestrator.md:486`), CLAY Round 2 cost list | `## What it costs` | append | Measured cost: `LabelWriter` about 87 lines, about 22 of 58 tests touch label writes (rough), FU-3 token scope, `hand_removed` state | Low |
| 6 | Add the unattended-wrong-write risk with a mitigation | V1 Cited fact 7 and Risks (withdrawn in part: add is idempotent; wrong-issue repeat stays) | `## What it risks` | append | X-003 split agreed; mitigation is the grant switch, the dry-run, the budget and a per-cycle failure memory (INV-006) | Low |
| 7 | Add the spec lines from the probe's MEDIUM findings | INV-001, INV-003 to INV-009 | new section `## Rule text` | insert | Each is a one-line spec rule: `plan_check` before the approval read; an edit that fills the plan voids the approval and needs a fresh one (R19, R36); grant is document-level; off state skips as `held_incomplete` with no warning and ignores a leftover label; `<...>` placeholder-only sections count as empty; body read allowed for `plan_check` only, held in memory, never in audit, store, argv or a typed line; one poll per repo is a stated rule; both labels created by init; failed label write counts against the budget once per cycle | Medium |
| 8 | Record the single unresolved point | Debate C-002 | `## Open point` | insert | Whether the dormant label-write code ships in PR 686 now or later is not agreed; the rule text is | Low |
| 9 | Keep OURS' honest concession and fold the visibility finding in | V1 Concession; Round 2 both sides conceded visibility is plausible and unmeasured | `## What it gets right` | append | No evidence anyone reads `hold:plan`; a hand-cleared label does not release the issue (CLAY Round 2 capability test) | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|------------|-------------------|-----------|
| C-002 (OURS) | Coordinator writes the label under a grant row | OURS advocate withdrew it in Round 2: a held issue is never sent to the coordinator (`orchestrator.md:459`), so the coordinator would need a new wake kind or a second cron script; it fails on simplicity |
| C-004 (CLAY) | Poll sends a plan request after one quiet hour | Both sides defer to the topology decision (D07); it is a wake-file item, not a GitHub write |
| C-005 (CLAY) | Orchestrator writes a lease comment | Not a poll write; depends on one orchestrator per repo or several (D07) |
| OURS fact 9 (Jay's system, "ironbelly is shared") | Use as evidence against the label | The Jay comparison is UNVERIFIED; the shared login applies to all existing writes alike (A-005) |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1, 3, 4, 5, 6, 8, 9 | Low | wording only | revert the paragraph |
| 2, 7 | Medium | a spec rule that is too tight or too loose | each rule is one line, individually removable |

## Review Status

Auto-approved (unattended mode, `--interactive` not set).
