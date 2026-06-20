# Phase 4 Output Summary — TFEP Return-Contract Adapter

**Date:** 2026-06-16
**Files edited:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, `.../refs/report-template.md`
**verify-sync:** EXIT 0, no drift, no `.claude/` staged (`test-results/phase-4-verify-sync.txt`)

All snippets below are from the captured `git diff`.

## 5 new Output Contract rows (after `known_escapes_caught`)
1. **Step 4.1** `| \`recommended_escalation\` | enum \`none\|retry\|escalate_depth\|halt\` | TFEP adapter field (contract v1.1.0+). Forward-looking recommendation … \`none\`=remediation ready; \`retry\`=re-run same depth; \`escalate_depth\`=re-run deeper; \`halt\`=full stop. |`
2. **Step 4.2** `| \`tasklist_insertion_path\` | string \| null (abs path) | TFEP adapter field (contract v1.1.0+). Path to the adjudicated remediation-plan block … null when no remediation (e.g. \`recommended_escalation: halt\`). Distinct from \`task_file_path\` and \`diagnosability_tasklist_path\`. |`
3. **Step 4.3** `| \`remediation_target\` | enum \`test\|code\|docs\|none\` | … composed from \`test_is_wrong\`/\`behavior_is_documented\`; \`code\` otherwise; \`none\` when halt. |`
4. **Step 4.4** `| \`root_cause_summary\` | string | … extracted from REPORT.md **Diagnosis** (Wave 5). Empty when inconclusive. |`
5. **Step 4.5** `| \`solution_summary\` | string | … extracted from REPORT.md **Proposed Fix** / **Next Steps** (Wave 5). Empty when no fix (e.g. halt). |`

## Step 4.6 — contract_version bump
- **Before:** `Output-contract semver, default \`1.0.0\`. Additive … Pipeline Hardening Closure fields below (FR-13); … (NFR-6).`
- **After:** `Output-contract semver, default \`1.1.0\`. Additive … Pipeline Hardening Closure fields (FR-13) and the TFEP adapter fields (\`recommended_escalation\`, \`tasklist_insertion_path\`, \`remediation_target\`, \`root_cause_summary\`, \`solution_summary\`); … (NFR-6).`

## Step 4.7 — Wave 5 conditional emission step 4.5
- Inserted between the SUMMARY footer fence and step 5. Gated on `caller=task-unified`; writes `<output-dir>/return-contract.yaml` mapping `status`,`test_is_wrong`,`recommended_escalation`,`tasklist_insertion_path`,`remediation_target`,`root_cause_summary`,`solution_summary`; derives summaries from REPORT.md Diagnosis / Proposed Fix; records `return_contract_path` in the SUMMARY footer; explicit NOTE that TFEP passes NO `--fix` (diagnosis only). **This resolves PG3's deferred Cluster 1.**

## Step 4.8 — Wave 5 exit-criteria + surface list
- Surface list: new bullet `- (if \`caller=task-unified\`) the emitted \`return-contract.yaml\` path.`
- Exit criteria appended: `When \`caller=task-unified\`, \`return-contract.yaml\` is written and its path returned.`

## Step 4.9 — report-template `## TFEP Consumer` block
- Inserted between `## Next Steps` and `### Hard-stop variant`. A `## TFEP Consumer` heading + one-line note (emitted only when caller=task-unified; report-rendered echo of return-contract.yaml) + fenced ```yaml block echoing the 7 fields. Field names EXACTLY match the Output Contract rows (4.1–4.5) + `status`/`test_is_wrong`.
- RECONCILIATION: speculative R-003 names `tasklist_insertion_recommendation`/`safe_to_auto_insert` intentionally reconciled to the canonical consumer token `tasklist_insertion_path` (logged in Phase 4 Findings).

## Step 4.10 — sync + verify-sync → EXIT 0.

## Producer/consumer integrity (pre-PG4 self-check)
The report-template `## TFEP Consumer` yaml keys = {status, test_is_wrong, recommended_escalation,
tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary} — every one has a
matching Output Contract producer row (status + test_is_wrong pre-existing; the other 5 added in 4.1–4.5).
No consumer token without a producer.

No fabrication: every snippet is from the captured `git diff`.
