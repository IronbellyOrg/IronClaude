# QA Report — Post-Completion Structural QA (Internal-Consistency Lens)

**Topic:** Forensic→troubleshoot TFEP backend migration (5-file end-to-end consistency)
**Date:** 2026-06-16
**Phase:** report-validation (post-completion structural QA — internal-consistency lens)
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed ≥5 internal-consistency errors and hunted for them.

---

## Overall Verdict: FAIL

One genuine internal-consistency defect (F1, IMPORTANT) found: the `troubleshoot` command
mislabels the `--context` INPUT file as `return-contract.yaml`, which is in fact the OUTPUT
artifact troubleshoot emits — the producer (task-protocol) writes and passes `context.yaml`.
A reader following the command doc would supply the wrong file. Two MINOR enum-rendering
observations (F2, F3) are noted but are pre-existing/out-of-scope of the TFEP wire set.

Per zero-tolerance: any genuine inconsistency = FAIL. F1 alone fails the gate.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 5 adapter field names IDENTICAL across all 4 locations | PASS | `recommended_escalation`, `tasklist_insertion_path`, `remediation_target`, `root_cause_summary`, `solution_summary` appear verbatim in: skill Output Contract rows (SKILL.md L73-77); Wave 5 step 4.5 emission list (SKILL.md L471); report-template `## TFEP Consumer` YAML (report-template.md L161-167); task-protocol §4.5 consumer (sc-task-protocol SKILL.md L219, L233, L236, L257-258). grep cross-match clean. |
| 2 | `recommended_escalation` enum `none\|retry\|escalate_depth\|halt` IDENTICAL | PASS | skill L73 `enum none\|retry\|escalate_depth\|halt`; report-template L163 `<none\|retry\|escalate_depth\|halt>`; consumer branches on all four values verbatim (sc-task-protocol L227-230). Byte-identical value set. |
| 3 | `remediation_target` enum `test\|code\|docs\|none` IDENTICAL | PASS | skill L75 `enum test\|code\|docs\|none`; report-template L165 `<test\|code\|docs\|none>`; consumer references `remediation_target == "docs"` (L225) + composes from `remediation_target` (L236). Value set consistent. |
| 4 | 7-field TFEP Consumer block = Wave 5 step 4.5 emission list (same fields, same order) | PASS | report-template L161-167 lists `status, test_is_wrong, recommended_escalation, tasklist_insertion_path, remediation_target, root_cause_summary, solution_summary` — identical order to skill L471 emission list. |
| 5 | tier→depth mapping consistent: §4.5 Step 3 mapping vs dispatch vs Escalation Budget | PASS | Step 3 bullets (L210-213): 1st→standard, 2nd/systemic/≥3-new→deep, 3rd→FULL STOP. Dispatch sentence (L215): standard for 1st/simple, deep for systemic/≥3-new/2nd. Escalation Budget (L268-270): identical. All three agree. |
| 6 | `contract_version 1.1.0` referenced consistently | PASS (with note) | skill L62 default `1.1.0`; adapter rows L73-77 tagged `contract v1.1.0+`. task-protocol consumer does NOT reference a version string — but it reads fields by name, not by version gate, so no inconsistency (see F-note below). |
| 7 | `--context`/`--caller` descriptions agree across command + skill | FAIL | F1: command L59 mislabels `--context` input as `return-contract.yaml`. See Issues Found. |
| 8 | `caller=task-unified` value consistent across all 5 files | PASS | Verbatim `task-unified` in: command L60/L69; troubleshoot skill L148/L471/L479/L481; report-template L158; task-protocol L215/L239/L268-269. No drift. |
| 9 | `behavior_is_documented`→`remediation_target=docs` derivation consistent skill↔consumer | PASS | skill L75 `docs when behavior_is_documented indicates a doc gap`; consumer L225 `If behavior_is_documented == true (or remediation_target == "docs")`. Aligned. |
| 10 | Cross-reference labels (`Wave 5 step 4.5`) accurate | PASS | report-template L158 cites "Wave 5 step 4.5" → skill L471 is literally step "4.5". task-protocol L219 cites "Wave 5 emission". Targets exist. |

## Summary

