# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (Proposal A; `adversarial/variant-1-original.md`)
- Incorporating strengths from: Variant B (Proposal B; `adversarial/variant-2-original.md`), the agreed Round 2 hybrids (`round2-advocate-A.md` "Proposed merged resolution", amended by `round2-advocate-B.md`), and the Round 2.5 invariant probe (`invariant-probe.md`)
- Merged output path: `<output>/merged-output.md` (here `.../consumer-entry-effect-and-delivery/merged-output.md`)
- Planned changes: 16
- Risk level: Medium overall (the merge rewrites the effect and reach statements of the base and adds an open-conditions section; no new claims beyond the debate)
- Rule for the merge-executor: the merged file states only what the transcripts, the diff analysis, the probe and the two variants already contain. It adds no new evidence, no new file:line citation and no new recommendation. Where the debate left a point open, the merged text records it as open with the invariant ID. The merged file never mentions or cites `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`.
- Source key: `A-Sec N` = a section of `variant-1-original.md`; `B-Sec N` / `B-E<n>` = a section or evidence item of `variant-2-original.md`; `R2A` / `R2B` = `round2-advocate-A.md` / `round2-advocate-B.md`; `INV-nnn` = `invariant-probe.md`.

## Planned Changes

### Change 1: Restate the position as three separable parts (from Variant B)
- **Source**: Variant B, Sec 1 and Sec 8 item 4; debate S-002 (B won, 88%)
- **Target**: Base, Sec 1 (restructure)
- **Rationale**: Both advocates' final verdicts adopt the three-part structure: entry, effect, delivery, each with the argument that carries it. A's one-paragraph bundle is replaced by three labelled parts plus the merged one-line decision for each.
- **Integration point**: Sec 1 keeps A's headline (reflect UC-1 stays the only entry this release) and gains three labelled sub-parts: Entry (A wins C-001), Effect (Hybrid, C-002), Delivery (A wins C-003).
- **Risk**: Low, restructuring of one section.

### Change 2: Correct the effect statement for Stage 10.5 (probe INV-001, INV-002)
- **Source**: INV-001, INV-002 (HIGH, UNADDRESSED); A-Sec 3 item 2 and B-E2 already name the `needs_human_decision` halt
- **Target**: Base, Sec 1, Sec 2 (rows for Stage 10.5), Sec 3 item 2, Sec 8 objection 1 (modify)
- **Rationale**: The agreed consensus said "advisory at Wave 4 and Stage 10.5". The probe shows Wave 4 is advisory with no halt, while Stage 10.5 is labelled "advisory-blocking" (`sc-tasklist-protocol/SKILL.md:1640-1646`): `needs_human_decision` halts, under `--unattended` the run ends `blocked`, and `--remediate` is a write path that can nest reflect, workflow and reflect. The merged text states this precisely and records the engine-switch effect on those paths as unmeasured and open.
- **Integration point**: replace "advisory at generation time" by "Wave 4 advisory; Stage 10.5 advisory-blocking (bundle ships regardless of verdict; halt and unattended `blocked` on `needs_human_decision`; `--remediate` write path)". Keep A's evidence lines.
- **Risk**: Medium, changes a headline claim of the base; it is a correction the debate's own probe produced.

### Change 3: Add a "Reach" part (from Variant B and R2A/R2B)
- **Source**: B-E4, round1-advocate-B strength 1, R2A "Responses" item 1, R2B item (i); probe INV-003, INV-005, INV-006; debate C-004 (Hybrid, 88%)
- **Target**: Base, new Sec 3a "Reach behind reflect" placed after Sec 3 (insert); and Sec 8 objection 2 (modify)
- **Rationale**: A's strength 6 (low-complexity phases are the lowest risk) is narrowed: reflect's default depth is `standard`, so workflow Wave 4 reaches a panel only on rubric escalation and tasklist reaches it only on forced-deep phases and rubric escalations; a rubric stop never reads the engine; with `legacy` a rubric escalation never calls the panel; `--budget-remaining` downgrades are a second limiter. The reach share is unmeasured.
- **Integration point**: new subsection with the reach chain and the statement "unsized". Record the probe conditions: the depth-policy remedy changes remediation route and forces Tier 2 on the legacy engine at Wave 4 (INV-003); a call-site depth flag needs both workflow trees edited (INV-004) and the phrase "defaults for every other flag" reworded; the denominator rule for the share is unset (INV-006).
- **Risk**: Medium, adds a section; every statement traceable to R2A, R2B or the probe.

