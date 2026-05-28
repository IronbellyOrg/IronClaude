# Phase 3 Refs Aggregation Summary

**Date:** 2026-05-27
**Phase:** 3 (Refs authoring — Steps 3.1-3.11)
**Status:** All 11 refs authored; awaiting Step 3.13 QA gate.

## File inventory (11 expected, 11 found)

| # | File | Line count | Anticipated band (per researcher 01) | Verdict |
|---|------|------------|--------------------------------------|---------|
| 1 | `refs/input-resolution.md` | 94 | 80-150 | PRESENT ✓ |
| 2 | `refs/reflection-rubric.md` | 162 | 120-200 | PRESENT ✓ |
| 3 | `refs/deviation-taxonomy.md` | 120 | 150-250 | PRESENT (slightly below band; spec content is dense — see Finding 1) |
| 4 | `refs/coverage-mapping.md` | 158 | 100-180 | PRESENT ✓ |
| 5 | `refs/reviewer-spec.md` | 110 | 100-180 | PRESENT ✓ |
| 6 | `refs/report-template.md` | 201 | 150-300 | PRESENT ✓ |
| 7 | `refs/remediation-handoff.md` | 137 | 80-150 | PRESENT ✓ |
| 8 | `refs/ops-integration.md` | 209 | 200-350 | PRESENT ✓ |
| 9 | `refs/grader-extensions.md` | 301 | 150-300 | PRESENT (1 line over due to trailing newline; content within budget) |
| 10 | `refs/promotion-adapters.md` | 154 | 150-250 | PRESENT ✓ |
| 11 | `refs/cost-profile.yaml` | 70 | 60-120 | PRESENT ✓ — YAML parse confirmed |

**Total:** 1,716 lines across 11 refs.

## Spec §16-row-to-file mapping (per spec lines 1500-1512)

| Spec §16 row | Ref filename | Wave assignment | File present |
|--------------|-------------|------------------|-------------|
| 1 | `refs/input-resolution.md` | Wave 0 | YES |
| 2 | `refs/reflection-rubric.md` | Wave 1D + Wave 3C | YES |
| 3 | `refs/deviation-taxonomy.md` | Wave 1B (UC-2) + Wave 5 | YES |
| 4 | `refs/coverage-mapping.md` | Wave 1B (UC-1) | YES |
| 5 | `refs/reviewer-spec.md` | Wave 3A | YES |
| 6 | `refs/report-template.md` | Wave 5 | YES |
| 7 | `refs/remediation-handoff.md` | Wave 6 | YES |
| 8 | `refs/ops-integration.md` | build-time | YES |
| 9 | `refs/grader-extensions.md` | eval-time | YES |
| 10 | `refs/promotion-adapters.md` | Wave 7 | YES |
| 11 | `refs/cost-profile.yaml` | pre-invocation | YES |

All 11 spec §16 rows have a corresponding file on disk.

## SKILL.md ref-pointer verification (11 expected, 11 found)

SKILL.md references each ref via inline `(See refs/<name>.md for ...)` pointer pattern. Verified via Grep:

```
refs/cost-profile.yaml
refs/coverage-mapping.md
refs/deviation-taxonomy.md
refs/grader-extensions.md
refs/input-resolution.md
refs/ops-integration.md
refs/promotion-adapters.md
refs/reflection-rubric.md
refs/remediation-handoff.md
refs/report-template.md
refs/reviewer-spec.md
```

All 11 refs are referenced inline from SKILL.md. No orphan refs (each is consumed by at least one wave per its §16 row). No SKILL.md ref-pointer references a non-existent file.

## YAML parse check

```
uv run python -c "import yaml; yaml.safe_load(open('refs/cost-profile.yaml'))" → OK
```

`cost-profile.yaml` parses cleanly with `yaml.safe_load`.

## Key fidelity checks (preview before QA gate)

