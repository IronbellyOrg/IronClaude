# Merge Log (Step 5)

## Metadata
- Base: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/adversarial/variant-1-original.md`
- Non-base source: Variant 2 (CLAY), `.../adversarial/variant-2-original.md`
- Plan: `.../adversarial/refactor-plan.md`
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG4/adversarial/merged-qg4-position.md`
- Executor: merge-executor
- Changes applied: 8 of 8 planned
- Status: complete, post-merge validation pass
- Timestamp: 2026-11-20

Housekeeping edits outside the plan (required by the merge instruction): document retitled "QG4 merged position: build now or reserve (OD-7, OD-8, OD-9)"; the base line "Status: header stub. Sections are appended below." replaced with "Status: merged position. Base: Variant 1 (OURS); eight planned changes applied from the refactoring plan."; provenance header comments and per-block source tags added.

## Changes Applied

### Change 1: Correct the WC:137 claim
- Status: applied
- Target: OD-7, Fact 1
- Before: "The input-veto line says "never interrupt" (`:137`)."
- After: "Line 137 (input veto) belongs to the "Answers and acks" block (`:131-138`) and governs the typed copy of an answer, so it is not a general ban; the point that stands is that no contract text authorizes a second interrupt: D:749 and D:764 add the exception themselves and D:764 says it conflicts with the coordinator spec in five places."
- Provenance tag: `Base (original, modified) - Change #1`
- Validation: the following sentence of the base ("N7 would be a second interrupt case with no contract text behind it ...") is kept and is consistent with the new text. No "never interrupt" statement remains.

### Change 2: Keep the escalation-first rule without the interrupt
- Status: applied
- Target: OD-7, inserted after Fact 7 and before "Cost of No"
- After: "Hybrid kept: the verb `escalate` writes the escalation first and sends nothing if the escalation is refused (D:749, D:764), with no interrupt option."
- Provenance tag: `Variant 2 (CLAY), Section OD-7 "What it gets right" - merged per Change #2`
- Validation: consistent with the base line "What it gets right: keep the ordering rule ..." and with the OD-7 answer No.

### Change 3: Record build conditions for a later N7
- Status: applied
- Target: Summary, OD-7 clause
- Before: "OD-7 closed unless the owner asks (needs a contract exception written like S6's, a rule that suppresses the L2 nudge afterwards, and the U40 receipt check)"
- After: "OD-7 closed unless the owner asks. To reopen it: (a) a contract exception written like S6's (WC:63, WC:124); (b) the five coordinator-spec changes C25 to C29 (D:925-928); (c) a rule that suppresses the L2 nudge after an interrupt (WC:164); (d) a check whether `--interrupt` has its own receipt, because U40 (D:1298) covers text sends only."
- Provenance tag: `Variant 2 (CLAY), Section OD-7 Fact 3 (D:925-928) - merged per Change #3`
- Validation: item (b) agrees with the five-places statement in Change 1; items (a), (c), (d) match OD-7 Facts 1 to 3. The summary was split into one paragraph per clause for the longer text; wording of the plan text is verbatim.

### Change 4: Soften "not possible" to "trigger not present", add K13
- Status: applied
- Target: OD-8, "Risk of No"
- Before: "a double claim by two logins or hosts, not observed and not possible on the present single-host topology."
- After: "a double claim by two logins, two users or two hosts. The trigger is not present on the settled one-host topology (D07) and none has been observed. The design itself rates the risk medium likelihood, medium impact and names the lease as its mitigation (K13, D:1235), so the reserve rests on the absent trigger, not on a small risk."
- Provenance tag: `Base (original, modified) - Change #4`
- Validation: the phrase "not possible on the present single-host topology" no longer appears in the document body (it appears only inside a provenance comment that names the change). Consistent with OD-8 Fact 2 and the reserve trigger.

### Change 5: Narrow the `marker_in_window` defence
- Status: applied
- Target: OD-8, Fact 4
- Before: "The owner's line has its own defences: create-once claim files on a shared branch (Q26) and the claim-marker guard `marker_in_window` (D01 item 4)."
- After: "The owner's line has the create-once claim files on a shared branch (Q26) and the claim-marker check `marker_in_window` (`src/superclaude/cli/issue_watch/predicates.py:279-293`, D01 item 4). The marker check counts an own-login claim marker only after the claim exists, so it does not close the window before the marker is posted."
- Provenance tag: `Variant 2 (CLAY), Section OD-8 Fact 4 and orchestrator check of predicates.py:279-293 - merged per Change #5`
- Validation: new file:line citation comes from the plan text; not re-read by the executor (no read access to the code was in scope). Consistent with the "What it gets right" line that the race is real.

