# Diff Analysis: Pre-execution review card comparison (reviewer-1 haiku/analyzer vs reviewer-2 opus/qa)

<!-- stub: sections appended below, one at a time -->

## Metadata
- Variant 1: reviewer-1-card.md (haiku-class, persona analyzer), 6 findings (F1-F6), copied to variant-1-original.md
- Variant 2: reviewer-2-card.md (opus-class, persona qa), 9 findings (F1-F9), copied to variant-2-original.md
- Target under review: .dev/tasks/to-do/TASK-WF-loosenBlockerCla-20261115-133045/TASK-WF-loosenBlockerCla-20261115-133045.md (465 lines, 39 tasks); citations "plan:N" are line numbers in it
- Focus: correctness, coverage, deviation-classification
- Mode A, depth standard

## Structural Differences

| # | Area | Variant 1 (haiku/analyzer) | Variant 2 (opus/qa) | Severity |
|---|------|----------------------------|---------------------|----------|
| S-001 | Header / path legend | Citation legend at the top (lines 1-5): maps "plan", "spec", "plan-input" to full paths | Path note at the bottom (line 42), also lists 09-plan-input, 06-blocker-characteristics, 04-historical, 08-test | Low |
| S-002 | Severity spread | All 6 findings MAJOR and blocking true | 7 MAJOR blocking true, 2 MINOR blocking false (F8, F9) | Medium |
| S-003 | Citation basis | Cites plan and spec lines only (plan:N, spec:N, plan-input:N) | Also cites live repo files read by the reviewer (rf-qa-qualitative.md:240, hooks.json:173, fmea_classifier.py:304, remediate_parser.py:55) | Medium |
| S-004 | Checked section | 5 bullets; bullets 3 and 4 make positive claims that V2 findings dispute | 8 bullets, each tied to a file:line or Grep | Medium |
| S-005 | Self-report | confidence 0.92, notes "Static review only" | confidence 0.80, no static-only note | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Registry rows set to v2 for files with no digest | Two findings: F2 (document_review_loop_prompts.md, pointer plus ledger sentence only, plan:419 vs plan:237) and F3 (task skill row Task 11 never creates, plan:361, no digest insertion in Task 30) | One finding, F2, covers both files (plan:146, 361, 416, 419, 237) | Low (same defect) |
| C-002 | Canonical rule.md vs the T2 reverse scan | F1: Task 7 creates a fenced digest in rule.md, Task 11 does not register it, so Task 19 T2 rejects it (plan:237, 104, 146) | Not raised | Medium |
| C-003 | Final-gate sweep wiring | F4: sweep (Task 20) wired into tech-research (Task 22) but not the task skill (Task 21, Task 30) (plan:250, 261, 273) | Not raised | High |
| C-004 | Owner checkpoint between stage 0 and stage 1 | F5: "Phases 1 to 3 ... one pass" (plan:20) skips the owner go required by spec stage 1 (spec:945, 940) | Not raised | High |
| C-005 | Fresh-findings second evaluation | F6: no task evaluates findings outside the 318 (plan-input:16) | Not raised (V2 F4 and F6 touch classifier and seeded-recall measurement, different gaps) | Medium |
| C-006 | Task 33 merge-rule scan allow-list | Not raised | F1: allow-list omits code files containing the phrases (fmea_classifier.py, remediate_parser.py) | High |
| C-007 | rf-qa-qualitative.md fail-by-label bullets | Not raised | F3: 7 PASS/FAIL bullet pairs not touched by Task 28 or found by Task 1 patterns | High |
| C-008 | Classifier inputs and row counts | Checked bullet 3 says code-input restrictions are explicit (plan:23, plan:197) | F4: no acceptance check enforces them; row-count report missing (09-plan-input.md:15) | Medium |
| C-009 | Per-run offer in tech-research | Not raised | F5: Task 22 omits the offer spec stage 2 requires (plan:273, spec:946, 323) | High |
| C-010 | Seeded-recall set and false-negative audit | Not raised | F6: no task builds the spec 8.3 planted set or the 8.2 audit (plan:20, spec:947, 987) | Medium |
| C-011 | Acceptance checks pinned to line numbers or a missing path | Not raised | F7: line pins shifted by the task's own edit (Tasks 21, 22, 26) and hooks/hooks.json at the repo root | High |
| C-012 | Task 24 pin on pragmatic.md lines 225-231 | Checked bullet 4: "bounded to before Task 26", sound | F8 (MINOR, non-blocking): goes red at Task 26, no task retires it | Medium |
| C-013 | Wording slips | Not raised | F9 (MINOR): "exactly the 11 carriers" vs 18 rows; Task 33 names Task 34 as trimming the allow-list | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is the Task 24 pin on pragmatic.md lines 225-231 sound? | Checked: "Legacy pin is bounded to before Task 26" (plan:299) | F8: plan:295 pin "unchanged" goes red at Task 26; Task 31's list (plan:372) omits it | Medium |
| X-002 | Are the classifier input restrictions sufficiently enforced? | Checked: "Code-input restrictions and classifier authority remaining off are explicit, plan:23 and plan:197" | F4: Task 16 reads "findings plus a judge answers file" (plan:203) and Task 14 acceptance has no gating check (plan:183) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | F1: canonical rule.md is not a registry row yet carries a fence opener (T2 conflict) | Medium |
| U-002 | V1 | F4: sweep not wired to the task skill (GR7 only half-applied) | High |
| U-003 | V1 | F5: owner-go checkpoint skipped by the one-pass instruction | High |
| U-004 | V1 | F6: fresh-findings evaluation unscheduled | Medium |
| U-005 | V2 | F1: Task 33 scan fails on code files, evidence from live repo | High |
| U-006 | V2 | F3: rf-qa-qualitative fail-by-label bullets left untouched | High |
| U-007 | V2 | F4: classifier input gating and row counts missing | Medium |
| U-008 | V2 | F5: tech-research offer missing | High |
| U-009 | V2 | F6: seeded recall and audit unbuilt | Medium |
| U-010 | V2 | F7: line and path pins unpassable after own edits | High |
| U-011 | V2 | F8: Task 24 pin red at Task 26 | High |
| U-012 | V2 | F9: two wording slips | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both cards grade unpassable acceptance checks as blocking (V1 F1-F3, V2 F1, F2, F7) | The executor and the per-task QA run each acceptance check literally, so a check that cannot pass on correct work stalls or forces a deviation | UNSTATED | Yes |
| A-002 | Both cards cite "plan:N" lines | The plan file has not changed since the reviewers read it, so cited line numbers still point at the quoted text | UNSTATED | Yes |
| A-003 | V1 F5, V2 F5, V2 F6, V2 F4 all measure the plan against the spec | The spec (merged-requirements.md) overrides the plan wherever they differ, and a plan departure from the spec is a defect not a decision | UNSTATED | Yes |
| A-004 | V1 F2 and V2 F2 agree on T1 failing for a pointer-only file | Registry test T1 applies to every registry row including own-scale rows (spec REQ-28 states "every row's file holds exactly one digest") | STATED (spec:726) | No |

