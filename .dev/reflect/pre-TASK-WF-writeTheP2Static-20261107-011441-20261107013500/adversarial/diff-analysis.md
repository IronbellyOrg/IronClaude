# Diff Analysis: reviewer-card Comparison

## Metadata
- Generated: 2026-11-07T01:47:00Z
- Variants compared: 3 (Variant 1 = reviewer-1 card, sonnet:analyzer; Variant 2 = reviewer-2 card, haiku:qa; Variant 3 = reviewer-3 card, opus:refactorer)
- Subject: the three Tier-2 reviewer cards of the sc:reflect UC-1 review of the P2 static plan `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md` ("plan") against its brief `source.md` and the spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` ("spec")
- Calibrated card scores (blind, ../artifacts/calibration.yaml): V1 0.70, V2 0.78, V3 0.79
- Total differences found: 31
- Categories: structural (3), content (8), contradictions (2), unique (15), shared assumptions (3)
- Focus areas: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card sections | findings, self_confidence, self_audit | findings, self_confidence, self_audit | findings, verified_ok (6 negative-evidence items), self_confidence, self_audit | Medium |
| S-002 | Finding count and granularity | 10 findings (0 P1, 3 P2, 7 P3) | 5 findings (1 P1, 3 P2, 1 P3) | 14 findings (1 P1, 5 P2, 8 P3) | Medium |
| S-003 | Evidence form | plan:N and spec:N shorthand plus repo paths; some `[INFERRED]` | repo-relative paths with line numbers; one `[INFERRED]` | plan:N shorthand plus repo paths; two `[INFERRED]` findings | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | cli-eval `run` safety-flag gate (Task 13 vs spec:164 "requires `--suite` and the safety flags in the brief, else blocked") | R1-F2, P2: name the flags, block without them; FR-G5 and `--no-pty` unresolved | R2-F1, P1: block before launch when safety inputs missing; separate assertions | R3-F2, P2: add "blocked" for missing safety flags, settle FR-G5 and `--no-pty`, or record as an owner decision | High |
| C-002 | Stale workflow.md:72 artifacts clause after Task 17 moves reflect output to `nested/reflect-<n>/` | R1-F1, P2, class necessary: additive line or widen ADDITIVE exemption; same for refs/return-contract.md | silent | R3-F3, P2, class drift: additive line or second exemption; update test pin 837-844 | Medium |
| C-003 | F1 "left out (WC-4)" requirement (source.md:7) pinned for only some P2 commands | silent | R2-F3, P2: clause-scoped F1 check for all 15; assign the "one short local sentence"; correct matrix claim | R3-F11, P2: one parametrized test over all 15 P2 commands | Medium |
| C-004 | Gate assertions pin labels, not resolutions (AC-2.1 "one assertion per gate") | R1-F10, P3: Tasks 5, 13, 16 lack per-gate phrases | R2-F2, P2: phrases must join condition to outcome; negative tests that reverse the outcome | silent | Medium |
| C-005 | Task 21 commit-path list and its equality AC | silent | R2-F4, P2: list omits staged `.dev/tasks` package | R3-F13, P3 [INFERRED]: exact equality with git status is fragile | Medium |
| C-006 | D-P2-1 research arms in brainstorm | R1-F5, P3: rule-compliant; show `/sc:research --depth deep` alternative to owner; `--strategy planning` redundant | silent | R3-F12, P3 [INFERRED]: `enrichment/research-light.md` vs `claudedocs/research_*` output path unresolved | Low |
| C-007 | Plan instructions that collide with a check | R1-F8, P3: "added sentence" at WRITE_VERB-classified lines would change keys (Tasks 10, 14, 15) | silent | R3-F8, P3: Task 12 "flag list line" (task.md:44) edit fails Check ADDITIVE | Low |
| C-008 | Deviation-classification practice | mixed classes (necessary, drift, none, authorized) | every finding "Drift" | every finding "drift" | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Severity of the cli-eval safety-flag gap (C-001) | P2 (calibrator: "P1 defensible") | P1 | P2 (calibrator: "arguably P1") | High |
| X-002 | Deviation class of the stale workflow.md:72 clause (C-002) | necessary | (no position) | drift | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V3 | R3-F1 (P1): tasklist Stage 9 calls `sc:task` via Skill (sc-tasklist-protocol SKILL.md:1535-1557); Task 16 nests only Stage 10.5 reflect, breaking plan:26's nested rule now that Task 12 gives task `--unattended` | High |
| U-002 | V3 | R3-F4 (P2): release-split Part 4 "Skill `sc:analyze` or inline verification" (SKILL.md:324) not handled by Task 8 | Medium |
| U-003 | V3 | R3-F5 (P2): reflect Wave 1B optional `tech-research` call (SKILL.md:632) not resolved by Task 15 | Medium |
| U-004 | V1 | R1-F3 (P2): Task 14 skips only the task-builder CLI-mode gate's staging step, leaving its `superclaude reflect run --fix --promote` call undefined under `--unattended` | High |
| U-005 | V1 | R1-F4 (P3): spec-panel `--mode socratic` "does not wait" is an unrecorded decision, unlike P1's business-panel refusal | Medium |
| U-006 | V1 | R1-F6 (P3): tasklist HALT mappings and `depth-map.yaml` location (calibrator: the "D-P2-13 covers only the move" part is wrong, plan records both HALTs; the High/Medium HALT is Stage 10) | Low |
| U-007 | V1 | R1-F7 (P3): no code reads `reflect-pre` (resolves T1-F4); add the grep to Task 16 ACs | Low |
| U-008 | V1 | R1-F9 (P3): single owner-approval table of all refusals/defaults (calibrator: plan:45 already records them) | Low |
| U-009 | V2 | R2-F5 (P3): coverage matrix lacks rows for two source.md:14 lessons (reflect-internal gap, not plan drift) | Low |
| U-010 | V3 | R3-F6 (P3): brainstorm.md:158 / SKILL.md:352 handoff-skip reason stale after P2 (calibrator: still true for the task handoff) | Low |
| U-011 | V3 | R3-F7 (P3): improve has no Safety Threshold section for the D-P2-8 clause | Low |
| U-012 | V3 | R3-F9 (P3): cleanup/improve Tool Coordination lists no Write tool (P1 precedent: explain) | Low |
| U-013 | V3 | R3-F10 (P3): Task 1 format baseline omits test_sc_recommend_routing_contract.py | Low |
| U-014 | V3 | R3-F14 (P3): Task 1 "drop the equality case" has no target (= T1-F2) | Low |
| U-015 | V3 | verified_ok: dependency chains, deferred:P2 entry count, EXPECTED_NESTING edits, mirror rule, auggie options all confirmed | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | C-001 (all three agree the safety-flag gate is missing) | The cli-eval "safety flags" are an identifiable, nameable set the plan can require; spec:164 names no flag, while cli-eval SKILL.md:138-139 lists run options (`--parallel`, `--no-pty`, `--no-mcp`, `--json`, `--junit`, `--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`) none of which is labelled "safety flag" | UNSTATED | Yes |
| A-002 | C-002, U-010 (fixes constrained by the one-deleted-line exemption) | The plan's Check ADDITIVE exemption budget (one deleted line each for workflow.md and brainstorm.md) is fixed; spec SA-4 allows existing-line changes only where section 3 names a defect fix, and the plan itself set the one-line cap | UNSTATED | Yes |
| A-003 | U-001, U-002, U-003 (missed nested calls) | Spec 2.1's nested propagation rule governs every nested call a converted command makes, including calls its own section 3 row does not name (tasklist Stage 9, release-split Part 4, reflect Wave 1B) | UNSTATED | Yes |
| A-004 | all variants | Findings are advisory to the owner; the reflect run never edits the plan (sc:workflow Wave 4 rule) | STATED | No |

## Summary
- Total structural differences: 3
- Total content differences: 8
- Total contradictions: 2
- Total unique contributions: 15
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Scored diff points (denominator): S 3 + C 8 + X 2 + A 3 = 16
- Highest-severity items: C-001, X-001, U-001, U-004
- Taxonomy pre-tag: L3 (gate/guard/state) C-001, X-001, A-001, A-003, U-001..U-004; L2 (structure) S-001, S-002, C-002, C-003, C-004, C-005, A-002; L1 (wording/presentation) S-003, C-006, C-007, C-008, X-002
- Similarity check: differences far above 10%; debate proceeds
