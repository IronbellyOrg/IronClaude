# QA Report — Structural / Template-Schema Conformance

**Topic:** Troubleshoot Pipeline Hardening — §5.5/§5.6/§5.7 schema + template conformance of the 6 new refs, 4 modified files, and test-dir markdown
**Date:** 2026-06-11
**Phase:** report-validation (structural template/schema conformance lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY — no files modified)

---

## Scope

QA input inventory: `.dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/phase-outputs/reports/qa-input-inventory.md`
Spec of record: `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md` §5.4 / §5.5 / §5.6 / §5.7

Verification target (zero-trust, files read directly):

- 6 new refs (`pipeline-hardening-closure.md`, `hardening-output-contract.md`, `runtime-entrypoint-verification.md`, `contract-enumeration.md`, `unmask-and-sweep.md`, `effective-input-proof.md`)
- 4 modified files (`SKILL.md`, `commands/troubleshoot.md`, `refs/report-template.md`, `refs/remediation-handoff.md`)
- test-dir markdown (`e2e-backtest-scenarios.md`) for placeholder scan

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | §5.6 H0 boundary-scan = 6 fields, in `pipeline-hardening-closure.md` | PASS | Schema table L26-33: `boundary_type`, `producer`/`transformers`/`consumer`, `evidence_source`, `risk`, `decision`, `rationale` — 6 rows, names verbatim vs spec L444-452 |
| 2 | §5.6 H0 `boundary_type` 9-value enum verbatim | PASS | Ref L28 lists CLI/subprocess, file-stdin-prompt, generated-artifact-parser, gate-status-enum, duplicate-evaluator, persisted-state, review-selector, sibling-pipeline, prior-escape-unmask — identical 9 vs spec L447 |
| 3 | §5.6 H1 runtime-entrypoint card schema, in `runtime-entrypoint-verification.md` | PASS | Schema table L13-24: 10 rows matching spec L457-467 exactly (producer, transformers, consumer_or_evaluator, boundary_crossed, replay_command, production_boundary_reach_proof, forbidden_interpretation, negative_witness_command/result, positive_witness_command/result, accepted_substitute_rationale). See Note A on the "11" count. |
| 4 | §5.6 H2 contract-ledger schema = 6 fields, in `contract-enumeration.md` | PASS | Schema table L7-14: contract_token, role, component_path, discovery_method, classification, unreachability_proof — 6 rows verbatim vs spec L472-478 |
| 5 | §5.6 H3 unmask/sweep/classifier card = 10 fields, in `unmask-and-sweep.md` | PASS | Schema table L41-52: anchor_failure, sibling_family_discovery_method, K_true, K_swept, coverage_proof, positive_fixture, sibling_negative_fixture, full_artifact_mixed_fixture, severity_assertions_by_consumer, heuristic_cost_rationale — 10 rows verbatim vs spec L483-493 |
| 6 | §5.6 H4 effective-input manifest = 8 field-groups, in `effective-input-proof.md` | PASS | Schema table L18-27: selector_command/cwd, base_ref/head_ref, dirty/staged/unstaged_files, included_files, excluded_foreign_commits, runtime_surface_claim, intersection_proof, validation_command/result — 8 groups verbatim vs spec L499-506 |
| 7 | §5.5 11-field output contract fully reproduced in `hardening-output-contract.md` (7 columns) | PASS | Field schema table L11-23: 11 rows × full 7-column shape (Field/Type/Required/Default/Nullability/Producer/Consumer-Behavior) verbatim vs spec L427-439 |
| 8 | §5.5 11-field contract reproduced additively in SKILL.md | PASS | SKILL.md L62-72: all 11 fields present (contract_version, pipeline_hardening_applicable, pipeline_hardening_verdict, waiver_status, backtest_status, off_path_review_decision, 4× *_card_path, known_escapes_caught), condensed 3-col additive form |
| 9 | §5.4 verdict-aggregation truth table = all 7 rows, in `hardening-output-contract.md` | PASS | Truth-table L31-39: rows 1-7 present, priorities + verdicts + report language + "Downstream Override Allowed? = No" verbatim vs spec L392-400 |
| 10 | §5.4 H5 decision-to-status (4 rows) + backtest-status (3 rows) sub-tables | PASS | hardening-output-contract.md L45-50 (4 H5 rows) + L60-64 (3 backtest rows) vs spec L404-409 / L417-421 |
| 11 | Each ref has exactly one H1 (MD025) | PASS | `grep -cE '^# '` = 1 for all 6 refs; report-template's 2nd `#` (L8) is inside the ````markdown fence; troubleshoot.md `#`-lines are comment lines inside code fences |
| 12 | Fenced code blocks carry language tags (MD040) | FAIL | 5 bare ``` fences in `commands/troubleshoot.md` L108/119/130/141/149 (Examples section). markdownlint-cli2 (repo `.markdownlint.json`, MD040 enabled by `default:true`) flags all 5. See MINOR-1. |
| 13 | No placeholder text (TODO/TBD/FIXME/lorem/<insert>) | PASS | grep across all 6 refs + 4 modified files + e2e scenarios: 0 hits (the one "TodoWrite" hit at SKILL.md L4 is a tool name in frontmatter, not a placeholder) |
| 14 | report-template Pipeline Hardening Closure section: 4-token verdict + NOT PROVEN/ADVISORY blockers | PASS | report-template.md L204-238 (in-template) renders `<pass\|blocked\|advisory\|not_applicable>`, H0-H5 statuses, evidence cards, NOT PROVEN ×3 + ADVISORY ×2 blockers; post-template rule L296-303 |
| 15 | remediation-handoff §5.4 no-override + verdict/waiver carry | PASS | remediation-handoff.md L7-11 (downstream may-not-re-green), L35-37 (offer surfaces verdict), L68-73 (BUILD_REQUEST carries pipeline_hardening_verdict + waiver_status) |

---

## Summary

- Checks passed: 14 / 15
- Checks failed: 1 (MD040 — check 12)
- Critical issues: 0
- Important issues: 0
- Minor issues: 1
- Issues fixed in-place: 0 (fix_authorization=false; REPORT ONLY)

The five required schema sets (§5.6 H0/H1/H2/H3/H4) and the two contract artifacts (§5.5 11-field schema, §5.4 7-row truth table) are **fully and verbatim conformant** to the spec — field names, field counts, enum values, column shape, row priorities, and report-language strings all match. No fabricated, renamed, or dropped schema field was found in any of the six new refs or in the SKILL.md additive reproduction. The single failure is a pre-existing MD040 lint defect in a modified deliverable, not a schema/template-content defect.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| MINOR-1 | MINOR | `src/superclaude/commands/troubleshoot.md` L108, L119, L130, L141, L149 | 5 fenced code blocks in the `## Examples` section open with a bare ` ``` ` (no language tag), violating MD040. Confirmed by `markdownlint-cli2 --config .markdownlint.json` (repo config has `"default": true`, which enables MD040). These fences are PRE-EXISTING (git diff vs `master` shows this work only added one Behavioral-Summary sentence + one Boundaries→Will line to this file; the Examples block predates the hardening change), and they fall OUTSIDE the inventory's cleanliness claim, which scopes only "9 src **skill** markdown files" — `troubleshoot.md` is a command file (the 10th deliverable). | Add a language tag to each fence, e.g. ` ```text ` (these blocks contain a command line plus `#`-prefixed comment lines, so `text` is appropriate). Out-of-change-scope but should be cleaned to satisfy the project's `default:true` MD040 gate on this listed deliverable. |