| Criterion | Verdict | Notes |
|-----------|---------|-------|
| §10.6 Grounding Gaps YAML schema verbatim in `deviation-taxonomy.md` | PRESENT | All 6 required fields preserved (hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed, owner, decision_needed_by_user). |
| §11.3 calibrator selection pseudocode in `reflection-rubric.md` | VERBATIM | Spec lines 889-898 reproduced byte-exact per the authoring agent's confirmation. |
| §14.5.4 5 override flags in `promotion-adapters.md` | ALL PRESENT | `--no-promote`, `--promote-anyway`, `--promote-dry-run`, `--promote-mode`, `--promote-resume` with mutual-exclusion rules. |
| §14.5.5 7-row collision table in `promotion-adapters.md` | VERBATIM | Spec lines 1291-1299 reproduced byte-exact. |
| §14.5.5 4-state recovery table in `promotion-adapters.md` | VERBATIM | Spec lines 1278-1283 reproduced byte-exact. |
| §14.5.5 promotion-checkpoint.yaml schema in `promotion-adapters.md` | VERBATIM | All 10 keys from spec lines 1263-1274. |
| §12.4 grader DSL extensions in `grader-extensions.md` | 9 TRULY-NEW DOCUMENTED | sc-brainstorm grader.py has 8 baseline types (file_exists, frontmatter_field, section_present, section_enumerated, yaml_field, yaml_field_min, yaml_substring, dir_count); ALL 9 spec types are TRULY NEW (6 §12.4 semantic + path_exists + path_does_not_exist + falsifier_skeleton_present). Exceeds the "≥8" QA criterion. |
| `remediation-handoff.md` authored FRESH from `task-builder/SKILL.md:785-985` | YES (DOC-CONTRADICTED #1 respected) | Authoring agent confirmed task-builder uses prompt-style sections, not strictly enumerated fields. Documented 13 actual field names (GOAL, WHY, TASK_ID_PREFIX, TEMPLATE, QA_GATE_REQUIREMENTS, VALIDATION_REQUIREMENTS, TESTING_REQUIREMENTS, EXECUTION_CONTEXT_REQUIREMENTS, DOCUMENTATION STALENESS WARNINGS, RESEARCH DIR, QUALITY GATE RESULTS, OPEN QUESTIONS, REMAINING GAPS) rather than fabricating a "15-field" framing. The "M1-frozen 15-field" label in task-builder/SKILL.md:843 may include 2 implicit/structural elements (e.g., TASK FILE LOCATION + STEPS); ship-it for v1.0. May need follow-up reconciliation if QA gate flags. |
| `cost-profile.yaml` values match spec §15 | EXACT | T1 (2k-5k auggie / 3k-8k claude / 1-3min / 6 turns), T2 (10k-25k / 35k-70k / 8-15min / 52 turns), T3_added (+0 / +20k-40k / +5-10min / +30 turns); hard_kill_multiplier: 1.25; claude_tokens_per_turn: 1000. |
| No ref body duplicates SKILL.md content | TRUE | Each ref absorbs detail that SKILL.md only summarizes. SKILL.md cites refs via inline pointers; the ref bodies are not duplicated inline. |

## Findings

**Finding 1: `deviation-taxonomy.md` line count 120 vs anticipated 150-250.** Reason: spec §10 categories are tight (definition + detection signals + gold-standard ref + default remediation per category × 4) without significant elaboration content. The Grounding Gaps section is verbatim YAML schema (compact). The agent shipped within content scope but below the line band. No content gaps — recommend QA accept the below-band line count since the file covers all required sub-sections (Aggregation, Authorized, Necessary, Drift, Regression, Classification precedence, Grounding-gaps parallel artifact, Reporting).

**Finding 2: `remediation-handoff.md` BUILD_REQUEST field count.** Authoring agent documented 13 actual fields from task-builder/SKILL.md:785-985 rather than fabricating a "15-field" framing. The "M1-frozen 15-field" label in task-builder/SKILL.md:843 may include 2 implicit/structural fields. v1.0 ships the 13 fields verbatim from the actual template. Recommend QA accept with a note in Phase 3 Findings; potential follow-up cleanup if task-builder maintainers later clarify the exact field count.

**No other findings.** All 11 refs landed on disk, all referenced from SKILL.md, all spec-mandated content preserved.

## Resume point

Next unchecked item: Step 3.13 — Phase 3 QA Gate (spawn rf-qa in task-integrity mode against all 11 refs + SKILL.md + this summary).
