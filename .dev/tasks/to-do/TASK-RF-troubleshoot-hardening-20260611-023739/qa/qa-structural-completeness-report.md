# QA Report — Structural Completeness (FINAL_ONLY gate)

**Topic:** v1.1.0 troubleshoot-pipeline-hardening deliverable set completeness
**Date:** 2026-06-11
**Phase:** report-validation / structural-completeness
**Fix cycle:** N/A (fix_authorization: false — REPORT ONLY)
**Stance:** ADVERSARIAL. Assume >=10 completeness gaps exist; find them.

---

## Overall Verdict: FAIL

Physical deliverable SET is COMPLETE (15/15 checks PASS — all 6 refs, 4 mods, 11 fields,
18/18 tests incl. the 2 named tests, 6 E2E scenarios present and passing). FAIL is driven by
**11 document-level completeness/consistency gaps (G1–G11)** in the two QA-input documents
under review (research 08 + the inventory), 2 of them IMPORTANT (count drift in the
AUTHORITATIVE research file). Per the binary gate rule (FAIL on any issue of any severity).

---

## Scope verified

Deliverable set per QA input inventory (Step 8.1) cross-checked against authoritative
research `08-v1.1.0-deliverable-reconciliation.md` (6 refs / 10+1 fields / 18 tests / 6 E2E).

## Items Reviewed (physical deliverables — all VERIFIED PRESENT)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | All 6 new refs exist | PASS | `ls refs/` + `git status` shows all 6 as `A`: pipeline-hardening-closure, hardening-output-contract, runtime-entrypoint-verification, contract-enumeration, unmask-and-sweep, effective-input-proof |
| 2 | All 4 modified files modified | PASS | `git status --porcelain` shows `M` for SKILL.md, commands/troubleshoot.md, report-template.md, remediation-handoff.md |
| 3 | `tests/troubleshoot/__init__.py` present | PASS | `ls` + Read: package marker w/ convention note (parents[2], tests/skills/ pattern) |
| 4 | 7 test modules present | PASS | h0,h1,h2,h3,h4,verdict,output_contract all on disk |
| 5 | `e2e-backtest-scenarios.md` present | PASS | Read: 6 scenarios E1–E5 + Waiver re-green |
| 6 | pytest collects 18 tests | PASS | `uv run pytest --collect-only -q` = "18 tests collected" |
| 7 | 18/18 tests PASS | PASS | `uv run pytest -q` = "18 passed in 0.03s" |
| 8 | 13 unit + 5 integration split | PASS | h0:2u h1:1u h2:2u h3:3u h4:2u verdict:3u = 13 unit; verdict:2int output_contract:3int = 5 int |
| 9 | NEW `test_h2_sibling_sweep_required_when_concept_shared` | PASS | Present in test_hardening_h2.py:36, collected, passes (FR-6 / G-PRE-1) |
| 10 | Paired `test_downstream_success_cannot_override_latched_hardening_verdict` | PASS | Present in test_hardening_verdict.py:76, collected, passes (FR-12↔NFR-4) |
| 11 | All §8.1/§8.2 test-function names match exactly | PASS | All 18 collected names byte-match the §8 names in research 08 RECON-3 tables |
| 12 | 11 hardening fields in SKILL.md | PASS | grep-counted all 11 field backticks present (incl. contract_version, waiver_status, backtest_status) |
| 13 | 19 legacy Output Contract fields preserved | PASS | test_output_contract_backward_compat asserts all 19 LEGACY_FIELDS + 11 HARDENING_FIELDS; passes |
| 14 | NFR-5: no new CLI flag in troubleshoot.md | PASS | grep for `--harden`/`--closure` flag = none found |
| 15 | All 6 E2E scenarios documented | PASS | E1 (H1), E2 (H3), E3 (H3 sweep), E4 (H2 ledger), E5 (H4 fail-closed), Waiver re-green — all in e2e-backtest-scenarios.md |

**Physical deliverable set: COMPLETE.** Every ref, field, test, and scenario the task
asked me to confirm is present, collected, and passing. No missing physical artifact.

## Document-Level Completeness Gaps (the QA inputs under review)

The task scope places the **QA input inventory** and **authoritative research 08** themselves
under review. Adversarial audit of those documents surfaced internal inconsistencies and
omissions. Per the gate rule (FAIL on any issue of any severity), these are reported below.

### Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| G1 | IMPORTANT | research 08 L129 (SUPERSESSION SUMMARY) | Stale test count: row reads "**17 unit/integration** + 6 E2E + new FR-6 test" — contradicts RECON-3 (L49/L51) and the as-built suite which are **18** (13 unit + 5 integration). The "17" is the pre-G-PRE-1 number; the FR-6 test that makes it 18 is mentioned in the same cell but the total was not updated. | Change "17 unit/integration" → "18 unit/integration (13 unit + 5 integration)" so the summary row matches RECON-3 and the collected suite. |
| G2 | IMPORTANT | research 08 — RECON-1 L21 + RECON-5 L105 vs RECON-2 header L29 + inventory L13 | Internal contradiction on the §5.5 field count. RECON-1 row 2 and RECON-5 both state "§5.5 field schema (**10 fields**)"; RECON-2's header (L29) says "**ELEVEN**-field output contract"; the as-built ref `hardening-output-contract.md` §5.5 table contains **11 rows** (`backtest_status` is folded INTO the §5.5 table, not separate). The "§5.5 = 10 fields" phrasings undercount the as-built schema. | Reconcile to a single number: §5.5 schema = 11 fields (as built). Update RECON-1 row 2 and RECON-5 to "§5.5 field schema (11 fields)" OR add an explicit "10 result + backtest_status = 11 in the §5.5 table" note at each site. |
| G3 | MINOR | research 08 RECON-2 body L31 | Self-inconsistent wording within RECON-2: header says "ELEVEN-field … (NOT eight)" but the body sentence says "The authoritative additive field set is **10 result fields** (plus backtest_status = the 11th)". Reader cannot tell whether the canonical count is 10 or 11 without inferring. Compounds G2. | Rephrase body to lead with "11 fields total" then break down "(10 result fields + backtest_status)". |
| G4 | MINOR | inventory L44 | Totals line says "**20 deliverables**" = 6 refs + 4 mods + 9 test-dir files. The 9 test-dir files include `e2e-backtest-scenarios.md`, which the same line (L40) flags as "not pytest-collected (M5)" — i.e. a documentation artifact, not a test module. Counting it as a "test-dir file" is fine, but the headline "20 deliverables" silently bundles a doc-scenario file with executable code; no breakdown distinguishes the 18 executable tests' home (7 modules) from the 1 doc + 1 `__init__`. Not wrong, but under-specified for a completeness inventory. | Add a one-line sub-breakdown: "9 test-dir files = 7 pytest modules + `__init__.py` + 1 documented-scenarios md". (Already partially present in parens; promote to explicit count.) |
| G5 | MINOR | inventory L45 vs research 08 L51 | The inventory correctly states "13 unit + 5 integration = 18", but research 08's own §8.1 heading (L57) reads "§8.1 Unit tests (**12**) + the G-PRE-1 addition (13th)" while the SUPERSESSION row (L129, see G1) still says 17. Three different running totals (12/13 unit; 17/18 total) appear across research 08. The inventory is internally consistent; research 08 is not, and it is the AUTHORITATIVE source feeding the inventory. | Normalize all running totals in research 08 to "13 unit / 5 integration / 18 total" (the as-built reality). |
| G6 | MINOR | inventory L12 vs research 08 RECON-1 L20 | H0 boundary-scan schema field count: inventory L12 says "6-field boundary-scan schema (9-value boundary_type enum)"; research 08 RECON-1 row 1 (L20) says "H0 boundary-scan schema (§5.6 H0 row, 6 fields)" — these agree on 6 fields, but the "9-value boundary_type enum" detail appears ONLY in the inventory and is NOT stated or sourced anywhere in research 08. An enum-cardinality claim with no upstream authority is an unverifiable inventory assertion. | Either add the 9-value boundary_type enum to research 08's H0 description with a spec §5.6 anchor, or drop the unsourced "9-value" qualifier from the inventory. |
| G7 | MINOR | research 08 RECON-3 §4.7 map L86-92 | The §4.7 "component→test map" lists 6 components but omits an explicit mapping for FR-6 (sibling sweep / `test_h2_sibling_sweep_required_when_concept_shared`) and for the H1 negative+positive witness beyond folding them under "H2 tests"/"H0 tests" generically. The NEW G-PRE-1 test (the headline addition of this whole reconciliation) has no dedicated row in the executable-validation map. | Add a §4.7 row binding FR-6 → `test_h2_sibling_sweep_required_when_concept_shared` so the map is complete for the 13-test suite. |
| G8 | MINOR | inventory L40 + research 08 L5/L83 (E2E scenario semantics) | Both docs call the E2E set "6 documented E2E backtests (E1–E5 + Waiver re-green)". The as-built `e2e-backtest-scenarios.md` maps E2 to "FR-7 + FR-8" and E3 to "FR-7 + FR-8 + FR-9", but research 08 §8.3 (L84) describes E2 only as "complete/incomplete near-miss → H3" and E3 as "Task-Log/Findings sibling headings → H3 sweep" with NO FR tags. The FR-coverage mapping in the built scenarios is RICHER than what either upstream doc specifies, so neither doc lets a reviewer confirm the built FR-mapping is correct/complete. | Add the per-scenario FR-coverage tags to research 08 §8.3 (or the inventory) so the E2E FR mapping is traceable upstream, not invented at build time. |
| G9 | MINOR | research 08 RECON-1 L22 ("negative-witness rule (FR-4)") vs inventory L14 + as-built | research 08 row 3 specifies H1 ref content as "negative-witness rule (FR-4)" only; the inventory L14 and the as-built test `test_h1_runtime_card_requires_negative_and_positive_witness` (FR-3/FR-4) require BOTH a negative AND a positive witness. Research 08's H1 ref spec omits the positive-witness requirement that the built test enforces — an upstream under-specification of the ref's required content. | Update research 08 RECON-1 row 3 to "negative + positive witness rule (FR-3/FR-4)" to match the built contract. |
| G10 | MINOR | research 08 L131 (MDTM op-count) | SUPERSESSION row says recompute "for 6 refs + 4 mods + **13 tests** + wiring (~19+ ops)". "13 tests" counts only unit tests and silently drops the 5 integration tests (and the e2e doc) from the op math, while the authoritative suite is 18 + e2e. The op-count basis is therefore stated against a stale denominator. | Restate the op basis as "6 refs + 4 mods + 18 tests + e2e doc + wiring" for a consistent denominator. |
| G11 | MINOR | inventory L46 / L47 | Inventory asserts "All 9 src skill markdown files markdownlint-clean" and "pytest 18/18 PASS" as completeness facts, but provides no per-file enumeration of which 9 markdown files were linted. A completeness inventory that asserts a lint-clean count without listing the 9 files cannot be independently confirmed from the inventory alone (a reviewer must reconstruct the set: 6 new refs + 3 of the 4 modified that live under skills/ — note commands/troubleshoot.md is the 4th modified but lives under commands/, so "9 skill md" excludes it; this is correct but unstated). | List the 9 markdown files (or note "6 new refs + report-template + remediation-handoff + SKILL.md = 9; commands/troubleshoot.md linted separately") so the "9" is auditable. |