### Change 4: Invariant table with per-row verdicts (from Variant B)
- **Source**: B-Sec 5; debate S-003 (B won, 85%); probe INV-007, INV-008, INV-012
- **Target**: Base, Sec 5 (restructure)
- **Rationale**: Replace the "Preserved" column by "Keeps / Keeps with a cost / Endangers" per row. Carry B's INV-J (Endangers for a later revise loop) and INV-G (a plugin reviewer agent must be the read-only kind) rows. Correct INV-K: the three diff-based fence tests are working-tree guards, the content pins in the same test file are standing, and the Stage 3 edit must update them (INV-012).
- **Integration point**: one table, rows INV-M, INV-B, INV-N, INV-K, INV-J (slot invariants) then INV-A, INV-C to INV-L as in A and B. Withdraw A's "the fence test must be changed" wording in favour of the INV-012 wording.
- **Risk**: Medium, touches the invariant claims.

### Change 5: Return-contract statement corrected and extended (INV-M)
- **Source**: R2A item (ii), R2B concession 1; B-E8; probe INV-007, INV-008, INV-009, INV-014 F3
- **Target**: Base, Sec 2 (row for reflect UC-1 and the workflow Wave 4 row), Sec 5 INV-M row (modify)
- **Rationale**: Delete "the panel verdict reaches consumers only as `status`, `coverage_pct`, `tier_reached`". State instead: consumers also read `needs_human_decision`, `unmapped_requirements`, `run_id` and `report_path`; `coverage_pct` and `tier_reached` are fixed before the engine is read, so only `status` and the report and gap fields can carry a panel effect; the panel-to-status map is not pinned (INV-011) and a short or refused panel stays inside the closed enum (INV-009). Replace "four readers" by "at least the four skill readers, one closed-enum validator and the tests" (INV-008). Keep: additive keys with `contract_version` staying "1.1" are safe at the three consumer-side readers (INV-014 enumeration); the 1.1 to 1.2 bump is wrong.
- **Integration point**: Sec 2 rows and Sec 5 INV-M row.
- **Risk**: Medium.

### Change 6: Engine-switch statement (C-006, INV-008, INV-010, INV-011, INV-012)
- **Source**: R2A item (v) and bullets 2 and 7; probe INV-008, INV-010, INV-011, INV-012; B-E5, B-E13
- **Target**: Base, Sec 3 item 8 and Sec 8 objection 3 (modify)
- **Rationale**: One reflect-side switch is a prose edit in three places of the reflect skill with no staged selector reachable from a consumer call; it flips every UC-1 caller (task-builder PRE gate, auggie-review, troubleshoot handoffs); shadow-first doubles Tier-2 reviewer spend on consumer escalations; reflect-owned tests change at Stage 3 (the content pins; the remediation route table if depth policy changes). The contract-compat test against the 36-test matrix is necessary, not sufficient, until the panel-to-status map is defined (INV-011). Gate stays: replay, contract-compat test, headless smoke run.
- **Integration point**: replace the base's "one controlled change" sentence with these statements.
- **Risk**: Medium.

### Change 7: Lens statement (C-007)
- **Source**: B-E7 (weak per round1-advocate-B concession 2), R2A concessions item 6, R2B item (v)
- **Target**: Base, Sec 2 (add one row) (insert)
- **Rationale**: Wave 4 and Stage 10.5 use the `reflect-pre` lens; the five Stage 7 dimensions apply only to a Stage 7 reviewer feed, which is net-new code with no code home today (`findings_v2.py:36`; no `tasklist` or `effect` match in `cli/review`).
- **Integration point**: one table row in Sec 2.
- **Risk**: Low.

### Change 8: Relation to Stages 6-10 (C-008, X-001)
- **Source**: B-E3, R2A "Responses" (iv), R2B item (iii); debate X-001 (Hybrid, 90%)
- **Target**: Base, Sec 2 (row for Stages 6-10) and Sec 8 objection 1 (modify)
- **Rationale**: Generation-time blocking already exists in Stages 8-10 (`sc-tasklist-protocol/SKILL.md:1604-1615`). A call-site direct call adds no loop. A Stage 7 reviewer-feed swap changes the evidence base of that block, touches the P2 pins and halt strings, and is a separate later module. Replace A's "a direct call would add a new revise loop" wording.
- **Integration point**: rewrite the two passages; keep A's pin citations (`tests/tasklist/test_tasklist_cli.py:568-580`).
- **Risk**: Medium.

