# Diff Analysis: Tier-2 reviewer card comparison (Mode A)

## Metadata
- Generated: 2026-11-08T18:35Z
- Variants compared: 2 (reviewer-1-card.yaml, reviewer-2-card.yaml)
- Plan under review: .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md (266 lines)
- Audited against: source.md (1 line) and .dev/issues/442/observation-runbook.md
- Calibrations applied: reviewer-1-calibration.yaml (C=0.75, plan-line citations systematically shifted ~40-60 lines low, runbook citations exact); reviewer-2-calibration.yaml (C=0.67, QA-1 whole-plan claim under-grounded); artifacts/t1-calibration.yaml (C=0.61)
- Total differences found: 27 (structural 3, content 9, contradictions 4, unique 15 treated as finding rows, shared assumptions 3 — unique contributions are enumerated per-card in the merged rows of merged-verdict.yaml)

## Structural Differences

| # | Area | Variant 1 (R1, analyzer persona) | Variant 2 (QA, qa persona) | Severity |
|---|------|----------------------------------|---------------------------|----------|
| S-001 | Finding schema | 14 findings, each with id/category/severity/claim/citation/recommendation; severity scale blocking+minor | 4 findings, same schema; all severity=blocking, no minor tier used | Medium |
| S-002 | Self-audit section | Long, itemized against real files (runbook ranges, guard script, fixtures) | Short, procedural; explicitly declines to re-check the cleanup store comparison | Low |
| S-003 | Citation granularity | Dual citations (plan + runbook) per finding; 7 plan ranges mislocated per calibration | Dual citations; ranges broad (134-161, 240-264) but containing the load-bearing lines | Low |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Coverage focus | Driver mechanics (stop conditions, start directory, dialog answering), Task 8 step coverage, runbook edit correctness, authorization, secret exposure | Wait semantics for background notices, gate enforcement before each governed subcommand, gated-outcome satisfiability, evidence classification tests | Medium |
| C-002 | Verdict derivation | FAIL from 7 blocking findings | FAIL from 4 blocking findings | Low |
| C-003 | Severity philosophy | Differentiated (blocking vs minor) | Undifferentiated (all blocking) — calibration flags this as a grading weakness | Medium |
| C-004 | Store-diff gap (R1-F03) | Filed blocking: diff not scripted, baseline deleted by step 7 | Not filed; self-audit states Task 8 step 2 "already contains that comparison" | High |
| C-005 | Authorization ambiguity (R1-F13) | Filed minor: issue/PR creation not literally covered by owner line | Not examined (calibration lists it as a QA risk-surface miss) | Medium |
| C-006 | Citation discipline | Plan citations shifted ~40-60 lines low on 7 findings; runbook citations exact | Plan citations accurate but broad | Medium |
| C-007 | Driver stop conditions | Blocked-line baseline absent (R1-F01) | Notice-wait absent (QA-1) — two distinct defects in the same `send` wait block (plan 70-75) | Medium |
| C-008 | Gate before governed sessions | Not examined as a per-subcommand gate | QA-2: item-5 gate not checked before `c` | Medium |
| C-009 | Live-run acceptance coherence | Not examined | QA-3: PR-dependent ACs unsatisfiable when gates correctly skip session E | High |

## Contradictions

| # | Point of Conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Does any script run the store-versus-baseline diff? | R1-F03: no; the plan:263 criterion is not built into any script and step 7 deletes the baselines | Self-audit: "Task 8 incorporates runbook cleanup step 2, which already contains that comparison" | High — resolved by evidence: runbook:796-804 step 2 removes only `>` lines (the comparison exists as removal logic) but no task prints the diff result the plan:263 AC demands, and the pending diff (runbook:800) appears nowhere in the plan. Both narrowly right; R1-F03 confirmed in the T1-calibrator's narrowed form. |
| X-002 | Severity of a missing per-subcommand gate | R1 treats comparable enforcement gaps as blocking (F07) | QA-2 filed blocking; its own calibration says "arguably high rather than blocking" | Medium — resolved: QA-2 downgraded to minor because plan:156 checks item 5 before `b`, which precedes `c` in the Task 10 order (plan:240); the gap is defense-in-depth for independently invoked `c`. |
| X-003 | Severity of secret-scan/staging exposure | R1-F12 filed minor | (No QA position; R1 calibration argues blocking "consistent with how F07 is treated") | Medium — resolved: raised to blocking; screens are saved unconditionally (plan:74-75), the scan has 4 patterns, and `git add .dev/tasks` (plan:259) stages unconditionally. |
| X-004 | Is item 5 blocked on a needs-reading mark? | R1-F14: claims PASS "may depend on a needs reading mark" (plan:139) | No position | Medium — resolved against R1-F14: the needs-reading list (plan:183) is explicit and excludes item 5; the cited plan lines (114, 139, 199) are unrelated. Dropped. |

## Unique Contributions

Enumerated as the 18 merged finding rows in merged-verdict.yaml: R1-F01..R1-F14 (14, unique to Variant 1) and QA-1..QA-4 (4, unique to Variant 2). Value assessment is carried by the final severity in each merged row.

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both cards cite the plan text as the only artifact (scripts do not yet exist) | The plan's prose will become scripts faithfully enough that prose gaps are real defects | UNSTATED | Yes — [SHARED-ASSUMPTION] diff point; both verdicts depend on it. Verified plausible: the plan is a workflow-plan whose tasks are script specifications. |
| A-002 | Both cards treat runbook section 3.1 order (plan:240) as binding | Task 10 runs the scripts in the fixed order setup → a → a2 → evidence → setup-github → b,c,d,e | STATED (plan:240) | No |
| A-003 | Both cards treat the runbook as normative over the plan | A plan step lacking its runbook counterpart's behaviour is a gap | STATED (plan:134 "follows its runbook section in order"; plan:199 "steps 1 to 8 ... in that order") | No |

A-001 is accepted by both advocate roles (ACCEPT/ACCEPT); it survives as the licensing assumption for every prose-level finding.

## Summary
- Total structural differences: 3
- Total content differences: 9
- Total contradictions: 4
- Total unique contributions: 15 sections consolidated into 18 per-finding rows
- Total shared assumptions surfaced: 3 (UNSTATED: 1, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: X-001, C-004, C-009 (High)
- Similarity check: differences well above the 10% threshold; debate proceeds.
