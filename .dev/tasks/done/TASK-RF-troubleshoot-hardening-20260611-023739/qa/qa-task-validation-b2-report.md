# QA Report — Task Integrity Check (B2 Self-Containment Lens)

**Topic:** Pipeline Hardening Closure mode (H0-H5 + waiver/no-re-greening latch) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: FAIL

FAIL is driven by one IMPORTANT defect (unresolved `{EXECUTOR_CLASS}` placeholder inside an embedded agent-spawn command, Step 8.14) plus one IMPORTANT internal-consistency defect (the Phase 7 preamble asserts "One checklist item per test" while the lens-mandated "each of the 18 tests its OWN item" is violated — 18 test functions are batched into ~11 author items). Remaining findings are MINOR. None of the findings are CRITICAL; the core B2 self-containment posture is strong (no "see above" references, full path discipline, embedded QA prompts, correct OI HALT markers, no stale draft §-numbering). Per zero-tolerance gate policy, ANY issue of ANY severity = FAIL.

---

## Confidence

**Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%**

**Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 6 (all targeted: spec advisory-enum, truth-table rows, OI items, test-plan counts, §1.2/§9 line refs, task self-containment scans). No web research performed (all claims local).

---

## Items Reviewed (B2 Self-Containment Lens, 8 checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has all 5 B2 components (context+action+output+verification+completion gate) | PASS (with 1 defect → see #5) | Sampled every author item (Steps 2.1–7.18, 8.2–8.16): each opens with Read-context, states the create/modify action + exact output path, has explicit acceptance criteria + mapped §8 test, and ends "Once done, mark this item as complete." Defect: Step 8.14 verification embeds an unresolved placeholder (Finding 1). |
| 2 | No item references prior-item context without restating it | PASS | `grep -Ei 'see above\|continue from\|as described above\|previous item\|same as'` → 0 hits. Items that consume earlier outputs (e.g. 5.1/5.2 read `skill-anchors.md`; 6.1/6.2 read `report-handoff-anchors.md`; 7.x read the authored refs) all restate the FULL absolute path of the upstream artifact. |
| 3 | Agent-spawning items have FULLY embedded prompts (not "see SKILL.md") | PASS | Steps 8.2–8.8 each carry a complete quoted lens prompt (adversarial framing, inputs by path, verification list, output report path, "Do NOT modify any file"). Steps 8.10 (fix agent) + 8.11 (2 verification agents) embed inline instructions (fix_authorization, targets, output paths, I20 serialization). Step 8.14 embeds the reflect invocation inline — but with a placeholder (Finding 1). |
| 4 | File paths specific (the 6 refs, 4 mods, test files) — not "the relevant file" | PASS | Every ref/mod/test item names the exact `src/superclaude/skills/sc-troubleshoot-protocol/refs/<file>.md` or `tests/troubleshoot/<file>.py` path. No generic "the relevant file" phrasing in any action clause. |
| 5 | Verification criteria measurable (FR acceptance + mapped §8 test), not "verify it works" | PASS (with 1 placeholder defect) | Each author item ends with "The acceptance criteria are FR-N (AC…) … the mapped §8 test is `test_…`." Verified against spec §8.1/§8.2 (Bash): all named test functions exist in the spec test plan except the intentionally-NEW `test_h2_sibling_sweep_required_when_concept_shared` (correctly flagged as G-PRE-1 reflect-gap addition; absent from spec §8.1 by design). Defect: Step 8.14 `{EXECUTOR_CLASS}` is not measurable as written (Finding 1). |
| 6 | No batch items — each ref / test / E2E scenario / modified file has its OWN item | PARTIAL FAIL | Refs: PASS (2.1, 2.2, 3.1, 3.2, 3.3, 4.1 — one per ref). Modified files: PASS (5.1+5.2 SKILL, 5.3 cmd, 6.1 report, 6.2 handoff). E2E scenarios: PASS (7.13–7.18 — one per scenario). **Tests: FAIL** — the lens requires "each of the 18 tests its OWN item," but 18 test FUNCTIONS are batched into per-module items (7.2=2 fns, 7.4=2, 7.5=2, 7.6=3, 7.7=3); the Phase 7 preamble even self-contradicts: "One checklist item per test" (L265) is literally false (Finding 2). |
| 7 | No items based on stale draft §6.2/§7/§9 numbering or superseded design (5 refs / 8 fields / tests=NONE) | PASS | All spec anchors in items use the v1.1.0 §3/§4/§5/§8 final numbering. The `§9`/`§1.2` references (G1 gate L42, rollback L586) were verified by Bash to be REAL v1.1.0 spec sections (§1.2 Scope Boundary @L38, §9 Migration & Rollout @L582), NOT the deprecated draft §6.2/§7/§9 the Key-Constraints warning (L135) cautions against. Deliverable inventory uses the corrected 6 refs / 10+1 fields / 18 tests (not the superseded 5/8/NONE). |
| 8 | The 3 needs_human_decision items (OI-2/3/5) write PENDING + halt their dependent mutation, never auto-default | PASS | Steps 1.5 (OI-2), 1.6 (OI-3), 1.7 (OI-5) each create an `OI-N-PENDING.md` with `STATUS: PENDING HUMAN DECISION`, the verbatim question, and an explicit "MUST NOT finalize / MUST NOT auto-default" instruction that names the exact dependent downstream item it halts (OI-2→Step 3.3 contract_token open-enum; OI-3→Step 3.1 substitute-witness classes; OI-5→`target_release` stamp, kept DISTINCT from `contract_version 1.0.0`). Confirmed against spec §11: OI-2/3/5 are the genuinely-open items; OI-1/4/6 resolved in-spec (§5.4/§5.7) and correctly excluded. |

