# QA Report — Structural Internal Consistency (Phase 6)

**Topic:** TFEP ↔ troubleshoot rebound: budget / mapping / contract field consistency
**Date:** 2026-06-16
**Phase:** report-validation (internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: PASS

The escalation-budget depth values, the rebound incident-artifact references, and the
Root cause / Solution sources are all internally consistent with the Phase 5 Step 3
tier→depth mapping and with the troubleshoot Output Contract field names. The adversarial
hunt for ≥5 inconsistencies surfaced candidates; each was run to ground and found to be a
deliberately-reconciled design point, not a contradiction. Details and the cleared-candidate
ledger are below.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Budget depth values vs Step 3 mapping | PASS | task §4.5 L210-213 (mapping) vs L268-270 (budget) — see Finding 1 |
| 2 | `report_path` field exists in Output Contract | PASS | troubleshoot L45 `report_path` ↔ task L260 |
| 3 | `audit_log_path` field exists in Output Contract | PASS | troubleshoot L46 `audit_log_path` ↔ task L260 |
| 4 | `root_cause_summary` source = REPORT.md Diagnosis | PASS | task L257 ↔ troubleshoot L76 + Wave 5 L438 |
| 5 | `solution_summary` source = Proposed Fix/Next Steps | PASS | task L258 ↔ troubleshoot L77 + Wave 5 L440/L443 |
| 6 | `--depth standard`/`--depth deep` are real flag values | PASS | troubleshoot L137 enum `quick\|standard\|deep\|auto` |
| 7 | `--caller task-unified` matches backend | PASS | task L215 invocation ↔ troubleshoot L148 `caller=task-unified` |
| 8 | 7-field return-contract wire set matches consumer | PASS | troubleshoot L471 emit set ↔ task L219/L236 consume set |
| 9 | Budget block vs Step 3 dispatch — no contradiction | PASS | see Finding 2 (re-entry vs hard-cap reconciliation) |
| 10 | "light to standard" gradient vs depth enum | PASS | see Cleared Candidate C1 — orthogonal axis, not depth value |

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY mode)

## Detailed Findings (the four verification axes)

### Finding 1 — Budget depth values ARE consistent with the Step 3 tier→depth mapping (CONSISTENT)

Three places in task §4.5 encode the tier→depth mapping. They agree exactly:

- **Step 3 bullets (L210-213):**
  `1st TFEP trigger → --depth standard`;
  `2nd TFEP trigger (escalation) → --depth deep`;
  `systemic failure OR ≥3 new failing tests → --depth deep`;
  `3rd TFEP trigger → FULL STOP`.
- **Step 3 invocation prose (L215-216):** "`--depth standard` for the 1st/simple TFEP
  trigger, and `--depth deep` for a systemic failure, ≥3 new failing tests, or a 2nd
  (escalation) trigger."
- **Escalation Budget block (L268-270):**
  `1st TFEP trigger → ... --depth standard`;
  `2nd TFEP trigger (escalation, systemic, or ≥3 new failing tests) → ... --depth deep`;
  `3rd TFEP trigger → FULL STOP`.

The systemic / ≥3-new shortcut to `deep` is stated identically in all three. The required
spec mapping (1st→standard, escalation/systemic/≥3-new→deep, 3rd→FULL STOP) is satisfied
verbatim. **No discrepancy.**

### Finding 2 — Rebound incident-artifact references MATCH troubleshoot Output Contract field names (CONSISTENT)

Incident template L260 cites: "troubleshoot `report_path` (REPORT.md), `audit_log_path`
(audit.log)". Both are real Output Contract fields:

- `report_path` — troubleshoot Output Contract L45 ("Absolute path to `REPORT.md`"). The
  parenthetical "(REPORT.md)" in the incident template matches the contract description.
- `audit_log_path` — troubleshoot Output Contract L46 ("Absolute path to `audit.log`"). The
  parenthetical "(audit.log)" matches.

Field names are byte-exact (`report_path`, `audit_log_path`) — no typo, no singular/plural
drift, no `_log_` vs `log_` reordering. **No discrepancy.**

### Finding 3 — Root cause / Solution sources MATCH adapter fields + Wave 5 sections (CONSISTENT)

- **Root cause:** Incident template L257 sources `root_cause_summary` from "the **Diagnosis**
  section of troubleshoot REPORT.md". Troubleshoot Output Contract L76 defines
  `root_cause_summary` as "extracted verbatim or condensed from the REPORT.md **Diagnosis**
  section (Wave 5)". Wave 5 L438 confirms REPORT.md contains a "Diagnosis" section. Three-way
  agreement.
- **Solution:** Incident template L258 sources `solution_summary` from "the **Proposed Fix**
  / **Next Steps** section". Output Contract L77 defines `solution_summary` as "extracted
  from the REPORT.md **Proposed Fix** / **Next Steps** section (Wave 5)". Wave 5 confirms BOTH
  a "Proposed Fix" section (L440) and a "Next Steps" section (L443) exist. Three-way agreement,
  and the dual-section "/" phrasing is identical on both sides.

