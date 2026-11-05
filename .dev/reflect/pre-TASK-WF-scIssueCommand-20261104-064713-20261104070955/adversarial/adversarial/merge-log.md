# Merge Log

## Metadata
- Base: Variant 3 (reviewer-3, opus:refactorer), `adversarial/variant-3-original.md`
- Executor: merge-executor (sc:adversarial Step 5)
- Changes planned: 22
- Changes applied: 22
- Status: success
- Timestamp: 2026-11-04T08:03:32Z
- Plan: `adversarial/refactor-plan.md` (auto-approved 2026-11-04T08:30:00Z)
- Output: `merged-verdict.yaml` (OUT = `.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/adversarial`)
- Other inputs read: `adversarial/variant-2-original.md` (Q-1 verbatim text for F-14)

## Changes Applied

### Change #1: Restructure base card into merged-verdict schema
- **Status**: Applied
- **Source**: Base (Variant 3) top-level keys
- **Target**: `merged-verdict.yaml` top level
- **Before**: `reviewer`, `persona`, `model_class`, `verdict`, `findings` (S-1..S-7), `self_reported_confidence` 0.78, `self_audit`
- **After**: `merge_method: adversarial`, `verdict: FAIL`, `convergence_score: 1.0`, `convergence_status: BLOCKED_BY_INVARIANTS`, `base_variant`, `source_cards: [reviewer-1, reviewer-2, reviewer-3]`, `citation_legend`, `findings`, `rejected_findings`, `unresolved`, `unaddressed_invariants`, `severity_rule`, in that order. `self_reported_confidence` and `self_audit` dropped. Threshold 0.80 recorded as an inline comment on `convergence_score`.
- **Provenance tag**: header comment block
- **Validation**: Pass. Parsed key list equals the Change 1 order. Each finding has exactly the 8 keys of Change 1.

### Change #2: F-01 (blocking, ordering)
- **Status**: Applied
- **Source**: Base S-1 + V1 A-2 + invariant probe INV-001/INV-002 + V3 Round 2 Branch A
- **Target**: `findings[0]`
- **Before**: S-1 (7 citations incl. `retry.md:14`; reorder-only recommendation)
- **After**: Plan claim, 11 citations, 4-part recommendation, `source_cards: [reviewer-1, reviewer-3]`, C-001 ruling
- **Provenance tag**: `# Source: ... Change #2, Disposition: modified`
- **Validation**: Pass. Evidence equals plan list exactly.

### Change #3: F-02 (blocking, security)
- **Status**: Applied
- **Source**: reviewer-3 calibration `missed_by_card`; debate A-001; INV-003, INV-004
- **Target**: `findings[1]`
- **Before**: (none)
- **After**: Plan claim/evidence/recommendation including `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID uv run --no-project python ...` and `monkeypatch.delenv`
- **Provenance tag**: `Disposition: merged-from-multiple`
- **Validation**: Pass.

### Change #4: F-03 (minor, missing-test)
- **Status**: Applied
- **Source**: V1 A-1 + V2 Q-3, narrowed; INV-005
- **Target**: `findings[2]`
- **Before**: A-1 (blocking, ACs 1-6, `./artifacts/t-ac-1-6.md`); Q-3 (ACs 2, 3, 6, `artifacts/t16-manual-acceptance.md`)
- **After**: ACs 1, 2, 3, 4, 6 unrun; `./artifacts/t-acceptance.md` covering ACs 1-8; `gh issue edit --add-assignee` caution
- **Provenance tag**: `Disposition: merged-from-multiple`
- **Validation**: Pass.

### Change #5: F-04 (minor, missing-test)
- **Status**: Applied
- **Source**: debate A-002; V1 A-1 recommendation; reviewer-2 calibration
- **Target**: `findings[3]`
- **Before**: (none as a standalone finding)
- **After**: `--repo` scan test in `tests/skills/test_issue_protocol.py`, `{owner}/{repo}` placeholder check
- **Provenance tag**: `Disposition: merged-from-multiple`
- **Validation**: Pass.

### Change #6: F-05 (minor, missing-requirement)
- **Status**: Applied
- **Source**: V1 A-3 + V2 Q-2 + A-004
- **Target**: `findings[4]`
- **Before**: Q-2 (5 citations)
- **After**: 6 citations (adds `source.md:320`); `git fetch origin` and `git log --since` in Task 5, worker-body sentence and test in Task 3
- **Provenance tag**: `Disposition: merged-from-multiple`
- **Validation**: Pass.

### Change #7: F-06 (minor, non-observable-ac)
- **Status**: Applied
- **Source**: Base S-3 (claim narrowed), V1 A-4 part
- **Target**: `findings[5]`
- **Before**: S-3 claim; evidence `plan:178, plan:145, plan:159`
- **After**: Plan claim (Q0 snapshot narrowing); evidence adds `src/superclaude/skills/sc-implement-protocol/SKILL.md:123`; S-3 recommendation verbatim
- **Provenance tag**: `Disposition: modified`
- **Validation**: Pass. Recommendation byte-identical to S-3.