### Change 9: Workflow Wave 4 and "door open" for later direct modules (C-009, C-005, X-003)
- **Source**: B-Sec 3 (entry shape, `plan-review`), B-E1, R2A bullet 5, R2B amendments to bullets 5, 8, 9; probe INV-014 F3
- **Target**: Base, Sec 2 (workflow row) and a new Sec 9a "What a later direct module needs" (insert)
- **Rationale**: Wave 4 stays one advisory Skill call; Will Not at `sc-workflow-protocol/SKILL.md:107` stays true. A later direct module (a Stage 7 reviewer feed, a Wave 4 `plan-review`) is possible with `effect` as module data and needs: additive keys with `contract_version` "1.1" and `reflect_*` unchanged; the `artifacts` rule (`refs/return-contract.md:52`) and nested-kind constants (`tests/skills/test_worker_contract.py` `EXPECTED_NESTING`, `UNATTENDED_EXPECT`) edited by hand; companion-eval allow-list and staging edited; a parity test per added plugin file; a Wave 4 `plan-review` edits both workflow trees; its own replay. B's costs for the module (C-02 INV-001/002/003, C-03 INV-007, INV-J) are listed.
- **Integration point**: the new section lists these as conditions, not as a plan.
- **Risk**: Low to Medium; additive.

### Change 10: Plugin delivery (C-003, X-002, A-006)
- **Source**: B-E9, B-Sec 8 third objection, R2B item (iv) three-case account; debate C-003 (A won, 93%), A-006 (B won, 90%)
- **Target**: Base, Sec 3 item 9 and Sec 8 objection 4 (modify)
- **Rationale**: Keep A's "no panel-only plugin copy". Add the three-case account of what a plugin copy would deliver (CLI absent: `skipped`, nothing gained; CLI present and `superclaude install` run: redundant; CLI present, plugin-only: the only case with value, unverified), that CLI availability in a plugin-only install and `verify-sync` coverage of `plugins/` are unchecked, that a parity test per added plugin file is required because the existing pin covers `*.md` of one skill and one command, and that A's "cannot work without reflect" wording is too strong for a delegate skill that brings its own reviewer agent (withdrawn).
- **Integration point**: two passages.
- **Risk**: Low.

### Change 11: Measurement section merged (C-011)
- **Source**: A-Sec 6, B-Sec 6, R2A bullet 8, R2B amendments to bullets 4 and 8; probe INV-005, INV-006, INV-013
- **Target**: Base, Sec 6 (restructure)
- **Rationale**: Merge A's replay (6.1), routing coverage (6.2), contract-compat test (6.3) and call-site non-regression (6.4) with B's two-arm replay (arm D is the path E2 already measured, loop columns, cost column) and free checks. Arm R must be a real Wave 4 or Stage 10.5 call. Record the instrument gaps the probe found as open: no ground-truth scorer; the only aggregator globs shadow-run panel manifests and cannot see phases that never reach the panel or tasklist consumer output directories; the companion eval pool denies Bash, Agent, Task and `mcp__*`; no engine selector exists for arm R; the denominator rule is unset; a numeric reopen threshold must be registered before the first run (B asked, A did not answer).
- **Integration point**: Sec 6 gains the merged list and an "Instrument gaps (open)" list.
- **Risk**: Medium to High: the measurement is the decision mechanism of the whole merged resolution and has no instrument today (INV-013).

### Change 12: Dependence on adjudicated slots and effect on later consumers (C-010, C-012)
- **Source**: A-Sec 4, B-Sec 2, B-Sec 7; debate C-010 (A won, 94%), C-012 (Hybrid, 82%)
- **Target**: Base, Sec 4 and Sec 7 (modify)
- **Rationale**: Keep A's one-condition-per-slot text and add the reverse view: a later direct module would be a ledger consumer and carry C-02 INV-001/002/003 and C-03 INV-007. Sec 7: module-declared effect is the rule for later direct consumers (PR review, rf-qa); none is added here; the plugin gap is carried forward.
- **Integration point**: appended paragraphs.
- **Risk**: Low.

### Change 13: Shared assumptions section (A-002 to A-006)
- **Source**: diff-analysis "Shared Assumptions", both Round 2 "Shared assumption responses"
- **Target**: Base, new Sec 9b (insert)
- **Rationale**: Record the final answers: A-002 Neither (unmeasured; advisory first), A-003 Hybrid (existing `nested/reflect-<n>/` covered by the `artifacts` rule, a new kind is not; headless fan-out unrun for both), A-004 Hybrid (fail-open for advisory only; a zero-success blocking feed escalates), A-005 Neither (shared inference, not executed), A-006 B (parity test per added plugin file).
- **Integration point**: small table.
- **Risk**: Low.

### Change 14: Counter-evidence carried in the evidence list (from Variant B)
- **Source**: B-E11, B-E12, B-E13
- **Target**: Base, Sec 3 (append items 11 to 13) (insert)
- **Rationale**: B carried the evidence that cuts against its own blocking effect (0 of 8 real blocking in every pilot arm; five advisory FAIL results on real workflow plans went on to implementation; Stage 2 exit FAIL, shadow runs 13 of 20). Keep the tags as in B ([UNVERIFIED] where B marked it).
- **Integration point**: three appended evidence items with source tags.
- **Risk**: Low.

