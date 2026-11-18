# Diff Analysis: reviewer cards for TASK-WF-blockerStage2-20261116-030156

Variants: V1 = reviewer-1 (analyzer, sonnet class), V2 = reviewer-2 (qa, haiku class), V3 = reviewer-3 (refactorer, opus class). Finding ids R1-n, R2-n, R3-n. PLAN, SRC, PSPEC, S0, S1 as defined in the cards. Each point carries a taxonomy level (L1 surface, L2 structural, L3 state mechanics).

## Metadata

- Generated: 2026-11-16 (orchestrator, inline analytical pass)
- Variants compared: 3
- Total differences found: structural (2), content (10), contradictions (3), unique (5), shared assumptions (4)
- Debate denominator (S + C + X + A): 19 diff points

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Card layout | bold-id bullets, "Smallest fix" line | H3 blocks with "Literal execution correct?" line | H3 blocks, "Executor would / Fix" lines | Low | L1 |
| S-002 | Check against the earlier review (F6, F7, F8) | explicit section "Earlier review findings" | none | none | Low | L1 |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Skills told to call code that has no command (sweep, follow-up writer, safety route) | R1-1 blocking: add `review sweep` command, name commands in Task 2 | not raised | R3-1 blocking: new task before Task 2 creating subcommands; cites CLAUDE.md:95 | High | L2 |
| C-002 | `--unattended` branch of the offer and the three halts | R1-2 blocking | not raised | R3-3 blocking | High | L3 |
| C-003 | Safety-miss count cannot be computed from ledgers | R1-3 blocking: `--confirmed-misses` input | R2-1 blocking: name a confirmation artifact | not raised | High | L3 |
| C-004 | Task 6: how 3 agents x 3 replicates become judge verdicts, and blindness of agents | R1-5 minor: each agent its own judge id, blind table only | not raised | not raised | Medium | L2 |
| C-005 | Stage 3 entry sentence omits "no capture failure" | R1-6 minor | R2-2 minor | not raised | Low | L1 |
| C-006 | Existing tests that pin the edited skills not run by Tasks 2 and 3; no no-edit diff check | not raised | R2-4 minor (prompt-overrides test) | R3-6 minor (prompt-overrides, worker_contract, `git diff --stat`) | Medium | L2 |
| C-007 | Consolidation points and halts that reach the ledger and the offer: phase gate, Post-Completion Step 3, fidelity Step 4, halts ordered by a tech-research task-file item | R1-8 minor | not raised | R3-8 minor | Medium | L2 |
| C-008 | Task 1 owner-go and stage 1 checks are acceptance lines, checked after the body edits `src/` | not raised | not raised | R3-5 minor | Low | L3 |
| C-009 | Sweep has no input contract (ledger path, deliverable, kind, decision-basis sections) | not raised | dropped (T1-8a: spec supplies the mapping) | R3-7 minor | Medium | L2 |
| C-010 | Request span SRC:3 (ledger rows hold package ids) and SRC:13 (`stage0b-sample.md`) not matrixed or read | R1-7 (partly: names the sample file) | R2-3 minor | R3-4 (partly) | Low | L2 |

## Contradictions

| # | Point of conflict | V1 | V2 | V3 | Impact | Level |
|---|---|---|---|---|---|---|
| X-001 | Live shadow judge never named, so "shadow agreement" is empty or trivially 1.0 | R1-4 minor | not raised | R3-2 blocking | High (grade) | L2 |
| X-002 | Task 6 inputs: master-table, consensus, `stage0b-sample.md`, `@E2` rows via git | R1-7 minor | R2-3 minor | R3-4 blocking | High (grade) | L2 |
| X-003 | PLAN:20 "old definition still decides every gate outcome" versus GR12 making the safety route live | not raised | dropped: wording only, GR12 explicitly required | R3-3 (part): reword PLAN:20 | Low | L2 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V3 | `@E2` rows cannot be resolved by the disk-only inputs supplier (S1:148, S1:153), so those rows are UNSET | Medium |
| U-002 | V1 | PLAN:22 omits the SRC:19 no-edit list (rf-qa.md, rf-qa-qualitative.md, rf-analyst.md, templates, rule prompts) | Medium |
| U-003 | V3 | CLAUDE.md:95 rule: installed primitives reach package behaviour through the `superclaude` CLI | High |
| U-004 | V2 | Each finding states whether a literal executor would still be correct | Low |
| U-005 | V1 | F6, F7, F8 of the earlier review checked against this plan (F6 resolved, F7 resolved apart from inputs, F8 partly) | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | `/sc:implement` executes tasks literally and checks only the acceptance lines as written | all three judge by "what a literal executor would do" | UNSTATED | yes |
| A-002 | The stage 0 and stage 1 packages will be built as their plans say (file names, modules, commands) when this package runs, although neither has run and stage 0's review says NEEDS-REVISION | all three cite S0 and S1 as if they were facts | UNSTATED | yes |
| A-003 | Tasks 4 (worker-contract keys) and 5 (brief pin test) are sound; no card examines their acceptance lines in depth | V1 and V3 never mention Task 5; V2 mentions neither Task 4 nor 5 | UNSTATED | yes |
| A-004 | Reviewer labels under the old definition (blocking, minor, CRITICAL, IMPORTANT, MINOR) can be placed into the ledger tiers Medium and Note in stage 2 (through the stage 1 scale map), so the ledger gets rows at all | no card asks how a shadow-stage ledger row gets its tier | UNSTATED | yes |

## Summary

- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 4, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, X-001, X-002
- Level counts: L1 = 3 (S-001, S-002, C-005), L2 = 11, L3 = 5 (C-002, C-003, C-008, A-002, A-004)