- Checks passed: 9 / 10
- Checks failed: 1
- Critical issues: 0
- Important issues: 1 (F1)
- Minor issues: 2 (F2, F3)
- Issues fixed in-place: 0 (REPORT ONLY — fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | `src/superclaude/commands/troubleshoot.md` L59 | The `--context` flag is described as: "Path to a caller-supplied context file (e.g. TFEP `return-contract.yaml` consumer brief)." This mislabels the INPUT file. `return-contract.yaml` is the OUTPUT artifact troubleshoot *emits* in Wave 5 step 4.5 — it is never the inbound `--context` file. The producer (task-protocol §4.5 Step 2, sc-task-protocol SKILL.md L205) writes `{output_dir}/context.yaml` (a `failure_context` package) and passes THAT as `--context {context_path}` (L215). The troubleshoot skill (SKILL.md L148) correctly calls it "the caller brief" (neutral, no filename). So the command conflates the input contract file (`context.yaml`) with the output contract file (`return-contract.yaml`). A user following the command doc would supply the wrong file. | Change the example to the inbound file, e.g. "(e.g. the TFEP `context.yaml` failure-context brief)" — or drop the filename and mirror the skill's neutral "caller brief" wording. Do NOT name `return-contract.yaml` here. |
| F2 | MINOR | `refs/report-template.md` L14 (report header `**Status**`) and `SKILL.md` L457 (audit SUMMARY footer `status`) | Both render the `status` enum as `<success\|partial>` (2 values), but the Output Contract (SKILL.md L43) and the TFEP Consumer block (report-template L161) render it as `success\|partial\|failed` (3 values). The task-protocol consumer branches on `status == "failed"` (L230), so `failed` is a live consumed value. The TFEP wire echo (L161) carries all 3 correctly, so the TFEP path itself is consistent — but the report header/footer drop `failed`. | Pre-existing inconsistency, broader than the TFEP wire set. For TFEP-path correctness it is non-blocking (the consumed YAML block is correct). Recommend aligning the report header + audit footer to `<success\|partial\|failed>` for global consistency, but this is outside the strict 5-field TFEP migration scope — flag, do not block on it. `[OUT-OF-SCOPE for fix]` |
| F3 | MINOR | `src/superclaude/commands/troubleshoot.md` L59 | Same line also states `--context` content is "echoed in the Wave 5 return." The skill records `context_path` in the audit TARGET header (L144) and SUMMARY footer (L466), and Wave 5 step 5 surfaces the `return-contract.yaml` path — but the `--context` *content* is not echoed back to the user. Defensible via the audit footer carrying `context_path`, so this is a wording-precision nit, not a contradiction. | Optional: tighten to "recorded in the audit-log header/footer" rather than "echoed in the Wave 5 return," to avoid implying the content is surfaced to the user. |

## Notes / Cleared Suspicions (adversarial sweep — checked and found CONSISTENT)

- **contract_version absent from consumer (F6 note):** The task-protocol consumer reads adapter fields by NAME (`recommended_escalation`, `remediation_target`, etc.), not gated on a `contract_version` string. The producer stamps `1.1.0` (SKILL.md L62); the consumer never needs to assert a version. No inconsistency — NOT a finding.
- **`test_file_path` not in the 7-field wire set:** Skill L471 explicitly and correctly justifies the omission (consumer presents-to-user on `remediation_target=test`, does not auto-fix; path available via broader Output Contract). Consumer never reads `test_file_path` from the wire. Consistent by design.
- **TFEP Consumer block "report-rendered echo" vs separate `return-contract.yaml` file:** The report-template L161-167 YAML block (rendered into REPORT.md) and the `return-contract.yaml` file (Wave 5 step 4.5) are both derived from the same 7 fields — the block is a faithful echo. Consistent.
- **5 adapter fields + 2 enums framing:** The 2 enums (`recommended_escalation`, `remediation_target`) are 2 of the 5 adapter fields; all 5 present and consistent in every required location. Confirmed.

## Actions Taken

None. `fix_authorization: false` — report only. No files modified.

## Recommendations

1. **Fix F1 before merge** (IMPORTANT): correct the `--context` example in `troubleshoot.md` L59 so it names the inbound `context.yaml`, not the outbound `return-contract.yaml`. This is the one genuine cross-file naming inconsistency in the migration's wire contract.
2. Consider F2 (status enum 3-value alignment in report header + audit footer) as a separate, broader cleanup — out of strict TFEP-migration scope.
3. F3 is an optional wording tightening on the same command line as F1; fold it into the F1 fix.

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 5 (each Bash invocation ran 1-3 targeted greps directly mapping to checklist items 1-10; no external web lookup needed — all claims are local source-truth)
- Every checklist item categorized [x] VERIFIED with cited file:line tool evidence (table above).
- No UNCHECKED items. No UNVERIFIABLE items.

## QA Complete