### Change #8: F-07 (minor, other)
- **Status**: Applied
- **Source**: Base S-6, V1 A-4 part
- **Target**: `findings[6]`
- **Before**: S-6; evidence `plan:159`, `tests/core/test_how_we_work_routing_table.py:341`
- **After**: S-6 claim and recommendation verbatim; evidence per plan (adds `plan:168`, `:290-310`, `:341-346`)
- **Provenance tag**: `Disposition: modified`
- **Validation**: Pass. Claim and recommendation byte-identical to S-6.

### Change #9: F-08 (minor, unexecutable)
- **Status**: Applied
- **Source**: V1 A-4 part, split out
- **Target**: `findings[7]`
- **Before**: bundled in A-4
- **After**: standalone; recommendation points to F-02 part (2)
- **Provenance tag**: `Disposition: modified`
- **Validation**: Pass.

### Change #10: F-09 (minor, missing-requirement)
- **Status**: Applied
- **Source**: V2 Q-4 (relabelled from weak-match); INV-006
- **Target**: `findings[8]`
- **Before**: Q-4 (claim.md and create.md only)
- **After**: all five refs; Task 7 phrase check over `refs/*.md`
- **Provenance tag**: `Disposition: modified`
- **Validation**: Pass.

### Change #11: F-10 (minor)
- **Status**: Applied
- **Source**: Base S-2
- **Target**: `findings[9]`
- **Before**: S-2
- **After**: S-2 claim, recommendation, category `unexecutable` and evidence `plan:209`, `plan:212` unchanged; U-005 ruling added
- **Provenance tag**: `Disposition: preserved-exact`
- **Validation**: Pass. Claim and recommendation byte-identical.

### Change #12: F-11 (minor, spec-inherited)
- **Status**: Applied
- **Source**: Base S-4, relabelled
- **Target**: `findings[10]`
- **Before**: S-4 category `false-claim`; evidence `:141`, `:144`, `:149`
- **After**: category `spec-inherited`; plan claim; evidence `plan:121`, `source.md:391`, `tests/core/test_how_we_work_routing_table.py:19`, `:141-153`; S-4 recommendation verbatim
- **Provenance tag**: `Disposition: modified`
- **Validation**: Pass.

### Change #13: F-12 (minor)
- **Status**: Applied
- **Source**: Base S-5
- **Target**: `findings[11]`
- **Before/After**: S-5 unchanged (evidence `plan:198`); U-007 ruling added
- **Provenance tag**: `Disposition: preserved-exact`
- **Validation**: Pass.

### Change #14: F-13 (minor, scope)
- **Status**: Applied
- **Source**: Base S-7
- **Target**: `findings[12]`
- **Before/After**: S-7 unchanged (evidence `plan:20`, `plan:209`, `plan:230`); U-008 ruling added
- **Provenance tag**: `Disposition: preserved-exact`
- **Validation**: Pass.

### Change #15: F-14 (minor, weak-match)
- **Status**: Applied
- **Source**: V2 Q-1
- **Target**: `findings[13]`
- **Before**: Q-1 evidence `artifacts/coverage-matrix.json:8-15, plan:92, plan:24`
- **After**: Q-1 claim and recommendation verbatim; evidence per plan with the full `.dev/reflect/.../artifacts/coverage-matrix.json:8-15` path, order `plan:24`, `plan:92`
- **Provenance tag**: `Disposition: modified`
- **Validation**: Pass. Claim and recommendation byte-identical to Q-1.

### Change #16: F-15 (minor, spec-inherited)
- **Status**: Applied
- **Source**: invariant probe INV-007
- **Target**: `findings[14]`
- **After**: `--limit 200`, gh default 30
- **Provenance tag**: `Disposition: modified` (new entry; the fixed tag set has no "new" value)
- **Validation**: Pass.

### Change #17: F-16 (minor, missing-requirement)
- **Status**: Applied
- **Source**: INV-008
- **Target**: `findings[15]`
- **Provenance tag**: `Disposition: modified` (new entry)
- **Validation**: Pass.

### Change #18: F-17 (minor, other)
- **Status**: Applied
- **Source**: INV-009
- **Target**: `findings[16]`
- **Provenance tag**: `Disposition: modified` (new entry)
- **Validation**: Pass.

### Change #19: F-18 (minor, other)
- **Status**: Applied
- **Source**: INV-010
- **Target**: `findings[17]`
- **After**: plan claim and recommendation (499 lines). The plan's claim text does not contain "500"; the 500-line anchor from the Change 19 heading is carried in the F-18 provenance comment so the claim text stays exactly as the plan gives it.
- **Provenance tag**: `Disposition: modified` (new entry)
- **Validation**: Pass.

### Change #20: rejected_findings
- **Status**: Applied
- **After**: 7 entries: `Q-5`, `A-1-as-blocking`, `Q-3-calibrated-blocking`, `A-2-recommendation-deferred-outcome`, `S-4-false-claim-category`, `A-003-ac7-phrase-test`, `calibration-make-test-vs-uv-run-pytest`; reasons copied from the plan
- **Provenance tag**: `# Source: ... Change #20`
- **Validation**: Pass.

