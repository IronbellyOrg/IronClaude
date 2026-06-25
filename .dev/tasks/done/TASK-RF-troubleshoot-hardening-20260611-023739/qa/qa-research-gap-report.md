# QA Report — Research Gate (Gap Detection Lens)

**Topic:** MDTM tasklist for Pipeline Hardening Closure mode (H0-H5) for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Phase:** research-gate
**Lens:** gap-detection (adversarial)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

**Authoritative spec:** troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0, 653 lines)
**Research dir:** .dev/tasks/to-do/TASK-RF-troubleshoot-hardening-20260611-023739/research/
**Assigned files:** 01, 02, 03, 04, 05-v2, 06, 07 (all 7 .md in research/)

---

## Overall Verdict: FAIL

The research set contains a **version split**: files 05-v2 and 07 were researched against the
authoritative **v1.1.0** spec, but files **01, 02, 03, 04, and 06 were researched against an OLDER
draft** (5 refs / 8 contract fields / §6.2-§9 numbering / "no tests"). The builder-actionable
"how to build it" research (the file-by-file ref construction in 03, the SKILL.md edit map in 01,
the contract surfacing in 02, the MDTM/QA encoding in 04, and the test plan in 06) is therefore
**stale on the highest-value deliverables of v1.1.0**: the 6th ref (`hardening-output-contract.md`),
the 3 new contract fields (`contract_version`, `waiver_status`, `backtest_status`), the §4.7
executable-validation architecture, and — most seriously — the **17 unit/integration + 6 E2E test
suite (§8)**, which file 06 affirmatively says should NOT be built.

This is not a cosmetic numbering drift. A builder that consumes files 01/03/06 as written will
create 5 refs (not 6), omit `hardening-output-contract.md`, omit `contract_version`/`waiver_status`,
and skip the entire test suite that §4.7 makes the load-bearing anti-prose-pass mechanism. Per the
research-gate rule, **ALL gaps regardless of severity = FAIL**; here there are CRITICAL ones.

---

## Items Reviewed (per LENS focus question)