### Note on physical completeness vs. document completeness

To be explicit: **every physical deliverable the task enumerated is present, collected, and
passing** (Items Reviewed 1–15 above, all PASS). The 11 gaps G1–G11 are **completeness/consistency
defects in the two QA-input DOCUMENTS** (research 08 and the inventory), not missing code. They
matter because research 08 is the AUTHORITATIVE source-of-truth feeding the inventory and any
future maintainer: its running totals disagree (17 vs 18 total; 10 vs 11 fields; 12 vs 13 unit),
and several as-built contract details (positive witness, FR-6→test binding, per-E2E FR tags,
9-value boundary enum) are richer in the build than in the upstream that allegedly governs it.
A "FINAL_ONLY" gate that blesses these documents as complete would propagate the count drift.

## Summary

- Physical-deliverable checks passed: 15 / 15
- Document-completeness gaps found: 11 (G1–G11)
- Severity: IMPORTANT 2 (G1, G2), MINOR 9
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — REPORT ONLY)

**Confidence:** Verified: 15/15 physical + 11/11 document-gap findings tool-evidenced |
Unverifiable: 0 | Unchecked: 0 | Confidence: 100% (physical set); document gaps each
cited to specific line numbers in the two source docs.

**Tool engagement:** Read: 7 | Grep/Bash-grep: 8 | Glob(ls): 2 | Bash(pytest/git/make): 5

## Recommendations

- This is a binary completeness gate. The physical deliverable SET is complete (no missing ref,
  field, test, or scenario). However, the two QA-input documents under review carry 11 internal
  consistency/completeness defects, 2 of them IMPORTANT (count drift in the AUTHORITATIVE research
  file). Per the gate rule "FAIL if any issue of any severity," the verdict is **FAIL**.
- Highest-priority fixes before re-gate: **G1** (research 08 L129 "17"→"18") and **G2** (reconcile
  §5.5 "10 vs 11 field" across RECON-1/RECON-2/RECON-5 to the as-built 11). These two remove the
  primary count-drift in the source-of-truth file.
- If the reviewing authority scopes this gate to PHYSICAL deliverables only (ignoring document
  internal-consistency), the physical set is PASS — but that scoping should be stated explicitly,
  because the task instruction "Assume these documents have at least 10 COMPLETENESS gaps. Find
  them." directs the audit at the documents, and 11 were found.

## QA Complete

VERDICT: FAIL