---

## Notes

**Note A — H1 "11 fields" vs 10 table rows (NOT a defect).** The task brief states "H1 11 fields". The spec §5.6 H1 card table (release-spec L457-467) itself has **10 table rows**, two of which are slash-paired atomic fields (`negative_witness_command`/`negative_witness_result`; `positive_witness_command`/`positive_witness_result`). Counting the paired witness fields as separate atomic fields yields 11; counting table rows yields 10. The ref `runtime-entrypoint-verification.md` reproduces the spec's 10-row table verbatim (identical field names, same pairing, same `Required` column values). The ref is therefore a faithful, complete reproduction of the spec's H1 schema; the "11" is a field-vs-row counting convention, not a missing field. No discrepancy between ref and spec.

**Note B — MD040 false positives suppressed.** The locally-available `markdownlint-cli2 v0.22.1 (markdownlint v0.40.0)` additionally flags MD060 (table-column-style), a rule that did not exist in the project's pinned `markdownlint-cli v0.38.0` (`.pre-commit-config.yaml`). MD060 findings were excluded from this report as not-gate-enforced; only MD040 (present in the pinned version and enabled by `default:true`) was treated as authoritative.

**Note C — §5.7 H3 parser decision.** `unmask-and-sweep.md` L5-12 reproduces the §5.7 four-rule allow-list grammar (ATX-only behavior-controlling, word-boundary/`re.escape` matching, setext/decorated/wrong-case as fixtures-not-syntax, every expansion needs positive+near-miss+full-artifact fixtures) verbatim vs spec L510-515. Conformant (covered structurally; not a numbered task requirement but verified).

---

## Confidence Gate

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 10

Tool-call-to-checklist ratio: 19 tool calls (9 Read + 10 Bash) ≥ 15 checklist items — engagement minimum satisfied. Every schema-count and field-name check was grounded in a direct file read or a grep/awk extraction of the actual table rows, cross-referenced line-by-line against the release-spec §5.6/§5.5/§5.4 source. The MD040/MD025 verdicts were grounded in an actual `markdownlint-cli2` run against the repo `.markdownlint.json`, not reasoning. No item was marked VERIFIED on the basis of a prior report.

---

## Recommendations

1. Add language tags to the 5 bare fences in `commands/troubleshoot.md` (MINOR-1). Lowest-risk fix: ` ```text `. This is out-of-change-scope and pre-existing, but it is a real MD040 violation in a listed deliverable; cleaning it makes the full deliverable set MD040-clean under the project's `default:true` config.
2. No schema or template-content remediation required — all §5.5/§5.6/§5.7/§5.4 structural requirements pass.

---

## Verdict Rationale

Per the gate rule "FAIL if any issue of any severity," the single MINOR MD040 violation (check 12) forces a FAIL verdict even though all schema/contract/template-content conformance checks (14/15) pass cleanly. The defect is lint-class and out-of-change-scope, not a schema or template-structure error; the binary gate nonetheless requires FAIL.

## QA Complete

VERDICT: FAIL
