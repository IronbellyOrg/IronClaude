# Refactoring Plan (Step 4)

## Overview
- Base: Variant 1 (OURS), file `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/variant-1-original.md`
- Incorporated from: Variant 2 (CLAY), file `.../variant-2-original.md`
- Planned changes: 8 (6 incorporations from Variant 2, 2 corrections of the base)
- Rejected alternatives: 5
- Overall risk: Low (text only; no code)
- Output file: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/merged-qg4-position.md`

## Planned Changes

### Change 1: Correct the WC:137 claim (base weakness, X-001)
- Source: debate-transcript.md, X-001 (both advocates, 85 percent); orchestrator check of `WORKER-CONTRACT.md:131-138`
- Target: base section "OD-7", Fact 1
- Approach: replace
- Text: replace "The input-veto line says "never interrupt" (`:137`)" with "Line 137 (input veto) belongs to the "Answers and acks" block (`:131-138`) and governs the typed copy of an answer, so it is not a general ban; the point that stands is that no contract text authorizes a second interrupt: D:749 and D:764 add the exception themselves and D:764 says it conflicts with the coordinator spec in five places."
- Rationale: verified error in the base; the conclusion survives the correction
- Risk: Low

### Change 2: Keep the escalation-first rule without the interrupt (U-006)
- Source: Variant 2, OD-7 "What it gets right"; both advocates' final answers
- Target: base "OD-7", after Fact 7
- Approach: insert
- Text: "Hybrid kept: the verb `escalate` writes the escalation first and sends nothing if the escalation is refused (D:749, D:764), with no interrupt option."
- Rationale: both advocates adopt it; separable from the contested rule
- Risk: Low

### Change 3: Record build conditions for a later N7 (U-004)
- Source: Variant 2 OD-7 Fact 3 (D:925-928) and both advocates
- Target: base "Summary of what is kept", OD-7 clause
- Approach: replace the OD-7 clause with: "OD-7 closed unless the owner asks. To reopen it: (a) a contract exception written like S6's (WC:63, WC:124); (b) the five coordinator-spec changes C25 to C29 (D:925-928); (c) a rule that suppresses the L2 nudge after an interrupt (WC:164); (d) a check whether `--interrupt` has its own receipt, because U40 (D:1298) covers text sends only."
- Rationale: makes the reserve testable
- Risk: Low

### Change 4: Soften "not possible" to "trigger not present" and add K13 (X-002)
- Source: debate-transcript.md X-002 (split resolved as HYBRID); D:1235
- Target: base "OD-8", "Risk of No"
- Approach: replace
- Text: "Risk of No: a double claim by two logins, two users or two hosts. The trigger is not present on the settled one-host topology (D07) and none has been observed. The design itself rates the risk medium likelihood, medium impact and names the lease as its mitigation (K13, D:1235), so the reserve rests on the absent trigger, not on a small risk."
- Rationale: both advocates say "not possible" is too strong
- Risk: Low

### Change 5: Narrow the `marker_in_window` defence (Variant 2 weakness 5)
- Source: Variant 2 advocate; orchestrator check `predicates.py:279-293`
- Target: base "OD-8", Fact 4
- Approach: replace
- Text: "The owner's line has the create-once claim files on a shared branch (Q26) and the claim-marker check `marker_in_window` (`src/superclaude/cli/issue_watch/predicates.py:279-293`, D01 item 4). The marker check counts an own-login claim marker only after the claim exists, so it does not close the window before the marker is posted."
- Rationale: the base overstated what the check covers
- Risk: Low

### Change 6: Reserve the persisted names and the marker, and note the stale-rule design task (U-005 and orchestrator inference)
- Source: Variant 2 OD-8 Fact 4 (D:547); D:113
- Target: base "Summary of what is kept", OD-8 clause
- Approach: replace the OD-8 clause with: "OD-8 reserved. Trigger: a second host or a second user runs a poll. Before building: a stale-lease rule (a time-based rule would give up the "no clock agreement between hosts" property D:113 names, so this is a design task; orchestrator inference); the marker renamed `sc:coordinator:lease` (D08); the state step names `plan_rechecked`, `lease_posted`, `claim_started`, `claim_done` (D:547) reserved so a later build needs no migration; test T4 rewritten."
- Rationale: both advocates accept the trigger and the stale-lease condition
- Risk: Low

### Change 7: OD-9 hybrid and cheap checks (C-007, A-001)
- Source: both advocates (C-007 at 60 percent, A-001 QUALIFY)
- Target: base "OD-9", closing paragraph and "Summary of what is kept"
- Approach: append
- Text: "If the owner ever turns the streams on, enable `could_assign` alone: `mention` and `affects` are subsets of `involves`. The two unproven assumptions behind OD-7 and OD-9 are cheap, read-only checks: U8 is three searches (D:137) and U40 is `orca terminal send --help` plus one local send (D:1298). Run them before the owner decides on a later build."
- Rationale: turns two unknowns into facts at low cost
- Risk: Low

### Change 8: Add the detector gap (Variant 2 weakness 4)
- Source: Variant 2 advocate (UNVERIFIED: no detector found)
- Target: base "OD-8", after "What it gets right"
- Approach: insert
- Text: "Known gap: no rule notices that a second host or user has started a poll, so the trigger depends on someone remembering (no detector found; UNVERIFIED that none exists elsewhere). Writing the trigger into the spec and the runbook is the minimum."
- Rationale: honest limit of a reserve
- Risk: Low

## Changes NOT Being Made
| Diff point | Variant 2 approach | Why the base stands |
|---|---|---|
| C-001 | Build N7 now, narrowly | No incident, no landing receipt (U40, D:1298), nudge undoes it (WC:164); CLAY's own advocate concedes |
| C-004 | Build the lease now | Trigger absent (D:113, D07); crashed-lease defect with no stale rule (C-005) |
| C-006 | Turn the info streams on now | U8 replies unverified (D:137); most of the streams duplicate `involves` (`collect.py:200-209`) |
| X-003 | "Narrow guard" as enough | It limits the caller (D:767), not landing or staying |
| S-002 | Concede-and-keep closing | The base closing already carries the same separable benefits through changes 2, 3, 6 and 7 |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 to 8 | Low | Text in the merged position; no code, no GitHub write | Re-run from the base variant |

## Review Status
Auto-approved (unattended mode; no interactive checkpoint). Timestamp 2026-11-20.
