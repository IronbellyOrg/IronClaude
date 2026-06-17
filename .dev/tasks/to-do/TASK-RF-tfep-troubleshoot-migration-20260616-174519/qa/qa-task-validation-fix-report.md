# QA Task-Validation Fix Report (A.10 / A.10.25 serialized fix agent I20)

**Task file:** TASK-RF-tfep-troubleshoot-migration-20260616-174519.md
**Consolidated findings:** qa/qa-task-validation-consolidated.md
**Fix authorization:** true (single serialized fix agent)
**Date:** 2026-06-16
**Result:** ALL 8 findings (F1–F8) applied in-place. No items marked "NOT fixed (accept as-is)" were touched.

---

## Verdict

**PASS** — all 8 consolidated findings applied. Task file remains well-formed: 123 checklist items, 123 B2 completion gates (1:1), Phase 5 renumbered cleanly (5.1–5.11), Phase 6 gained Step 6.0 (6.0–6.5), no dangling step references, no orphaned "Steps 5.1–5.7" range refs.

---

## Per-finding changelog

### F1 (IMPORTANT) — Split old Step 5.5 into Read-baseline + exact-edit
- **Old Step 5.5** ("Confirm/encode the Step 4 status branches … make ONLY the minimal edits needed") had a non-deterministic action and presumed branch text without Read-confirming it.
- **NEW Step 5.5** "Read-baseline the Step 4 status branches (record exact current text)" — a no-edit item that Reads the four status branches (lines ~219–222) and records each verbatim into the `### Phase 5 - Consume Findings` section under a `Step 4 status-branch baseline` sub-heading. Post-condition: baseline contains the four branch strings verbatim and is readable by Step 5.6.
- **NEW Step 5.6** "Align the Step 4 status branches to the adapter enum (exact edit)" — reads the 5.5 baseline + re-Reads the branches, then makes the exact edits giving the precise per-branch end-state text (per R-005 / R-002). Includes the precise dispatch-aligned enum mapping. rg-checkable post-condition: `rg -n "recommended_escalation" …SKILL.md` shows ONLY enum values `none|retry|escalate_depth|halt`; `rg -n "test_is_wrong" …` still shows the `Do NOT auto-fix tests` branch intact.

### F2 (IMPORTANT) — Split old Step 5.6 (a)–(d) into individual ASSERT/INSERT items
Old Step 5.6 conflated four sub-conditions with only (d) carrying concrete text. Split into:
- **NEW Step 5.7** ASSERT Step 5 reads `tasklist_insertion_path` (Phase 4 Step 4.2 field). Post-condition: `rg -n "tasklist_insertion_path" …SKILL.md` ≥1 hit in Step 5 block.
- **NEW Step 5.8** ASSERT the plan is composed from `remediation_target` / `root_cause_summary` / `solution_summary`. Post-condition: `rg -n "remediation_target|root_cause_summary|solution_summary" …` hits each token.
- **NEW Step 5.9** ASSERT append-not-replace insertion before existing test/verification tasks. Post-condition: `rg -n "append-not-replace|before existing test" …` ≥1 hit.
- **NEW Step 5.10** INSERT the Option-1 ownership statement — verbatim text: `(Remediation ownership: troubleshoot diagnoses and emits the contract under --caller task-unified with NO --fix; task-protocol owns this insertion and the Step 6 resume — see the Diagnostic backend declaration.)`. Post-condition: `rg -n "Remediation ownership: troubleshoot diagnoses" …` == exactly one hit.
- Old **Step 5.7** "Sync and verify" renumbered to **Step 5.11** (content unchanged).

### F3 (IMPORTANT) — New Step 6.0 + rewritten Step 6.1 (remove unbounded fallback)
- **NEW Step 6.0** "Enumerate the incident-report template fields (pre-rebind baseline)" — Reads the fenced incident template (~241–251), enumerates EVERY field line verbatim into `### Phase 6 - Reporting & Budget Findings` under an `Incident-template field enumeration` sub-heading, naming the Root-cause / Solution / Diagnostic-artifacts lines so 6.1/6.2/6.3 each act on a named line. No edit. If a field is absent, records the absence explicitly.
- **Rewritten Step 6.1** — now acts on the enumerated Root-cause line with the EXACT R-005 G2 mapping (`rca-verdict.md` → REPORT.md **Diagnosis** / `root_cause_summary`). The open-ended "rebind the nearest equivalent" fallback is REMOVED and replaced with a deterministic rule: if no Root-cause field exists, log the absence and leave the template verbatim (no judgment rebind). Phase 6 intro paragraph updated to describe Step 6.0 and the no-"nearest equivalent" guarantee.

