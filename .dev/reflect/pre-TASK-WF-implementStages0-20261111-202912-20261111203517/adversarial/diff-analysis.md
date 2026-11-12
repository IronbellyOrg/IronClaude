# Diff Analysis: reflect pre-execution reviewer cards (3 variants)

Variants: 1 = reviewer-1 (analyzer, sonnet class), 2 = reviewer-2 (qa, haiku class; self-report "OpenAI ChatGPT", identity mismatch suspected), 3 = reviewer-3 (refactorer, opus class).
Subject under review: plan `.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md` against spec `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`.

## Metadata
- Variants compared: 3
- Categories: structural (1), content (28), contradictions (2), unique (12), shared assumptions (4)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Same card schema (findings, lead verdicts, coverage observations, notes); V2 has no usable lead verdicts because its brief omitted the leads | 12 findings, 2 blocking | 10 findings, 7 blocking | 14 findings, 2 blocking | Low |

## Content Differences (findings by cluster)

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 10 acceptance needs Task 11's template (forward dependency) | F2 blocking | F4 blocking | L1 confirmed | Low (agree) |
| C-002 | Task 14 "clean git status" in a dirty worktree | F12 minor | F5 medium | F5 medium | Low (severity only) |
| C-003 | Task 8 byte-identity golden vs `tiers_sha256` changed by Task 9 `classes` | F1 blocking | - | - | High |
| C-004 | `ExclusionExhausted` lost by re-wrap in `resolve`; CLI prints no class name | F3 medium | - | - | Medium |
| C-005 | Task 9 reflect-profile validator has no stated caller; `--sequence` not passed | F4 medium | - | - | Medium |
| C-006 | Recorded-card format assumed idealized (Tasks 2, 4; 90% gate) | F5 medium | - | - | Medium |
| C-007 | `cluster_v2` has no input for calibrated confidence / reviewer order; calibration is a sidecar scalar | F6 medium | - | F4 medium | Medium |
| C-008 | v2 fingerprint uses `section`, undefined for citation-only findings | F7 medium | - | - | Medium |
| C-009 | Task 7 dependencies and "five exit items" but four listed | F8 medium | - | - | Medium |
| C-010 | Task 1 "every v1 block parses as v2" wrong at fence level | F9 minor | - | - | Low |
| C-011 | Task 11 never checks `reflect-lite` resolution | F10 minor | - | - | Low |
| C-012 | No task verifies the judge identity field (UNVERIFIED in spec) | F11 medium | partial in F8 | F8 medium | Medium |
| C-013 | Plan constraint "never use Opus in any new template" vs Task 11 resolving to Opus | - | F1 blocking | - | High |
| C-014 | Hand-labelled 50-pair check postponed; Stage 1 entry needs Stage 0 exit | related F8 | F2 blocking | - | High |
| C-015 | "lint test design" is a Stage 0 deliverable with no Stage 0 task | - | F3 blocking | - | High |
| C-016 | Task 20 finds shadow runs by manifest `t2_engine_effective`; no task writes it there; `panel_parity` not in 9.2 | - | F6 blocking | F1 blocking | High |
| C-017 | Task 20 does not run the contract lint (Stage 2 exit) and lacks the Task 15 dependency | - | F7 blocking | F2 blocking | High |
| C-018 | Forbidden-model filter not applied to calibrator/judge; REPORT collision note missing | - | F8 blocking | - | High |
| C-019 | Identity-mismatch comparison and restricted REPORT wording not assigned | - | F9 blocking | - | High |
| C-020 | `clusters_kept` needs a second `review cluster --kept` pass after the validator; kept-ids file undefined | - | F10 medium | F3 medium | Medium |
| C-021 | S-ID write probe cannot show whether the allowlist survives the model override | - | - | F6 medium | Medium |
| C-022 | Brief line added to `refs/reviewer-spec.md` with no shadow-only condition; YAML cards | - | - | F7 medium | Medium |
| C-023 | Task 15 EV-1 check says "equals"; real rule is "at least"; `reviewers_resolved` absent in legacy | - | - | F9 medium | Medium |
| C-024 | Task 16 legacy baseline includes shadow runs; `derive_verdict` args unspecified | - | - | F10 medium | Medium |
| C-025 | D3 effects on status/report not scoped to the `panel` engine | - | - | F11 medium | Medium |
| C-026 | Manifest publish renames `audit.log` while legacy writers stay authoritative in shadow | - | - | F12 medium (0.55) | Medium |
| C-027 | "section 4.3a" never created by Task 18; no baseline for "byte-identical" | - | - | F13 minor | Low |
| C-028 | Task 13 CLI inputs unlisted; Task 15 "derive" key list from unparseable 9.1 block | - | - | F14 minor | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Severity of the Task 14 git-status criterion | minor | medium | medium | Low |
| X-002 | Whether Stage 0-2 Cost/Risk spans lack tasks (L4) | refuted: covered by Tasks 7-11, 19, 5 | no gap reported (risk table adds no separate artifact) | refuted | Low (agree) |

## Unique Contributions
U-001 V1: C-003, C-004, C-005, C-006, C-008, C-010, C-011 (code-level checks against `panel.py`, `panel_cmd.py`, `findings.py`). U-002 V2: C-013, C-014, C-015, C-018, C-019 (spec-staging and exit-criteria coverage). U-003 V3: C-021, C-022, C-023, C-024, C-025, C-026, C-027, C-028 (cross-task coupling and exit tooling).

## Shared Assumptions

| A-NNN | Assumption | Classification | Promoted |
|---|---|---|---|
| A-001 | All three grade "blocking" as "an implementer would produce a wrong outcome or an acceptance criterion cannot be checked as written" | STATED (brief) | no |
| A-002 | The plan is executed once, in listed order, by one executor session (so a Task N acceptance may not rely on Task N+1) | UNSTATED | yes |
| A-003 | The owner will supply the 50 labels and 20 shadow runs after merge (plan Constraints line 27) | STATED | no |
| A-004 | Plan and spec line numbers cited by reviewers refer to the files as of the input snapshot (tree sha da9fb1f7...) | UNSTATED | yes |

## Summary
28 content clusters, 2 contradictions (low impact), 4 shared assumptions (2 promoted). Highest-severity items: C-003, C-013, C-014, C-015, C-016, C-017, C-018, C-019. Items found by only one reviewer and needing independent verification: C-003 to C-006, C-013 to C-015, C-018, C-019, C-021, C-022, C-025.