---

## Summary

- Checks passed: 6 / 8 fully PASS; 2 carry defects (checks #5/#1 share the placeholder defect; check #6 is a partial FAIL).
- Checks failed (gate sense): 2 distinct defects elevate the gate to FAIL.
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Step 8.14 (L413) | The embedded POST-reflect command contains a literal unresolved placeholder: `--executor-model {EXECUTOR_CLASS}`. A self-contained item (B2) must give the executor a runnable token, not a template variable to guess. Violates B2 item 5 (measurable/concrete) and the placeholder-scan rule. | Replace `{EXECUTOR_CLASS}` with the actual executor model class (or with explicit inline guidance, e.g. "set `--executor-model` to the model that ran Phase 1–7, default `opus`"). Do not ship a brace-delimited template token. |
| 2 | IMPORTANT | Phase 7 preamble (L265) vs Steps 7.2/7.4/7.5/7.6/7.7 | Self-contradiction + B2 batch violation: the preamble asserts "One checklist item per test," but the 18 test functions are authored in per-MODULE items that each create 2–3 test functions (7.2→2, 7.4→2, 7.5→2, 7.6→3, 7.7→3). The B2 lens explicitly requires "each of the 18 tests its OWN item." | Either (a) split each multi-function test item into one item per test function (true 18 items), OR (b) correct the L265 preamble to state "one checklist item per test MODULE" and have the lens owner accept per-module granularity. Recommend (b) as the lighter fix since each per-module item is otherwise fully self-contained and names every function it authors. |
| 3 | MINOR | Step 7.12 (L313) | Optionality leak: "alternatively the executor MAY append to `test_hardening_output_contract.py` if preferred." An either/or destination makes the produced-file set nondeterministic, which Step 8.13's Glob check then has to hedge ("`_report_closure.py` if created", L409). Mild B2 self-containment / determinism wrinkle. | Pick ONE destination for `test_report_closure_section_not_proven_blockers` (recommend the dedicated `test_hardening_report_closure.py`) and remove the "alternatively" clause so the deliverable set is fixed. |
| 4 | MINOR | Steps 7.13–7.18 (E2E) | Each E2E item correctly has its own item, but verification is "scenario text derived verbatim from §8.3 #N … markdownlint-clean" — there is no pytest assertion (by design: documented fixtures deferred to M5). This is acceptable per the Builder Notes (L509) and the non-code-task inline-verification exception, but the items lean on a project-level decision rather than a per-item measurable gate. No fix required; noted for completeness. | None required — flagged for transparency. The deferral rationale is documented (L494/L509). |

---

## Actions Taken

None — `fix_authorization: false`; this is a report-only B2 task-integrity pass. All findings are documented above for the orchestrator's fix cycle.

---

## Recommendations

1. **Before execution:** resolve Finding 1 (the `{EXECUTOR_CLASS}` placeholder in Step 8.14) — it is the only finding that would actually break a runnable command at execution time.
2. **Reconcile Finding 2** by correcting the Phase 7 preamble wording (L265) OR splitting the test items — whichever the lens owner prefers. The current text is internally contradictory and must not ship as-is.
3. Findings 3–4 are MINOR polish; resolve Finding 3 to keep the Step 8.13 Glob check deterministic.
4. **Strengths to preserve (do not regress in the fix cycle):** zero "see above" references, full absolute-path discipline, fully-embedded QA-lens prompts, correct OI-2/3/5 PENDING+HALT markers, accurate v1.1.0 §-anchoring, and the triple-guarded advisory 4-token invariant (Step 7.8 + 8.8 + 8.14). These are exactly what B2 wants — keep them.

## QA Complete
