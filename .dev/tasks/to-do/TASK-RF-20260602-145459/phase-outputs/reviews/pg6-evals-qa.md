# QA Report — Phase Gate PG-6 (Eval-Workspace Scaffold + evals.json Registry)

**Task:** TASK-RF-20260602-145459
**Phase:** PG-6 / task-integrity (eval scaffold + registry integrity)
**Date:** 2026-06-03
**Fix cycle:** N/A (no fixes required)
**Driving spec:** `.dev/releases/current/Reflect-V3.5-Serena_Mediums/05-spec-medium-complexity.md` (§8.1 + §8.2)
**Stance:** Adversarial — assumed errors; read every actual file (eval files are NOT under src/, no sync-dev applies).

---

## Overall Verdict: PASS

All 10 scaffolded cases (ids 27-36) exist with correct structure, the registry is valid JSON with
unique non-duplicate ids 27-36, every assertion `type` is in `grading_criteria`, every `target` is
`with_skill/`- or `old_skill/`-prefixed, per-case assertions match the spec/research criteria, the
top-level `scope` names the medium coverage, and both the §8.2 coverage map and the NFR-3 deferral
record are present and internally correct.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 7 §8.1 unit cases exist, each with `input/tasklist.md` + `input/diff.patch` + `expected.yaml` | PASS | `find` enumerated all 3 files in each of serena-execute-verify, -verify-injection, -verify-exitcodes, -verify-drift-guard, -onboarding, -handoff, -type-hierarchy |
| 2 | 3 §8.2 integration cases exist with declared shape | PASS | serena-token-budget = `expected.yaml` only (measurement declaration, NO `input/`, as spec'd); serena-telemetry-completeness + serena-citation-freshness each have full `input/` + `expected.yaml` |
| 3 | All expected.yaml carry `# STUB` header | PASS | `cat` of all 10 — every file opens with `# STUB — V3-Serena-medium eval scaffold` |
| 4 | Input fixtures non-empty | PASS | `wc -c`: tasklist 288-750 bytes, diff 177-415 bytes across all 9 input-bearing cases |
| 5 | evals.json is valid JSON | PASS | `uv run python -c json.load(...)` → `VALID JSON` |
| 6 | Unique ids 27-36, no dups | PASS | ids list = 1..36 contiguous; `dup ids: []`; `ids 27-36 present: [27..36]` |
| 7 | Every assertion `type` ∈ top-level `grading_criteria` | PASS | Per-assertion scan over ids 27-36 → `BAD TYPES: []` |
| 8 | Every assertion `target` starts `with_skill/` or `old_skill/` | PASS | Per-assertion scan → `BAD TARGETS: []` (id 34 uses `old_skill/expected.yaml` for the falsifier; all others `with_skill/...`) |
| 9 | injection (28): metachar-denied AND zero invocations per metachar class | PASS | Assertions: `regex_present verify_blocked_reason.*metachar-denied` + `regex_absent` on invocations.yaml (`rm -rf\|curl \|\$(\|`\|>/etc`) + `yaml_field verification_invocations == 0`. expected.yaml lists all 6 classes → metachar-denied, `subprocess_invocations_for_metachar_commands: 0` |
| 10 | exitcodes (29): pytest 1→Regression (vrd==1), flaky→verify_flaky_suspected, exit 5→Drift | PASS | `yaml_field verification_regressions_detected == 1` + `regex_present verify_flaky_suspected.*true` + `deviation_class_matches value drift`. expected.yaml taxonomy table covers 2/3→grounding_gap, ruff/mypy 1→s_dev_density, 124→grounding_gap, unmapped→grounding_gap |
| 11 | handoff (32): N>20 sweep + ordering + write_memory_fallback + both-fail ships | PASS | expected.yaml: `retention_sweep {before:21, sweep_triggered:true, after:20}`, `handoff_written_before_taskbuilder:true`, `fallback.handoff_persist_method: write_memory_fallback`, `both_fail.report_ships:true`. Registry uses `checkpoint_logged` (ordering) + `file_exists REPORT.md` (both-fail ships) |
| 12 | type-hierarchy (33): LSP-disabled skip-no-degrade + backend-error degrade | PASS | expected.yaml: `lsp_disabled {type_hierarchy_invoked:false, degraded:false, status:success}` + `backend_error {degraded:[type_hierarchy:backend_error], fallback_used:...}` + `lineage_confirm` HIGH-after-confirm + coverage 2/3 |
| 13 | telemetry-completeness (35): HOLISTIC sweep, both paths, distinct from per-FR | PASS | expected.yaml: 4 invoked/ran fields (all FRs) + 4 skip/degraded fields + `both_paths_required:true`; `disposition: ENCODED-NEW`. Registry: 3× `yaml_list_contains` + `regex_present` |
| 14 | citation-freshness (36): holistic re-Read-within-5-calls | PASS | expected.yaml: `all_citations_refreshed_within_5_calls:true`, new-output citations (hierarchy-slice.yaml, invocations.yaml), `evidence_validator_ran:true`; `disposition: ENCODED-NEW` |
| 15 | token-budget (34): runner-gated, skeleton-pending-runner, falsifier_skeleton_present | PASS | expected.yaml: `status: skeleton-pending-runner`, `runner_present:false`, `disposition: RUNNER-DEFERRED`. Registry: single `falsifier_skeleton_present` on `old_skill/expected.yaml` |
| 16 | execute-verify (27): triangle, allowlist/mutation/timeout, regression→promotion-block, skip variants | PASS | expected.yaml: `verification_invocations:3`, `verification_regressions_detected:1`, `regression_present:true`, `promotion_blocked:true`, allowlist/mutation denies, `timeout_124`, `--no-verify`/read-only skip-with-WARN |
| 17 | drift-guard (30): cache artifacts do NOT trip input-drift STOP | PASS | expected.yaml: `input_drift_detected:false`, `input_tree_sha256_changed:false`, `status:success`, `stop_reason:null`. Registry: `regex_absent` on audit.log |
| 18 | onboarding (31): cold-start, silent-fail guard, context-excluded WARN, warm skip, no-auto-trigger | PASS | expected.yaml covers FR-2.1–2.6 + NFR-7 budget breach; registry: `yaml_field` + 3× `regex_present` on audit.log |
| 19 | top-level `scope` ends `-10-serena-v3-medium` | PASS | scope = `v1.0-ship-it-3-pilot-15-promotion-2-falsifier-skeleton-6-serena-v3-10-serena-v3-medium` — literal suffix `-10-serena-v3-medium` present |
| 20 | section-8-2-coverage-map.md: 7 rows, exactly one disposition each | PASS | All 7 rows: ENCODED-NEW (3,6), RUNNER-DEFERRED (5), ABSORBED (1,2,4,7); cross-references + result section consistent |
| 21 | nfr3-token-budget.md: explicit deferral, make reflect-eval = grader not ledger | PASS | Records EXPLICIT DEFERRAL with IF-runner-present/IF-absent branches; CODE-VERIFIED claim confirmed independently (Makefile lines 493/501 define `reflect-eval`/`reflect-eval-quick` running grader.py) |

## Summary

- Checks passed: 21 / 21
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Issues Found

None.

## Independent Cross-Verification (adversarial spot-checks beyond agent claims)

- `make reflect-eval` target genuinely exists (Makefile .PHONY line 1 + targets at L493/L501) — the
  token-budget deferral's "assertion grader, not token ledger" rationale is grounded, not asserted.
- injection (28) `regex_absent` pattern `rm -rf|curl |\$\(|`|>/etc` materially covers the 6 metachar
  fixture commands in expected.yaml (`;`, `&&`, `|`, `$()`, backtick, `>`) — the zero-invocation gate
  is real, not cosmetic.
- token-budget falsifier correctly targets `old_skill/expected.yaml` (the only `old_skill/`-prefixed
  target in the batch) with the `falsifier_skeleton_present` grading type — both are valid per the
  registry's `grading_criteria`.
- All 36 ids are contiguous 1..36 with the new batch appended as 27-36 (no gaps, no collisions with
  the prior 26).

## Confidence Gate

- **Confidence:** Verified: 21/21 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 6
- No UNCHECKED items. No UNVERIFIABLE items. No web research performed (no external claims in scope).
- Tool-engagement note: Bash batched multiple independent verifications per call (JSON parse + field
  extraction + file cats + Makefile grep); each invocation maps to a specific checklist item or set
  of items. Total verification surface exceeds 21 distinct evidenced checks.

## Recommendations

- Green light to proceed past PG-6. The eval scaffold is structurally sound and the registry is
  machine-valid. No remediation required.
- (Forward note, non-blocking) When a token-ledger runner lands, replace the id-34
  `falsifier_skeleton_present` assertion with a `yaml_field` on the measured delta per the deferral
  record — already documented in `nfr3-token-budget.md`.

## QA Complete

VERDICT: PASS