### Change 6: Reserve persisted names and the marker, note the stale-rule design task
- Status: applied
- Target: Summary, OD-8 clause
- Before: "OD-8 reserved with the trigger "a second host or a second user runs a poll" plus a stale-lease rule and marker `sc:coordinator:lease`"
- After: "OD-8 reserved. Trigger: a second host or a second user runs a poll. Before building: a stale-lease rule (a time-based rule would give up the "no clock agreement between hosts" property D:113 names, so this is a design task; orchestrator inference); the marker renamed `sc:coordinator:lease` (D08); the state step names `plan_rechecked`, `lease_posted`, `claim_started`, `claim_done` (D:547) reserved so a later build needs no migration; test T4 rewritten."
- Provenance tag: `Variant 2 (CLAY), Section OD-8 Fact 4 (D:547) and D:113 - merged per Change #6`
- Validation: trigger, stale-lease rule and marker rename match OD-8 Facts 5 and 6; the marker name is the same as in the base.

### Change 7: OD-9 hybrid and cheap checks
- Status: applied
- Target: OD-9 closing paragraph (after "What it gets right") and Summary, OD-9 clause
- After (appended verbatim in both places): "If the owner ever turns the streams on, enable `could_assign` alone: `mention` and `affects` are subsets of `involves`. The two unproven assumptions behind OD-7 and OD-9 are cheap, read-only checks: U8 is three searches (D:137) and U40 is `orca terminal send --help` plus one local send (D:1298). Run them before the owner decides on a later build."
- Provenance tag: `Variant 2 (CLAY), Section OD-9 (C-007 hybrid, A-001 cheap checks) - merged per Change #7`; summary clause tagged `Base (original, modified)`
- Validation: consistent with OD-9 Facts 1 to 3. The base summary clause "OD-9 off until the U8 live capture, then an owner decision." is kept before the appended text. The text appears twice (OD-9 section and Summary) because the plan targets both places.

### Change 8: Add the detector gap
- Status: applied
- Target: OD-8, inserted after "What it gets right"
- After: "Known gap: no rule notices that a second host or user has started a poll, so the trigger depends on someone remembering (no detector found; UNVERIFIED that none exists elsewhere). Writing the trigger into the spec and the runbook is the minimum."
- Provenance tag: `Variant 2 (CLAY), Section OD-8 weakness 4 (detector gap) - merged per Change #8`
- Validation: carries the UNVERIFIED marker as the plan requires; consistent with the reserve and trigger wording.

## Post-Merge Validation

### Structural
- Heading hierarchy: one H1, then H2 sections Claim, OD-7, OD-8, OD-9, Summary of what is kept, in the base order. No gaps, no H3 or deeper.
- The "Facts:" numbered lists keep their numbering (OD-7 Facts 1 to 7, OD-8 Facts 1 to 6, OD-9 Facts 1 to 5).
- Provenance: 3 header comments, 18 source tags. No em dashes in the document (grep: none).
- Result: pass

### References
- Internal references ("OD-7", "OD-9", "OD-8 Facts", D07, D08, K13, T4, U8, U40) resolve to a section of the document or to an external ID defined in the base Terms line or used as in the base. New IDs from the plan (K13, C25 to C29, WC:63, WC:124, plan_rechecked and the other step names) are cited only as the plan gives them.
- The file:line citations not touched by a change are unchanged (for example `WORKER-CONTRACT.md:63`, `:152`, `WC:164`, `collect.py:200-209`, `claim.md:43`, `github.py:100`, `:171-176`, `cycle.py:931`, `:1644`, `wake.py:149`, D:1298, D:137, D:123, D:113, D:543-547, D:708).
- Not independently verified against source files (outside this task): `predicates.py:279-293`, D:925-928, D:1235, D:547 and WC:131-138 come from the plan.
- Result: pass

### Contradictions
- The three answers are unchanged: OD-7 No, OD-8 No (reserve), OD-9 No (off).
- "never interrupt" no longer appears; "not possible on the present single-host topology" no longer appears in the body.
- OD-7 Fact 1 ("no contract text authorizes a second interrupt") agrees with Change 3 (a contract exception is a condition to reopen).
- The OD-8 Risk of No (trigger absent, risk rated medium by the design) agrees with the reserve and Known gap lines.
- OD-9 "off" agrees with the appended "if ever turned on, enable `could_assign` alone".
- Result: pass, no new contradictions found

## Summary
- Planned: 8
- Applied: 8
- Failed: 0
- Skipped: 0
