# Phase 6 Output Summary — Incident Reporting Rebind + Escalation Budget Restatement

**Date:** 2026-06-16
**File edited:** `src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5 (incident template + escalation budget)
**verify-sync:** EXIT 0, no drift, no `.claude/` staged (`test-results/phase-6-verify-sync.txt`)

Snippets from the captured `git diff`.

## Step 6.0 — incident-template field enumeration
Recorded verbatim in the Phase 6 - Reporting & Budget Findings section. All three rebind targets
(Root cause, Solution, Diagnostic artifacts) present and named — no "nearest-equivalent" judgment needed.

## Step 6.1 — Root cause rebind (G2)
- **Before:** `- **Root cause**: {summary from rca-verdict.md}`
- **After:**  `- **Root cause**: {\`root_cause_summary\` from the return contract, sourced from the **Diagnosis** section of troubleshoot REPORT.md}`
- Post-condition: `rca-verdict` → 0 hits; `Diagnosis`/`root_cause_summary` present in incident template.

## Step 6.2 — Solution rebind (G2)
- **Before:** `- **Solution**: {summary from solution-verdict.md}`
- **After:**  `- **Solution**: {\`solution_summary\` from the return contract, sourced from the **Proposed Fix** / **Next Steps** section of troubleshoot REPORT.md}`
- Post-condition: `solution-verdict` → 0 hits; `Proposed Fix`/`solution_summary` present.

## Step 6.3 — Diagnostic artifacts value rebind (G2)
- **Before:** `- **Diagnostic artifacts**: {path to output_dir}`
- **After:**  `- **Diagnostic artifacts**: troubleshoot \`report_path\` (REPORT.md), \`audit_log_path\` (audit.log), Tier-2 hypothesis cards, and any adversarial artifacts`
- Post-condition: `Diagnostic artifacts.*report_path|audit_log_path` present; `{path to output_dir}` → 0 hits.

## Step 6.4 — Escalation Budget restatement (Change 8)
- **Before:** `1st → /sc:forensic --tier light --intent triage (~5-8K tokens)`; `2nd → /sc:forensic --tier standard (~15-20K tokens)`; `3rd → FULL STOP...`
- **After:**  `1st TFEP trigger → /sc:troubleshoot --caller task-unified --depth standard`; `2nd TFEP trigger (escalation, systemic, or ≥3 new failing tests) → /sc:troubleshoot --caller task-unified --depth deep`; `3rd TFEP trigger → FULL STOP. Report to user. Do not attempt further fixes.`
- Forensic `--tier`/`--intent` gone; systemic/≥3-new-tests → deep mapping encoded; depth values match the Phase 5 Step 3 mapping; fabricated token-band figures (~5-8K, ~15-20K) DROPPED (not invented for troubleshoot).

## Step 6.5 — sync + verify-sync → EXIT 0.

## Residual-forensic sweep (post-Phase-6, pre-PG6)
`grep -E "/sc:forensic|\bforensic\b|--tier|--intent|rca-verdict|solution-verdict"` on
sc-task-protocol/SKILL.md → **ZERO live hits**. The migration left no orphaned forensic reference
in the task-protocol skill.

No fabrication: every snippet is from the captured `git diff`.
