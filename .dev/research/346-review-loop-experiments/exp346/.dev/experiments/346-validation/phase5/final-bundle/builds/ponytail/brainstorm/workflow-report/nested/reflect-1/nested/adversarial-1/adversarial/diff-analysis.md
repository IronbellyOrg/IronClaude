# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-11-08T18:45:06Z
- Variants compared: 3
  - Variant 1 = reviewer-1-card.yaml (analyzer, sonnet; calibrated C 0.76; 9 findings, 1 blocking)
  - Variant 2 = reviewer-2-card.yaml (qa, haiku; calibrated C 0.75; 2 findings, 2 blocking)
  - Variant 3 = reviewer-3-card.yaml (refactorer, opus; calibrated C 0.81; 6 findings, 2 blocking)
- Subject under review: `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md` (plan) against `source.md` (spec), same folder
- Input warning: the three inputs are `.yaml`, not `.md`; loaded unchanged apart from trailing-whitespace stripping (copies are `variant-N-original.md`).
- Weighting rule (from the caller): weight by calibrated C, never by self_confidence (V2 self 0.94 vs calibrated 0.75).
- Severity rule (from the caller): blocking = the plan as written delivers wrong behaviour, misses a required in-scope deliverable, or two of its acceptance criteria cannot both pass; otherwise minor.
- Total differences found: 19 (+3 shared assumptions)
- Categories: structural (3), content (11), contradictions (5), unique (6), shared assumptions (3)
- Orchestrator spot-checks done before the debate (Read/grep, 2026-11-08T18:44Z):
  - `src/superclaude/commands/spec-panel.md` is 486 lines; line 220 contains `src/superclaude/examples/release-spec-template.md` (only occurrence of `src/superclaude`).
  - Line 23 Usage carries `[--unattended] [--report-dir <dir>] [--improve]`; `--unattended`, `--report-dir` and `--improve` appear elsewhere only in `## Unattended mode` (lines 451-462).
  - `tests/skills/test_worker_contract.py::_check_no_unattended_sections` (lines 831-839) checks only the `## Unattended mode` heading set; no test checks Usage-line flags.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Finding schema | flat: id, severity, plan_task, spec_ref, evidence (string), claim_tag, recommendation, optional orchestrator_note | adds `category` (drift) and `finding`; evidence is a list of quoted lines | same flat schema as V1 | Low |
| S-002 | Coverage statement | `checked_sound` (A1-A3 judged sound) | `actively_checked` (rejects T1 Q1/Q2 as gaps) | `actively_checked` (files and line ranges read) | Low |
| S-003 | Granularity | 9 findings, many small | 2 findings, both blocking | 6 findings | Medium |

## Content Differences