### Change 15: Withdrawn and corrected claims register
- **Source**: round1-advocate-A concessions, round1-advocate-B concessions, R2A and R2B concessions, probe "Claims in the consensus that I found FALSE or unsupported"
- **Target**: Base, new Sec 10 "Claims withdrawn or corrected in the debate" (insert)
- **Rationale**: Transparency. A: "fence test must be changed" (withdrawn), "zero pin changes" (a prediction), "only route that keeps the contract intact" (B-add can also meet it), X-002 "cannot work without reflect" (too strong), "four readers" (undercount), "switched on for both consumers with zero edits" (contradicts D1). B: contract 1.1 to 1.2 (wrong), E6 and E7 (overstated), blocking effect at Stage 10.5 (fenced), B-add as a recommendation for this release (withdrawn), pin claim for `:243-248` (an `any(...)`).
- **Integration point**: one table.
- **Risk**: Low.

### Change 16: Open conditions from the invariant probe
- **Source**: `invariant-probe.md`; status BLOCKED_BY_INVARIANTS
- **Target**: Base, new Sec 11 "Conditions under which this resolution holds, and what the debate left open" (insert)
- **Rationale**: Carry all 12 UNADDRESSED probe items with severity (7 HIGH, 5 MEDIUM), and the 3 ADDRESSED with residuals, as the conditions on the merged text. Holds-while list from R2A bullet 10: C-01 to C-03 outcomes stand; reopen if the replay shows the direct path catches materially more blocking GT items per cost not explained by depth routing, if the owner chooses plugin parity, or if blocking GT items sit in phases that never reach the panel. No convergence is claimed beyond what the debate produced.
- **Integration point**: table of INV items plus the holds-while list.
- **Risk**: Medium; this section is what turns the 24-of-24 agreement into a conditional result.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|----------------------------|
| C-001 | B-replace (swap the call at `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1630`) | Withdrawn by B's advocate; rewrites pins `test_workflow_command.py:251-261` and degrades `reflect_status` readers to `skipped`. |
| C-001 | B-add as a recommendation for this release | B's advocate withdrew it in Round 2: a second review per phase to close an unsized gap; reopen only on the pre-registered reach measurement. |
| C-002 | Generation-time blocking or a revise loop at Wave 4 / Stage 10.5 | B placed it ambiguously (Stage 10.5 is fenced); blocking use, if any, is a later Stage 7 reviewer-feed change after a replay. |
| C-003 | Plugin copy of the delegate-only skill, rules, brief and reviewer agent | No forcing element once call sites stay (B concession); delivery decided as a set after plugin CLI availability is known. |
| C-005 | Workflow contract 1.1 to 1.2 with `panel_status`, `panel_report_path` | Wrong: `scripts/eval_workflow_vs_task_builder.py:1140`, `archive_workspace.py:327` and `tests/commands/test_workflow_command.py:178` require "1.1". Later modules add keys only. |
| C-007 | `tasklist-review` and `plan-review` modules with `effect` as code | No code home today; design hypotheses until a replay. Described only as a later option. |
| C-006 | Second entry independent of reflect's engine readiness | Entry stays in reflect this release; B's independence argument is weakened because a direct skill would re-implement an orchestrator sharing the shadow-run failure modes (B Round 2). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Sec 1 reads as a bundle again | Restore A Sec 1 |
| 2 | Medium | Stage 10.5 effect misstated; consumers misread it as advisory-only | Revert to base wording, keep probe note as warning |
| 3 | Medium | Reach claim unsupported if the new section drifts from R2A/R2B | Delete Sec 3a, keep A Obj 2 |
| 4 | Medium | Invariant verdicts inconsistent with the probe | Restore A table plus probe note |
| 5 | Medium | Contract statements wrong for a later reader | Restore A wording, keep corrections as a note |
| 6 | Medium | Engine-switch cost understated | Restore A text, keep INV-008/010/011/012 as open items |
| 7 | Low | Lens claim wrong | Remove row |
| 8 | Medium | Stage 8-10 relation misdescribed | Restore A wording and note X-001 as Hybrid |
| 9 | Low | Over-specifies a later module | Remove Sec 9a |
| 10 | Low | Plugin case table claims too much | Keep "no copy" and cut the table |
| 11 | Medium to High | Measurement section implies an instrument exists | Mark all instrument gaps as open (already planned) |
| 12 | Low | None | Remove paragraphs |
| 13 | Low | None | Remove table |
| 14 | Low | Counter-evidence overstated | Remove items 11 to 13 |
| 15 | Low | None | Remove table |
| 16 | Medium | Conditions mis-transcribed from the probe | Quote probe rows verbatim |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14
