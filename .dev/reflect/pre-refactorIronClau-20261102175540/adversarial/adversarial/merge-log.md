# Merge Log

## Metadata
- Base: Variant 1 (reviewer-1, sonnet, analyzer), `variant-1-original.md`
- Plan: `refactor-plan.md` (14 planned changes, 5 changes not made)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `../merged-findings.md` (one fenced YAML block, provenance header as HTML comments)
- Changes applied: 14 of 14 (failed 0, skipped 0)
- Status: complete, with 1 new contradiction flagged for orchestrator review (see Post-Merge Validation)
- Timestamp: 2026-11-02T18:41:04Z

## Changes Applied

| # | Status | Before -> After | Provenance |
|---|---|---|---|
| 1 | applied | No finding on scripts/eval_runner.py -> new finding M-1 (drift, high) inserted after R1-1 | Variant 3 R3-F1 + INV-005 |
| 2 | applied | No list-argument accounting -> new finding M-2 (drift, medium) inserted after M-1, with the second-search command and separate total | INV-003, INV-004 |
| 3 | applied | R1-1 rationale/recommendation covered checks 1 and 3 only -> appended recovery gap (agent stops, reports, user closes; SKILL.md:222) and gh-flag gap (`gh repo view`, `gh api`; test_static_grep.py:616) plus "name the exact allowed forms" acceptance | INV-008, INV-009, INV-007 (addressed); R3-F2 alternative not adopted |
| 4 | applied | No upstream-remote finding -> new finding M-4 (drift, medium) | INV-001 |
| 5 | applied | R1-4 recommendation `-v` only -> `-v -rs`, zero skips or recorded skip reasons and a full-depth non-root rerun; skip sources and fixture citation placed in the recommendation (plan approach was "modify recommendation") | Variant 3 A-003, INV-006, Variant 2 fixture citation |
| 6 | applied | R1-5 rationale "static link is not a tool call" and recommendation "decide link vs de-link" -> rationale: literal text covers the static URL (X-001 majority, dissent noted), 22 lines in 10 files incl. negative fixtures; recommendation: narrow plan line 73 to "no tool call, and no gh or Orca link flag", static references out of scope | Variant 2 X-001, Variant 3 R3-F6 dissent, INV-011 |
| 7 | applied | R1-6 "Orca-link ban, fetch/pull ban and project id are authorized additions" -> fetch/pull ban is a literal reading (not a deviation); only the dated Orca project-id bullet is an authorized expansion. Headline and rationale rewritten; class stays `authorized` | Variant 2 C-005; Variant 1 Round 2 concession |
| 8 | applied | R1-2 rationale "calling it purely historical is not fully accurate" -> plan line 37 never calls the file finished; :576 records substantive work validated with only a manual reflect gate outstanding; class and surface-to-user request kept | reviewer-1-calibration.yaml; POST-REFLECT-TASK.md:576 |
| 9 | applied | No Orca-flag finding -> new finding M-9 (drift, low) with the plan line 76 mitigation | Variant 3 R3-F3 |
| 10 | applied | No contract-test finding -> new finding M-10 (drift, low; "coverage gap" stated in rationale) | Variant 3 R3-F4 |
| 11 | applied | No post-release finding -> new finding M-11 (drift, low) | Variant 3 R3-F5 |
| 12 | applied | No findings for INV-002/INV-014 -> new findings M-12a (live retired-location checkout) and M-12b (runbook.md:34), low each. Note: the plan gives no classification for these; `drift` was used, the class the plan assigns to every other plan-gap finding. Orchestrator may override | INV-002, INV-014 |
| 13 | applied | No coverage section -> top-level `coverage`: 11 INF rows, INF-003 partial (carried by M-1, M-2), all others covered | Variant 2 structure (S-001) |
| 14 | applied | No INV-010 or U-007 entry -> `inferred_claims` gains INV-010 [INFERRED] and U-007 [INFORMATIONAL]; `invariants_carried` lists INV-010 as carried by inferred claim | INV-010; Variant 1 U-007 Round 2 |

Other structural notes:
- Header keys `reviewer: 1`, `persona`, `model_class` replaced by `reviewer: merged`, `base: variant-1` (per the orchestrator's key list; base identity kept in the HTML provenance header).
- Base `t1_findings_disputed` and `self_confidence: 0.75` kept unchanged (plan says same schema as the base; nothing in the plan removes them); `self_confidence` carries a comment that it is the base value, not recomputed.
- Base inferred claim on SKILL.md:267 kept and marked `[SUPERSEDED by the U-007 guard verdict, Round 2]`; the plan does not say to drop it.
- `changes_not_made` reproduces the plan's 5-row table.
- Finding order: R1-1, M-1, M-2 (per Changes #1, #2 targets), then R1-2..R1-6, then the untargeted inserts M-4, M-9, M-10, M-11, M-12a, M-12b in change order.
- Cited repo lines spot-checked against the worktree before writing: CLAUDE.md:41, :64, :66, :251; scripts/eval_runner.py:138-147; sc-pr-submit-protocol/SKILL.md:222; tests/pr_submit/test_static_grep.py:616; sc-post-release-protocol/SKILL.md:91; .github/workflows/test.yml:17; docs/swarm/runbook.md:34; pyproject.toml:64-67. All match.

## Post-Merge Validation

### Structural integrity
- PASS. The fenced block was read through and also parsed with `yaml.safe_load`: top-level keys `reviewer, base, findings, t1_findings_disputed, self_confidence, coverage, invariants_carried, changes_not_made, inferred_claims`.
- 14 findings, each with all 9 fields (id, headline, location, classification, severity, evidence, rationale, recommendation, provenance). Strings containing colons or `#` are quoted or in block scalars.
- Severities: high 1 (M-1); medium 3 (R1-1, M-2, M-4); low 10. Classifications use only authorized | necessary | drift.

### Internal references
- PASS. Every finding id referenced elsewhere in the card (t1_findings_disputed -> R1-1, R1-2, R1-3; coverage -> M-1, M-2; invariants_carried -> R1-1, R1-4, R1-5, M-1, M-2, M-4, M-12a, M-12b) exists. Dangling references: none.
- invariants_carried lists all 11 UNADDRESSED INV ids (INV-001..006, 008..011, 014); INV-010 included per Change #14.

### Contradiction re-scan
- NEW contradiction (1): R1-2's base headline still says "The plan's description of POST-REFLECT-TASK.md as a finished past record is incomplete", while the Change #8 rationale now says plan line 37 never calls the file finished. Change #8 targets the rationale only, so the headline was not edited. Escalated to the orchestrator: a one-line headline edit would resolve it.
- Noted, not counted: R1-5's headline keeps "ambiguous" while the rationale now gives the majority reading that the literal text covers the static URL; with the 2-1 split and recorded dissent, "ambiguous" remains accurate.
- Resolved by the merge: base R1-6 (fetch/pull "authorized addition") previously conflicted with base t1 dispute F3 ("literal reading is the faithful one"); Change #7 removes that conflict.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 14 | 14 | 0 | 0 |

- New contradictions introduced: 1 (R1-2 headline vs rationale).
- Escalations: R1-2 headline (above); classification `drift` chosen for M-12a/M-12b where the plan named none.
