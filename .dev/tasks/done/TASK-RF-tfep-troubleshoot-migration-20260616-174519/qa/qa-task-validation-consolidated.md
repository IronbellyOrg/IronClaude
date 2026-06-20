# Consolidated Task-Validation Findings (A.10 + A.10.25)

**Task file:** TASK-RF-tfep-troubleshoot-migration-20260616-174519.md
**Gate verdicts:** structure=PASS, research-alignment=PASS (3 MINOR), b2-self-containment=FAIL (4 IMPORTANT + 3 MINOR)
**Action:** ONE serialized fix agent applies ALL items below (fix_authorization: true). Max 3 fix-verify cycles.

---

## IMPORTANT (must fix — from b2-self-containment lens)

**F1 — Step 5.5 non-deterministic "minimal edits" action.** Step 5.5 says "make ONLY the minimal edits needed" with no exact target text and presumes branch text without Read-confirming it. FIX: split into two B2-complete items — (a) a Read-baseline item that reads the current sc-task-protocol/SKILL.md §4.5 Step 3/Step 4 text and records the exact current strings into the Phase 5 Findings; (b) an exact-edit item giving the precise old→new replacement text (the `/sc:forensic ... --depth quick` dispatch → `/sc:troubleshoot "<TFEP issue + context path>" --type test --depth <standard|deep> --caller task-unified --context {context_path} --output-dir {output_dir}`), with an `rg`-checkable post-condition.

**F2 — Step 5.6 conflates assertions vs inserts.** "verify/encode that Step 5 (a)…(d)" never says which sub-conditions are assertions vs new inserts; only (d) has concrete text. FIX: split each of (a)–(d) into its own item, each labelled ASSERT (with the exact `rg`/Read check that must hold) or INSERT (with the exact text to add). The Option-1 ownership statement (TFEP passes NO --fix; task-protocol owns insertion+resume) is an INSERT with verbatim text.

**F3 — Step 6.1 unbounded fallback + unenumerated template.** Step 6.1 embeds "rebind the nearest equivalent" (executor judgment) and asserts an incident-template Root-cause field exists without enumerating it. FIX: (a) add a new **Step 6.0** that Reads sc-task-protocol/SKILL.md incident-report fenced block (~241–251) and enumerates every field line into the Phase 6 Findings BEFORE any rebind; (b) rewrite 6.1 to act on the enumerated field list with the EXACT G2 mapping from R-005 (rca-verdict.md→REPORT.md Diagnosis section; solution-verdict.md→Proposed Fix/Next Steps; Forensic artifacts→Diagnostic artifacts: report_path + audit_log_path + hypothesis cards + adversarial artifacts; "committed... forensic artifacts"→"...diagnostic artifacts"). Remove the open-ended fallback; if a field has no mapping, log it to Findings and leave verbatim (no judgment rebind).

**F4 — Unmeasurable verification clauses (consequence of F1–F3).** Once F1–F3 give fixed end-states, attach objective post-conditions to each: `rg -n "<old token>" <file>` returns 0, or `rg -n "<new token>" <file>` returns the expected count. No "verify it works" / "exactly as described" as the sole check.

## MINOR (fix — b2 + alignment lenses)

**F5 — Step 5.3 restate depth enum.** 5.3 leans on 5.2's depth enum without restating. FIX: restate the `--depth standard|deep` selection rule inline (standard = 1st/simple trigger; deep = systemic / ≥3 new tests / 2nd trigger).

**F6 — PC.5 soft verification.** PC.5 Summary verification is "no fabrication". FIX: make it checkable — "the Summary cites each of the 8 changes with the file it touched; `rg` each renamed token shows 0 residual in the two task-protocol files."

**F7 (alignment Finding 2) — reconciliation note.** R-003 §2 suggested report-block field names `tasklist_insertion_recommendation` / `safe_to_auto_insert` were reconciled to the consumer-side `tasklist_insertion_path`. FIX: add a one-line reconciliation note in the Step 4.9 (report-template block) item and/or Open Questions so the dropped field names read as intentional, not lost.

**F8 (alignment Finding 1+3) — `recommended_escalation` enum + retry routing.** The task-authored `recommended_escalation` enum (`none|retry|escalate_depth|halt`) appears in no research file (legitimate design fill for the additively-added field), and its `retry` value has no named consumer branch in Phase 5. FIX: (a) add a short note in the Step 4.x adapter item that this enum is task-authored design (additive, contract_version-bumped), and (b) add/҂name the consumer branch for each enum value in the Phase 5 consume item (none→insert+resume; retry→re-run same depth once; escalate_depth→re-invoke troubleshoot at --depth deep; halt→FULL STOP per the 3rd-trigger budget).

## NOT fixed (accept as-is — advisory only)

- structure-lens MINOR: `template_schema_doc` points at the `.claude/` mirror path — this matches the template's own convention; leave.
- structure-lens MINOR: 118-checkbox total driven by 6 standard-intensity gates — justified by PER_PHASE requirement; leave.
- b2-lens Issue 6 (Step 6.4 bounded fabrication-avoidance judgment) — acceptable bounded judgment; leave.