### Promoted shared-assumption diff points

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | Acceptance checks are executed literally | Decides whether C-001, C-002, C-006, C-011 are blocking | Open for debate |
| A-002 | Cited plan line numbers are current | Decides citation verification for every kept finding | Verified by orchestrator: plan:237, 261, 273, 295, 361, 394, 416, 419 match the quoted text on 2026-11-15 |
| A-003 | Spec outranks plan | Decides C-004, C-005, C-009, C-010 | Open for debate |

## Taxonomy tags (AD-5)

| Level | Diff points |
|-------|-------------|
| L1 surface | S-001, S-005, C-013 |
| L2 structural | S-002, S-003, S-004, C-003, C-005, C-006, C-007, C-008, C-009, C-010 |
| L3 state mechanics (guard, validation rule, transition, invariant) | C-001, C-002, C-004, C-011, C-012, X-001, X-002, A-001, A-002, A-003 |

## Summary
- Total structural differences: 5
- Total content differences: 13
- Total contradictions: 2
- Total unique contributions: 12
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Total diff points for convergence (S + C + X + A): 5 + 13 + 2 + 4 = 24 (A-004 is STATED and not promoted; denominator counts the 3 promoted: 5 + 13 + 2 + 3 = 23)
- Highest-severity items: C-003, C-004, C-006, C-007, C-009, C-011
- Variants substantially identical check: no (the two cards share one defect cluster, C-001, and nothing else)