### F4 (IMPORTANT) — Objective post-conditions on F1–F3 items
- Step 5.6 / 5.7 / 5.8 / 5.9 / 5.10 each carry an `rg`-checkable post-condition (see F1/F2 above).
- Step 6.1 post-condition: `rg -n "rca-verdict" …` == 0; `rg -n "Diagnosis|root_cause_summary" …` shows rebound source.
- Step 6.2 post-condition added: `rg -n "solution-verdict" …` == 0; `rg -n "Proposed Fix|solution_summary" …` shows rebound source.
- Step 6.3 post-condition added: `rg -n "Diagnostic artifacts.*report_path|…audit_log_path" …` ≥1; `rg -n "Diagnostic artifacts.*\{path to output_dir\}" …` == 0 (old placeholder gone).

### F5 (MINOR) — Step 5.3 restate the depth selection rule inline
- Step 5.3 dispatch-line rewrite now restates the rule inline so the item is self-contained: `--depth standard` for 1st/simple trigger; `--depth deep` for systemic failure, ≥3 new failing tests, or a 2nd (escalation) trigger (per R-002 §C / R-005 G1). No longer leans silently on Step 5.2's enum.

### F6 (MINOR) — PC.5 Summary verification made rg-checkable
- Step PC.5 ("Write the Task Summary") soft "no fabrication" check replaced with an objective post-condition: the Summary must cite each of the 8 pipeline changes paired with the file it touched (all five edited files named), AND `rg -n "/sc:forensic|\bforensic\b" sc-task-protocol/SKILL.md task.md` must return 0 live hits (non-zero ⇒ Summary is premature).

### F7 (MINOR, alignment Finding 2) — Reconciliation note for dropped report-block field names
- Step 4.9 (`## TFEP Consumer` report-template block) gained a RECONCILIATION NOTE: R-003 §2's speculative `tasklist_insertion_recommendation` / `safe_to_auto_insert` names were INTENTIONALLY reconciled to the consumer-side `tasklist_insertion_path` so producer and consumer use one canonical token — the dropped names are deliberate, not lost.

### F8 (MINOR, alignment Findings 1+3) — `recommended_escalation` enum provenance + retry routing
- **(a)** Step 4.1 gained a DESIGN NOTE: the `none|retry|escalate_depth|halt` enum is TASK-AUTHORED additive design (appears in no research file; legitimate fill for the additively-added field), covered by the same `contract_version` bump (Step 4.6) + NFR-6 discipline.
- **(b)** Phase 5 Step 5.6 (the consume item) now names a consumer branch for every enum value: `none` → remediation ready (insert + resume); `retry` → re-run `/sc:troubleshoot` once at the SAME `--depth`; `escalate_depth` → re-invoke at `--depth deep`; `halt` (or `status == "failed"`) → FULL STOP. This closes the previously-unbranched `retry` value.

---

## Reference-integrity updates (consequential renumber)
- PG5.1 (Phase 5 aggregate) updated: "Steps 5.1–5.7" → "Steps 5.1–5.11", with the new 5.5/5.6 split and 5.7–5.10 asserts/ownership-note enumerated.
- No phase-header item-count claims existed to update (grep confirmed none).

## Items explicitly NOT touched (accept-as-is, per consolidated §"NOT fixed")
- structure-lens MINOR: `template_schema_doc` `.claude/` mirror path — left.
- structure-lens MINOR: 118-checkbox total / 6 standard-intensity gates — left.
- b2-lens Issue 6: Step 6.4 bounded fabrication-avoidance judgment — left.

## Post-fix structural verification (tool evidence)
- `grep -c "^- \[ \]"` == 123; `grep -c "Once done, mark this item as complete."` == 123 (1:1 — no malformed/unterminated items).
- Phase 5 headers: 5.1–5.11 contiguous. Phase 6 headers: 6.0–6.5 contiguous.
- `grep -nE "Step 5\.1[2-9]|Step 6\.[6-9]|Steps 5\.1–5\.7"` → CLEAN (no dangling refs).
- All `nearest equivalent` occurrences are in NEGATED ("do NOT rebind a nearest equivalent") form — the unbounded fallback is gone.