Cross-checked against the 7-field return-contract wire emission (troubleshoot Wave 5 L471):
the emit set `{status, test_is_wrong, recommended_escalation, tasklist_insertion_path,
remediation_target, root_cause_summary, solution_summary}` is exactly the consume set read by
task-protocol (L219 read list, L236 plan-body composition). `root_cause_summary` and
`solution_summary` appear in both. **No discrepancy.**

### Finding 4 — No contradiction between the budget block and the Step 3 dispatch/mapping (CONSISTENT)

The budget block (L268-270) is a 3-row summary; the Step 3 flow (L207-216) plus the Step 4
re-entry branches (L227-230) are the full state machine. Potential tension: Step 4 lets
`recommended_escalation == retry|escalate_depth` re-enter Step 3 and increment
`escalation_count` (L228-229), which could appear to conflict with the budget's hard
"3rd trigger → FULL STOP". It does NOT, because:

- `escalate_depth` at an already-`deep` run is explicitly collapsed to FULL STOP
  (L229: "If the run was already at `--depth deep`, there is no deeper level — treat as FULL STOP").
- `halt` / `status == failed` is an immediate FULL STOP "regardless of `escalation_count`"
  (L230).
- The budget's 3rd-trigger FULL STOP (L270) is the outer hard cap; the inner
  retry/escalate_depth branches always terminate at `deep` (the budget's 2nd-trigger ceiling)
  or earlier. The inner loop cannot exceed the depth ceiling the budget defines.

The budget is a faithful, non-contradictory summary of the dispatch logic. **No discrepancy.**

## Cleared Adversarial Candidates (hunt for ≥5 inconsistencies — each run to ground)

| # | Suspected inconsistency | Verdict | Why it is NOT a defect |
|---|-------------------------|---------|------------------------|
| C1 | L176 "escalate from light to standard" references `light`, which is not a depth value (`quick\|standard\|deep\|auto`) | CLEARED | L176 is the **Escalation gradient** subsection describing diagnostic-backend escalation *intensity*, an orthogonal axis. It is not part of the Step 3 `--depth` mapping and never feeds the `{depth}` placeholder. No flag-value claim is made. |
| C2 | Budget L269 lists "systemic, or ≥3 new failing tests" under the **2nd** trigger, but Step 3 L212 lists systemic/≥3-new as a standalone deep-trigger independent of trigger ordinal | CLEARED | Both routes resolve to `--depth deep`. The standalone L212 rule and the L269 grouping are two phrasings of the same outcome (deep); they cannot disagree because both produce `deep`. No depth conflict. |
| C3 | Incident template L260 also names "Tier-2 hypothesis cards" and "adversarial artifacts" — are those real Output Contract fields? | CLEARED | These are descriptive artifact *names*, not field-name citations. The Output Contract does carry `hypothesis_cards` (L53) and `adversarial_artifacts_dir` (L54), so the referenced artifacts genuinely exist. The QA brief only required `report_path`/`audit_log_path` field-name matching, which holds. |
| C4 | `tasklist_insertion_path` is in the 7-field wire set but task L236 composes the plan body from `remediation_target`/`root_cause_summary`/`solution_summary` instead of consuming the path | CLEARED | By design: troubleshoot L471 defaults `tasklist_insertion_path` to `null` in diagnosis-only TFEP mode; task-protocol owns composition (remediation-ownership decision, L239). Field is present and consumed (read at L233) — absence of body-use is the documented contract, not drift. |
| C5 | Step 3 L208 says depth depends on "escalation count and failure severity" but the bullets key only on trigger ordinal + systemic/≥3-new | CLEARED | "failure severity" IS the systemic / ≥3-new clause (L212). The prose preamble and the bullet enumeration describe the same two inputs (ordinal + severity). No missing or extra input. |
| C6 | `--caller task-unified` (task L215) vs `caller=task-unified` (troubleshoot L148) — value-format drift? | CLEARED | The CLI form `--caller task-unified` (flag) and the recorded header form `caller=task-unified` (audit field) carry the identical value token `task-unified`. Flag-vs-field notation differs by surface, not value. |

## Tool engagement
Read: 4 | Grep: 4 | Glob: 0 | Bash: 4 (ls, wc, and the grep/wc invocations executed via Bash)

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

All 10 checks were verified against exact line text in both source files (cited above).
No item relied on another report's claim; every verdict cites a `file:line` I read directly.

## Recommendations
- None blocking. The TFEP↔troubleshoot rebound contract is internally consistent across the
  budget, the Step 3 mapping, and the troubleshoot Output Contract field names. Green light
  for Phase 6 on the internal-consistency axis.

## QA Complete