Each row is one deduplicated finding cluster (candidate merged finding).

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Task 8 drift pin (variant minus enumerated differences equals spec-panel.md) vs no-`src/superclaude` pin on the variant; spec-panel.md:220 carries the string | R1-F1 blocking, confirmed | silent | silent | High |
| C-002 | Variant Usage line 23 keeps `--unattended`, `--report-dir`, `--improve` whose definitions are only in the removed `## Unattended mode` section; Task 8 checks only the heading | R1-F2 minor, confirmed | silent | R3-F1 blocking, confirmed | Medium |
| C-003 | `verdict` exit 2 for an inconsistent (DISAGREE) verdict (source.md:183) absent from Task 5 | R1-F7 minor, confirmed | QA-001 blocking, confirmed ("blocking is overstated") | R3-F3 minor, confirmed | Medium |
| C-004 | Task 3 writes DOWNGRADE lines even on CHECK_FAIL; Task 5 builds held set from every DOWNGRADE line; contradicts Task 5 AC "with the audit skipped both numbers are equal" | R1-F4 minor, confirmed | silent | R3-F4 minor, confirmed | Medium |
| C-005 | FR-8/FR-9 protection: `MAJOR (FR-8 GAP)` graded-minor test (source.md:231) absent from Task 2 AC; V3 adds: state.json records no FR-8/FR-9 marker, so K6 cannot refuse | R1-F6 minor (test only), confirmed | silent; `actively_checked` rejects T1 Q1 because Task 2 incorporates the source test bullets | R3-F2 blocking (flag + test + K6 case), confirmed | High |
| C-006 | Staging: no task stages `.dev/tasks` (and Task 9's docs file); source.md:174 says stage src/, tests/, docs/, .dev/tasks | R1-F9 (part b) minor, confirmed | silent | R3-F5 minor, confirmed | Low |
| C-007 | No-src pin omits installed `scripts/fix_audit.py` | R1-F9 (part a) minor, confirmed | silent | silent | Low |
| C-008 | Task 12 copies T10-R3-reviser, outside source.md:254 (T05-T09); owner ruling msg_2000b167e322 authorizes it | R1-F3 minor, confirmed (label reference-only) | silent | R3-F6 minor, not-confirmed (authorized) | Low |
| C-009 | Task 2 brief-comparison test reads source.md from the package folder, which moves to `.dev/tasks/done/` | R1-F5 minor, INFERRED, confirmed | silent | silent | Low |
| C-010 | Task 4 defines no recovery when readback, apply-log or closed-minor writes fail after `os.replace`; breaks "every failure path leaves the spec byte-identical" and idempotent retry | silent | QA-002 blocking, INFERRED, confirmed (calibrator: spec shares the omission) | silent | High |
| C-011 | Owner count could double-count a held id that review 3 also lists as new ("withdraws" unmapped) | R1-F8 minor, INFERRED, not-confirmed | silent | silent | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Severity of C-002 (Usage flags) | minor: "drop tokens or keep and document" | none | blocking: Task 7 must drop the tokens and Task 8 must assert `--unattended` absent | Medium |
| X-002 | Severity of C-003 (exit 2 on DISAGREE) | minor | blocking (drift) | minor | Medium |
| X-003 | Scope and severity of C-005 (FR-8/FR-9) | minor: only the test is missing | Task 2 incorporates the full source test bullets, so not a missing deliverable | blocking: data model (state.json) cannot carry the protection, so K6 cannot enforce it | High |
| X-004 | Deviation classification of C-003 and C-010 | no category | both `drift`; V2's own calibrator re-classes C-010 as a spec-plus-plan gap | no category | Medium |
| X-005 | Status of C-008 (T10 copy) | confirmed minor (labelling) | none | not-confirmed (authorized expansion) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | C-001: two Task 8 pins cannot both pass (spec-panel.md:220) | High |
| U-002 | V1 | C-009: brittle path to source.md after archive | Low |
| U-003 | V1 | C-007: fix_audit.py missing from no-src pin | Low |
| U-004 | V2 | C-010: post-`os.replace` failure recovery | Medium |
| U-005 | V3 | C-005 extension: per-id protected flag in state.json plus a CHECK_FAIL K6 case | Medium |
| U-006 | V1 | C-011: possible double count (calibrator not-confirmed) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | The owner rulings cited in the plan (msg_7b27feaade5e, Unattended removal; msg_2000b167e322, T10 copy) are genuine and binding, so findings that collide with them are authorized expansions, not drift | All three accept the Unattended removal (V1 `checked_sound` A2; V2, V3 do not challenge it) | UNSTATED (no card verified the messages) | Decides C-008 and the frame of C-002 | Promoted |
| A-002 | Severity is judged against what `/sc:implement` delivers when it follows the plan literally: its per-task QA checks the acceptance criteria (the guard), so a requirement stated only by reference to a source.md section, and absent from the AC, may not be delivered | V1 and V3 both treat AC omissions as gaps; V2 assumes the opposite for test bullets | UNSTATED (and partly CONTRADICTED by V2's `actively_checked`) | Decides the severity of C-003 and C-005 | Promoted |
| A-003 | Where the spec itself is wrong or silent, a plan that inherits the defect still counts against the plan | Calibrators note C-001 (inherited from source.md:237-239) and C-010 (spec shares the omission) yet confirm both | UNSTATED | Decides the classification of C-001 and C-010 | Promoted |

## Debate Topic Taxonomy (auto-tagged)

| Point | Level | Signal |
|-------|-------|--------|
| S-001, S-002 | L1 | formatting/presentation |
| S-003, C-002, C-006, C-007, C-008, C-009, A-001 | L2 | interface, dependency, organization |
| C-001, C-003, C-004, C-005, C-010, C-011, X-001..X-005 (inherit their topic), A-002, A-003 | L3 | validation rule, state, guard, invariant, count |

Coverage: L1 2, L2 7, L3 13. All three levels have points.

## Summary
- Total structural differences: 3
- Total content differences: 11
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0; A-002 partly contradicted by V2)
- Highest-severity items: C-001, C-005, C-010, X-003
- Similarity check: differences far above 10% of comparable items; debate proceeds.
- Convergence denominator: S(3) + C(11) + X(5) + A(3) = 22 points.