| # | LENS check | Result | Evidence |
|---|------------|--------|----------|
| 1 | Every NEW ref's REQUIRED CONTENT covered (esp. `hardening-output-contract.md` beyond a name)? | **FAIL** | File 03 (the per-ref content spec) covers only 5 refs and explicitly argues AGAINST a 6th (§4.6, lines 271-281). `hardening-output-contract.md` appears in only 2 files (05-v2 ×1 naming it absent; 07 ×3 quoting the spec's one-line purpose). NO file specifies its required content: the §5.4 truth table, the §5.5 field schema, the waiver-latch propagation contract, or the downstream-consumer obligations it must carry. Grep: `hardening-output-contract` → 01-04,06 = 0. |
| 2 | §4.7 executable-validation architecture covered (which test validates which artifact; tests assert against markdown contracts, not pass from prose)? | **PARTIAL→FAIL** | Covered faithfully in 07 §2.6 (the 6-component table verbatim) and flagged in 05-v2. But NO builder-actionable file translates it: file 06 — the dedicated test/verification research — concludes "**TESTING_REQUIREMENTS = NONE**" and "Do NOT add or modify any pytest test" (lines 112, 127-129), the exact OPPOSITE of §4.7. The "tests must assert against the markdown contract so they cannot pass from prose" requirement is nowhere operationalized against the real `tests/` layout. |
| 3 | §5.6 artifact schemas covered field-by-field for ALL of H0/H1/H2/H3/H4? | **PARTIAL** | All 5 schemas appear field-by-field in **exactly one file (07 §5)**. File 03 reproduces the H1/H2/H4 CARD field lists from the OLD spec line ranges (e.g. "spec lines 136-151", "spec lines 171-180") which do NOT match v1.1.0 (§5.6 is at spec L443-506). H0 boundary-scan schema and H3 sweep-card schema (`boundary_type`, `K_true`/`K_swept`, `intersection_proof`) appear ONLY in 07. Single-file coverage with stale line-anchors in the build-actionable file = fragile. |
| 4 | Downstream no-override rule (§5.4 L411 `success_with_hardening_blocker/advisory`) covered for remediation-handoff.md? | **PARTIAL** | The RULE is captured in 07 §3.2 (L411 verbatim ×2) and flagged in 05-v2 §D. But the file that owns remediation-handoff.md edits (file 03 §3) was written pre-v1.1.0: it wires `pipeline_hardening_verdict` but does NOT mention `waiver_status` carry, does NOT mention the `success_with_hardening_blocker`/`success_with_hardening_advisory` rendering tokens, and does NOT reconcile them against the "loaded only on success" gate. 05-v2 §D names the reconciliation need but gives no construction detail. |
| 5 | 6 §8.3 E2E backtest scenarios (E1-E5 + waiver re-green) covered so the builder can encode them? | **PARTIAL** | All 6 scenarios are extracted verbatim in 07 §9.3 + §9.5 (escape→test map). NO other file encodes them; file 06 (test research) omits them entirely because it concluded no tests are needed. The backtest scenarios live only in the spec-extraction file, with no bridge to "how to encode each as a `tests/troubleshoot/` E2E item." |
| 6 | Integration points (report-template → downstream consumers; SKILL.md trigger → Wave 5 report composition)? | **PASS (with stale risk)** | SKILL.md insertion seam covered well in 01 §1-§2 and 05-v2 §E (both pin the Wave 4.5 / pre-Wave-5 seam and the Wave 5 report-composition bullet). report-template → consumer threading covered in 03 §2 and 02 §3. These are structurally sound and largely version-independent (the skill on disk hasn't changed). Main residue: line-number anchors in 01/03 are pre-edit and the §4.7 "Required Consumers" column (SKILL.md/report-template/remediation-handoff/post-run handoffs) is not cross-walked. |
| 7 | G1-HALT + needs_human_decision (OI-2/3/5) handling covered? | **PASS** | Covered correctly and ONLY in 07 §11-§12: OI-2/OI-3/OI-5 are the OPEN `needs_human_decision` HALT items (07 explicitly CORRECTS the brief's framing — OI-1/4/6 are resolved in-spec), with the `feedback_human_decision_items_must_halt` memory cited, plus the G1-HALT "no src/ edits pre-approval" constraint. This is the strongest single-question coverage. Risk: it is single-file; if the builder reads 01-04 first and stops, it is missed. |

---

## Summary

- LENS checks passed: 2 / 7 (Q6 integration, Q7 G1-HALT)
- LENS checks PARTIAL: 4 / 7 (Q2, Q3, Q4, Q5 — covered in 07/05-v2 only, absent or stale in build-actionable files)
- LENS checks FAILED: 1 / 7 (Q1 — `hardening-output-contract.md` required content genuinely uncovered)
- CRITICAL gaps: 3
- IMPORTANT gaps: 4
- MINOR gaps: 2

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | **CRITICAL** | 03 §4 (all subsections) + 03 §4.6; 01 §5; 02 §2.2; 04 §1d | **Stale ref count (5 vs 6).** Files 01/02/03/04 are built on the OLD draft's "5 new refs / 8 fields" model. File 03 §4.6 (lines 271-281) explicitly RECOMMENDS NOT creating a 6th ref and argues the spec "already chose 5 files." v1.1.0 §4.1 lists **6** refs; the 6th, `hardening-output-contract.md`, is implementation-order step 2 (§4.6) and the home of the §5.4 truth table + §4.7 component 1. A builder following 03 will OMIT it. | Add a research note (or re-spawn a targeted researcher) specifying `hardening-output-contract.md` REQUIRED CONTENT: §5.4 7-row truth table + H5 decision-to-status + backtest-vs-verdict tables, §5.5 11-row field schema, waiver-latch propagation contract, downstream no-override obligations (`success_with_hardening_*`), and its house-style shape per 03 §1. Explicitly RETRACT 03 §4.6's "do not create a 6th ref" recommendation. |
| 2 | **CRITICAL** | 06 (entire file: "FINDING deliverable #3", lines 112, 127-129) | **"TESTING_REQUIREMENTS = NONE" directly contradicts §8 + §4.7 + file 05-v2.** File 06 concludes no pytest tests are needed and "Do NOT add or modify any pytest test." v1.1.0 §8 mandates **12 unit + 5 integration + 6 E2E** tests in `tests/troubleshoot/`, §4.7 makes executable validation architectural (tests assert against markdown contracts, cannot pass from prose), and 05-v2 §A Claim 4 + Summary says "CREATE dir + `__init__.py` + 7 test files." Two research files give the builder OPPOSITE instructions on the single largest deliverable. | Supersede file 06's TESTING_REQUIREMENTS conclusion with the §8 test inventory (07 §9 has the full FR→test/escape→test/NFR→test maps + the new FR-6 test `test_h2_sibling_sweep_required_when_concept_shared`). Reconcile the contradiction explicitly so the builder cannot follow 06. The validation-command sequence in 06 §"VALIDATION" (sync/verify-sync/markdownlint) is still valid and additive to — not a replacement for — the test suite. |
| 3 | **CRITICAL** | 02 §2.2; 03 §4.1; 01 §3 | **3 v1.1.0 contract fields missing from build-actionable research:** `contract_version`, `waiver_status`, `backtest_status`. Files 01/02/03 enumerate "8 new fields" (the old §6.2 set). v1.1.0 §5.5 has **11 rows / 10+ fields**, adding `contract_version` (semver, the whole point of FR-13 "versioned additive"), `waiver_status` (the SV-15 one-way latch — the core anti-theatre control), and `backtest_status` (NFR-1 coverage state). A builder using 02's "8 rows append cleanly after L61" will under-populate the Output Contract and miss FR-13/FR-12's load-bearing fields. | Update the contract-field research to the §5.5 11-row schema (07 §4 has it verbatim with types/defaults/nullability/missing-behavior). Ensure `waiver_status` latch semantics and `contract_version` are threaded into SKILL.md Output Contract, remediation-handoff BUILD_REQUEST, and the audit footer. |
| 4 | **IMPORTANT** | 03 §3; 02 §3.3 | **remediation-handoff.md §5.4 L411 wiring is pre-v1.1.0.** File 03 §3 wires only `pipeline_hardening_verdict` into the handoff; it omits `waiver_status` carry and the `success_with_hardening_blocker`/`success_with_hardening_advisory` rendering tokens (§4.2 says the file must "Carry hardening verdict + waiver latch into handoff"). 05-v2 §D flags the need but gives no construction. | Add construction detail for carrying `waiver_status` + verdict into the BUILD_REQUEST and rendering `success_with_hardening_*` (never plain `success`) when verdict ∈ {blocked, advisory}, reconciled with the "loaded only on success" gate. 07 §3.2 has the L411 rule verbatim as the source. |
| 5 | **IMPORTANT** | 06 (§4.7 translation absent); 05-v2 §F (test pattern) | **§4.7 test-to-artifact mapping not operationalized.** The 6-component "which test validates which artifact" table is extracted (07 §2.6) but no file maps it onto the actual `tests/troubleshoot/` files to be created, nor specifies HOW a markdown-contract assertion test is written (05-v2 §F gives the `tests/skills/` precedent — `REPO_ROOT = parents[2]`, assert on `src/` markdown — but does not apply it per-artifact). | Produce a per-test-file construction note: for each of the 7 test files, which markdown contract (which ref/section) it asserts against, using the 05-v2 §F `tests/skills/` content-assertion pattern. This is what prevents "tests pass from prose." |
| 6 | **IMPORTANT** | 04 §1d ("9 file operations = 4 edits + 5 new ref files"); 04 §6 | **MDTM granularity math is stale (9 ops, should be ~19 ref/edit/test items).** File 04 sizes the build at "4 edits + 5 new refs = 9 file operations" and asserts (§6) "no `uv run pytest` code-test item is required (markdown-only build)." With 6 refs + 7+1 test files, the operation count and the I18 testing-applicability both change materially — the build DOES create Python test files, so I18/test items DO apply. | Re-derive the granular item count: 6 new refs + 4 edits + `tests/troubleshoot/__init__.py` + 8 test files (7 from §8 + FR-6) = ~19 file-creating items, plus the test files trigger I18 (the build now creates source-adjacent test code). Update 04 §6's "I18 testing N/A" conclusion. |
| 7 | **IMPORTANT** | 03 §4.2-§4.5 (spec line-anchors) | **Stale spec line-anchors in the per-ref content spec.** File 03 cites "spec lines 136-151" (H1 card), "171-180" (H2 ledger), "241-253" (H4 card), "266-294" (H5) — these are OLD-draft line numbers. In v1.1.0 the schemas are §5.6 at spec L443-506 and H5/FR-11 at L214-223. A builder copying "verbatim from spec lines 136-151" will copy the wrong/nonexistent lines. | Re-anchor 03's per-ref "must contain" lists to v1.1.0 §5.6 / §3 FR line numbers (07 §5 has the correct ranges). |
| 8 | **MINOR** | 04 ("Deliverable file" footer, line 223) | **Cross-task contamination signal.** File 04's footer cites deliverable path `TASK-RF-troubleshoot-hardening-20260610-144537/...` — a DIFFERENT (prior) task dir than the current `20260611-023739`. Indicates file 04 (and likely 01/02/03/06, which share the old-spec framing) were carried over from an earlier run against the draft spec, not freshly researched against v1.1.0. | Confirm whether 01/02/03/04/06 are carry-overs; if so, they must be re-validated against v1.1.0 before the builder consumes them, not just the footer corrected. |
| 9 | **MINOR** | 01 §3 / §5 ("8 fields", "5 refs") | **Stale counts echoed in SKILL.md edit map.** File 01 §3 says append "8 new fields" and §5 says register "5 new refs." Otherwise-excellent structural map will under-edit the Output Contract table and the Refs registry by one ref + 3 fields. | Update 01's field count to 11 and ref count to 6 (add `hardening-output-contract.md` row to the Refs-registry edit at SKILL.md L546). |

---

## Cross-File Contradiction Register (must be surfaced, never silently resolved)

1. **Ref count:** 03/01/04/06 say **5 new refs**; 05-v2/07 say **6**. Authoritative spec §4.1 = **6**. → 05-v2/07 are correct; 03's §4.6 "do not create a 6th" is WRONG and must be retracted.
2. **Tests:** 06 says **NONE / do-not-add**; 05-v2 + 07 + spec §8/§4.7 say **17 unit+integration + 6 E2E, CREATE `tests/troubleshoot/`**. → 06 is WRONG (researched against the old §9 conditional).
3. **Contract fields:** 01/02/03 say **8**; 07/§5.5 say **11 rows (incl. `contract_version`, `waiver_status`, `backtest_status`)**. → 07 correct.
4. **Spec section numbering:** 01-04/06 cite §6.2/§9/§5.1-§5.2 (old); 05-v2/07 cite §4.1/§4.2/§5.4/§5.5/§5.6/§8 (v1.1.0). → 05-v2/07 correct.

A builder reading the files in numeric order (01→07) hits the stale guidance FIRST and the corrections LAST. The consolidation must explicitly rank 05-v2 and 07 as authoritative over 01/02/03/04/06 wherever they conflict, or the stale files must be re-run.

---

## Confidence Gate

**Step 1-4 computation:**

- TOTAL checklist items (7 LENS questions): 7
- VERIFIED (tool evidence — Read of spec + all 7 research files + targeted greps): 7
- UNVERIFIABLE: 0
- UNCHECKED: 0
- confidence = 7 / (7 − 0) × 100 = **100%**

Confidence ≥ 95% AND UNCHECKED = 0. The verdict is eligible; it is FAIL on the merits
(documented gaps + contradictions), not on insufficient verification.

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 3 (grep-based coverage probes across all 7 files)

Note: tool-call count ≥ checklist items (7); each Read targeted a specific in-scope file
(spec + 7 research files + this report), each Bash grep directly tested a specific coverage claim
(ref count, field count, test presence, schema fields, E2E scenarios, G1-HALT, stale paths).
No web research was performed (no external claim required verification).

---

## Recommendations (before this research feeds the builder)

1. **Re-run or hard-supersede files 01, 02, 03, 04, 06 against v1.1.0.** They are the build-actionable
   files and are stale on the decisive deliverables. The cheapest fix is a single corrective research
   note that (a) adds `hardening-output-contract.md` required content, (b) replaces 06's
   "tests=NONE" with the §8 inventory, (c) bumps field count to 11 and ref count to 6, (d) re-anchors
   03's spec line numbers. The more robust fix is re-spawning those researchers with v1.1.0 pinned.
2. **Mark 05-v2 and 07 authoritative** in the consolidation; on any 5-vs-6 / tests / field-count
   conflict, they win.
3. **Add the FR-6 new test** `test_h2_sibling_sweep_required_when_concept_shared` (07 §10 / G-PRE-1)
   and the FR-12↔NFR-4 pairing to the test inventory the builder consumes — these are present only in 07.
4. Do NOT let the builder proceed to A.9 until the ref count (6), the test suite (§8), and
   `hardening-output-contract.md`'s content are represented in build-actionable research, not just the
   spec-extraction file.

## QA Complete