### Change #21: unresolved
- **Status**: Applied
- **After**: `unresolved: []`
- **Validation**: Pass.

### Change #22: provenance and severity rule
- **Status**: Applied
- **After**: header comment `# Provenance: produced by /sc:adversarial (Mode A, depth standard); Base: Variant 3 (reviewer-3, opus:refactorer); Merge date: 2026-11-04T08:03:32Z`; one `# Source:` comment above each of F-01..F-18 (18) plus top-level section comments (4); `severity_rule` = the caller's text from plan line 13
- **Validation**: Pass. 22 `# Source:` lines in total.

## Post-Merge Validation

### Structural integrity
- Status: Pass
- `yaml.safe_load` succeeds. Keys: `['merge_method', 'verdict', 'convergence_score', 'convergence_status', 'base_variant', 'source_cards', 'citation_legend', 'findings', 'rejected_findings', 'unresolved', 'unaddressed_invariants', 'severity_rule']`.
- 18 findings, ids F-01..F-18 in plan order; severities `[blocking, blocking, minor x16]`.

### Internal references
- Total references checked: every `evidence` list (18) compared against the backticked citations of its plan change; cross-finding refs (F-08 -> F-02 part 2; F-10 ruling -> F-01; rejected entries -> F-03, F-11)
- Resolved: all. Evidence lists equal the plan lists exactly (order and text) for all 18 findings. No citation added, changed or renumbered.
- Broken: 0

### Contradiction re-scan
- New contradictions introduced: 0
- `verdict: FAIL` with 2 blocking findings (F-01, F-02): consistent. `convergence_score: 1.0` with `unresolved: []`: consistent. `convergence_status: BLOCKED_BY_INVARIANTS` with `unaddressed_invariants: [INV-001, INV-002, INV-003]`: consistent. F-08 marked minor and pointed at F-02's fix: consistent with U-001 ruling.

### Threshold preservation check
| Source | Value | Required disposition | Result |
|---|---|---|---|
| V3 S-1 / F-01 | Task numbers 13, 14, 15, 16 | preserved-exact | Pass (Tasks 13-16 in F-01 claim/recommendation) |
| V1 A-1 / F-03 | section 20 items 1-6 | modified-with-rationale | Pass (ACs 1, 2, 3, 4, 6 unrun; ACs 1-8 in artifact; rationale in ruling) |
| V2 Q-1 / F-14 | INF-013, 054, 058, 059, 062 | preserved-exact | Pass (Q-1 claim verbatim) |
| V2 Q-3 | ACs 2, 3, 6 | modified-with-rationale | Pass (widened to 1, 2, 3, 4, 6) |
| F-15 | `--limit 200`; gh default 30 | preserved-exact | Pass |
| F-18 | 500 lines; 499 alternative | preserved-exact | Pass (499 in recommendation; 500-line in provenance comment, see Change #19) |
| F-02 | CLICKUP_API_TOKEN, CLICKUP_WORKSPACE_ID | preserved-exact | Pass |
| Change 1 | convergence 1.0, threshold 0.80 | preserved-exact | Pass (value 1.0; 0.80 in inline comment) |

### Dropped-anchor audit
| Anchor (plan omission table) | Expected | Result |
|---|---|---|
| V1 `./artifacts/t-ac-1-6.md` | omitted, replaced by `./artifacts/t-acceptance.md` | Pass (absent; replacement present) |
| V2 `artifacts/t16-manual-acceptance.md` | omitted, same replacement | Pass (absent) |
| V1, V2 self_reported_confidence 0.7 / 0.86 | omitted | Pass |
| V3 self_reported_confidence 0.78 | omitted | Pass |

Concrete anchors confirmed present in the merged file: `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID`, `--limit 200`, `git add .dev/tasks`, `CLICKUP_MAX_PAGES`, `E-TIER-UNAVAILABLE`, `E-HALT-QA`, `gh issue edit --add-assignee`, `monkeypatch.delenv`, `make sync-dev`, `make verify-sync`, `PYTHONDONTWRITEBYTECODE=1`, `grep -rIn`, `orca worktree rm --worktree name:<name>`, INF-013/054/058/059/062. No unplanned anchor dropped.

Verbatim checks against source variants (byte-equal): F-06 recommendation = S-3; F-07 claim and recommendation = S-6; F-10 claim and recommendation = S-2; F-11 recommendation = S-4; F-12 = S-5; F-13 = S-7; F-14 claim and recommendation = Q-1.

## Summary
- Planned: 22
- Applied: 22
- Failed: 0
- Skipped: 0
- Notes: Two executor-level placements, both within the plan: (1) the F-18 500-line anchor sits in the provenance comment because the plan's claim text omits it; (2) new probe-derived findings F-15..F-18 use the `modified` tag because the fixed tag set has no "new" value.
- Final status: success
