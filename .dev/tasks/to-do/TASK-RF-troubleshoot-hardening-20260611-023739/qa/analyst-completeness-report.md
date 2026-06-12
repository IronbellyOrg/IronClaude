# Research Completeness Verification (Breadth Lens)

**Track:** task-builder single track — Pipeline Hardening Closure mode
**Topic:** Build MDTM tasklist to implement waves H0-H5 + waiver/no-re-greening latch for sc:troubleshoot-protocol
**Authoritative spec:** troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)
**Date:** 2026-06-11
**Lens:** BREADTH — every area the builder needs has research coverage
**Files analyzed:** 7 (01-07)

---

## Verdict: FAIL — 1 CRITICAL + 4 IMPORTANT + 3 MINOR breadth gaps

The research collectively contains the material the builder needs, BUT a structural
spec-version split runs through it: files 01, 02, 03 (and parts of 04) are keyed to an
**older spec section layout** (§6.2 = 8-field contract, only 5 NEW refs, §7/§8/§9), while
files 05, 06, 07 are keyed to the **authoritative v1.1.0 layout** (§5.5 = 11-field contract,
6 NEW refs incl. `hardening-output-contract.md`, §4.1/§4.2/§5.4/§5.6/§5.7). The builder,
reading 01-04, would under-build the contract (miss `waiver_status`, `backtest_status`,
`contract_version`) and create only 5 of the 6 required NEW refs. File 07 alone is correct
and complete, but it does not override the structural-map files 01-03 the builder relies on
for insertion points. This must be reconciled before the build proceeds.

The enum CRITICAL-CHECK passed: **no file claims `advisory` was removed**, and no file uses
a 3-token enum in a State-Variable / output-contract verdict context. (Files 01 and 03 do
render `pass | blocked | advisory` in the REPORT.md display block — a 3-token nuance — but
that mirrors the spec's own §8 report block, not the canonical 4-token SV enum. Logged as a
MINOR consistency nit, NOT the CRITICAL the lens guards against.)

---

## Lens Criteria Scorecard

| # | Criterion | Result |
|---|-----------|--------|
| 1 | 6 NEW refs + 4 MODIFIED files (purpose, insertion point, conventions) | **FAIL** (6th ref + §4.2 spec-section keying) |
| 2 | All 13 FR acceptance criteria captured | **PASS** (file 07) |
| 3 | §5.4 truth table (7 rows) / §5.5 schema (11 fields) / §5.6 artifact schemas / §5.7 grammar | **PASS** (file 07); partial elsewhere |
| 4 | §8 test plan (12 unit + 5 integration + 6 E2E) + FR→test/escape→test maps + new FR-6 test + FR-12↔NFR-4 | **PASS** (file 07); CONTRADICTED by file 06 |
| 5 | needs_human_decision OI-2/OI-3/OI-5 captured (OI-1/4/6 not HALT) | **PASS** (file 07) |
| 6 | G1 HALT + sync/verify/markdownlint validation path | **PASS** (files 06, 07, 05) |
| C | Enum 4-token consistency (CRITICAL) | **PASS** (no "advisory removed"; MINOR display nit only) |

---

## Detailed Findings by Criterion

### Criterion 1 — 6 NEW + 4 MODIFIED files — FAIL

**6 NEW refs (spec §4.1):**

| Ref (spec §4.1) | Covered by | Status |
|---|---|---|
| `pipeline-hardening-closure.md` | 03 §4.1, 05 Claim 2, 07 §2.1 | COVERED |
| `runtime-entrypoint-verification.md` | 03 §4.2, 05 Claim 2, 07 §2.1 | COVERED |
| `contract-enumeration.md` | 03 §4.3, 05 Claim 2, 07 §2.1 | COVERED |
| `unmask-and-sweep.md` | 03 §4.4, 05 Claim 2, 07 §2.1 | COVERED |
| `effective-input-proof.md` | 03 §4.5, 05 Claim 2, 07 §2.1 | COVERED |
| `hardening-output-contract.md` | **05 Claim 2, 07 §2.1 ONLY** | **GAP in 01/02/03** |

The 6th ref `hardening-output-contract.md` (spec §4.1: "Field schema, verdict aggregation
truth table, waiver latch propagation contract, downstream consumer obligations") is
**absent from the structural/convention research the builder uses for ref construction**:

- **File 03** (the ref-conventions + per-ref build-recipe file) explicitly states "5 new refs
  exactly" (§4.6 heading, §6) and folds verdict-aggregation/truth-table content into
  `pipeline-hardening-closure.md` instead of a dedicated `hardening-output-contract.md`. Its
  §4.6 argues AGAINST a 6th ref. This contradicts spec §4.1 (6 refs), §4.6 build-order group 2
  ("`refs/hardening-output-contract.md` ... resolves OI-1/OI-6 before downstream wiring"), and
  §4.7 component 1 (verdict aggregation contract lives in `refs/hardening-output-contract.md`).
- **File 01** (SKILL.md structural map) lists "the 5 new refs" (§5, recommendation 12) — same
  undercount.
- **File 02** references "spec §9 ... 5 named new-ref filenames" — same older-layout keying.

**Impact:** Without correction the builder creates 5 refs and packs the verdict truth table
into the hub ref, diverging from the spec's §4.6 build order and §4.7 executable-validation
architecture (truth table + `test_hardening_verdict.py` pinned to `hardening-output-contract.md`).
Files 05 (Claim 2) and 07 (§2.1) DO list all 6 — the material exists, but the builder's primary
convention source (03) is wrong. This is the single most load-bearing breadth gap.

**4 MODIFIED files (spec §4.2):** all 4 covered with heading-anchored insertion points —
`commands/troubleshoot.md` (01 §136, 02 §1, 05 §B), `SKILL.md` (01 throughout, 05 §E),
`report-template.md` (01 §141, 03 §2, 05 §C), `remediation-handoff.md` (02 §3.3, 03 §3,
05 §D). COVERED.

---

### Criterion 2 — 13 FR acceptance criteria — PASS

File 07 §1 captures every FR-1..FR-13 with wave (H0–H5), escapes closed (E1–E5),
dependencies, and AC line numbers, plus the §3.1 traceability matrix verbatim. The new
FR-6 test gap (G-PRE-1) and FR-12↔NFR-4 pairing are explicitly flagged (07 §1 FR-6 note,
FR-12 note, §10, §9.6). Files 02/05 reference FRs by number where relevant. COVERED with
strong evidence (all AC cited to spec line numbers).

---

### Criterion 3 — §5.4 / §5.5 / §5.6 / §5.7 — PASS (file 07), partial elsewhere

- **§5.4 truth table (7 rows):** file 07 §3.1 reproduces all 7 rows verbatim, plus the 4-row
  H5 decision-to-status mapping (§3.2), 3-row backtest-vs-verdict (§3.3), and the downstream
  no-override rule (line 411). PASS.
- **§5.5 field schema:** file 07 §4 reproduces all 11 rows (10 distinct fields +
  `backtest_status`) verbatim. **CONTRAST:** files 01 §3 / 02 §2.2 / 03 §4.1 enumerate only
  **8 fields** (the older §6.2 set) and OMIT `contract_version`, `waiver_status`,
  `backtest_status`. File 05 (Claim D, §E) DOES surface `waiver_status` + `contract_version`.
  So the full 11-field schema is present (07) but the structural-map files undercount —
  builder must use 07/05's field list, not 01-03's.
- **§5.6 artifact schemas (H0–H4):** file 07 §5 reproduces all 5 (boundary scan, H1 card, H2
  ledger, H3 sweep card, H4 manifest) with every field + required flag. File 03 §4 gives the
  per-ref build recipe citing the same card line ranges. PASS.
- **§5.7 grammar:** file 07 §6 reproduces all 4 rules (small formal allow-list grammar, NOT
  CommonMark, NOT substring). File 03 §1.4 and file 05 reference it. PASS.

---

### Criterion 4 — §8 test plan + maps + new FR-6 test + FR-12↔NFR-4 — PASS (file 07), CONTRADICTED by file 06

- **12 unit + 5 integration + 6 E2E:** file 07 §9.1/§9.2/§9.3 reproduces all 23 tests
  verbatim with files and validations, plus FR→test (§9.4), escape→test (§9.5), NFR→test
  (§9.6) maps. PASS.
- **NEW test `test_h2_sibling_sweep_required_when_concept_shared` (FR-6/G-PRE-1):** file 07
  §10 specifies it (file `tests/troubleshoot/test_hardening_h2.py`, validates FR-6 AC1). PASS.
- **FR-12↔NFR-4 pairing:** file 07 §9.6 + §10 captures it explicitly. PASS.

**CONTRADICTION (flagged, not silently resolved):** File 06 §3 concludes
**"TESTING_REQUIREMENTS = NONE"** and recommends adding NO pytest tests — because no existing
test parses the troubleshoot skill metadata. File 07 §9 + spec §8 require **23 net-new tests**
(including the spec-mandated `tests/troubleshoot/` dir confirmed ABSENT by file 05 Claim 4).
These two research files give the builder directly opposing instructions on whether to author
tests. File 06's "NONE" is correct only about *pre-existing* tests breaking; it misreads spec
§8 (which *creates* the test suite) and the §10 sc:tasklist DoD ("Each task's DoD = its FR
acceptance criteria + the relevant unit test §8.1"). **The builder MUST follow 07/spec §8
(author the 23 tests + the new FR-6 test), NOT file 06's "NONE."** This contradiction must be
reconciled in the tasklist or the builder may omit the entire test suite.

---

### Criterion 5 — needs_human_decision OI-2/OI-3/OI-5 (OI-1/4/6 not HALT) — PASS

File 07 §11 correctly identifies **OI-2, OI-3, OI-5** as the OPEN/deferred `needs_human_decision`
HALT items (resolution target Roadmap M2 / G1) and explicitly CORRECTS the task-brief framing,
noting **OI-1, OI-4, OI-6 are RESOLVED in-spec** (§5.4 / §5.7) and must NOT be treated as HALT
items. It cites memory `feedback_human_decision_items_must_halt.md` (write PENDING + HALT, never
auto-default). PASS — this is the cleanest treatment in the set.

---

### Criterion 6 — G1 HALT + sync/verify/markdownlint validation path — PASS

- **G1 HALT:** file 07 §12 captures the implementation-halted-pending-G1 constraint (spec §1.2
  L42, §9 L586: no `src/superclaude/` or `.claude/` edits pre-approval); tasklist must encode
  the gate. File 05 Claim 5 + file 04 §6 reinforce.
- **Validation path:** file 06 §1/§2 + §VALIDATION and file 05 §F give the exact sequence:
  `make sync-dev` → `make verify-sync` (no ref-count assertion; src↔.claude byte-match) →
  markdownlint (MD025/MD040/MD041/MD047 on the in-scope `src/` markdown; `.dev/` excluded) →
  no `.claude/` staging (CLAUDE.md absolute rule, `block-claude-generated-mirrors` hook). File
  04 §6 encodes these as discrete `- [ ]` validation items. PASS.

---

### Criterion C (CRITICAL) — enum 4-token consistency — PASS

Checked every file for a verdict-context enum that drops `advisory` or claims its removal:

| File | Enum occurrences in verdict context | Verdict |
|---|---|---|
| 01 | L68/L138 `pass\|blocked\|advisory\|not_applicable` (SV/contract) ✓; L126 `pass\|blocked\|advisory` (proposed, in §6.2 prose) | OK (SV correct); MINOR nit at L126 |
| 02 | §2.2/§4 4-token incl. `not_applicable` | OK |
| 03 | §2.3 L142 `Closure verdict: pass \| blocked \| advisory` (REPORT.md display block) | MINOR display nit (3-token render) |
| 05 | L46/L76/L98 4-token; explicitly "advisory is MANDATED, do NOT drop it" | OK (strongest) |
| 06 | n/a (test/sync file) | OK |
| 07 | §3.0 4-token; explicitly "Any 'advisory removed' claim is FALSE" | OK (strongest) |

**No file claims advisory was removed. No file uses a 3-token enum for the canonical State
Variable / output-contract `pipeline_hardening_verdict`.** The two 3-token occurrences (01 L126,
03 §2.3) are in the REPORT.md *display* block, which mirrors the spec's own §8 report block
(the spec renders `Closure verdict: pass | blocked | advisory` in §8 while the SV/§5.4/§5.5
enum is 4-token). This is a spec-internal inconsistency the builder should normalize to 4-token
in the rendered report for safety, but it is **NOT** the CRITICAL the lens guards against.
**CRITICAL CHECK: PASS.**

---

## Compiled Gap List

### CRITICAL (blocks a faithful build)

- **C1 — 6th NEW ref `hardening-output-contract.md` missing from the builder's primary
  convention source.** Files 01, 02, 03 say "5 new refs" and fold the verdict truth table into
  `pipeline-hardening-closure.md`, contradicting spec §4.1 (6 refs), §4.6 group 2, and §4.7
  component 1. The ref IS listed in 05 (Claim 2) + 07 (§2.1), so the fix is to make the builder
  key off 07/05's file inventory, not 03's. Without this, the build produces 5 refs and a
  mis-located verdict contract. *(Sources: 03 §4.6/§6, 01 §5, 02 §1.4 vs 05 Claim 2, 07 §2.1.)*

### IMPORTANT (affect build quality / completeness)

- **I1 — Output-contract field undercount in structural-map files.** 01/02/03 enumerate 8
  fields and OMIT `contract_version`, `waiver_status`, `backtest_status`. The full 11-field
  §5.5 schema is only in 07 §4 (and partially 05). Builder must use 07's field list.
- **I2 — Direct test-requirement contradiction.** File 06 says "TESTING_REQUIREMENTS = NONE
  (add no tests)"; file 07 + spec §8 require 23 net-new tests + the new FR-6 test + the absent
  `tests/troubleshoot/` dir. Opposing instructions; builder must follow 07/spec §8.
- **I3 — Spec-section-layout drift across the file set.** 01/02/03/04 cite §6.2/§7/§8/§9
  (older layout); 05/06/07 cite §4.1/§4.2/§5.4/§5.5/§5.6/§5.7/§8 (v1.1.0). A builder cross-
  referencing the older-keyed files against the actual v1.1.0 spec will hit section-number
  mismatches. The substance is mostly equivalent, but the section anchors are stale in 01-04.
- **I4 — `backtest_status` / NFR-1 production-signoff semantics only in 07.** The run-verdict
  vs backtest-signoff distinction (§5.4 backtest table, §5.5 `backtest_status`) is captured
  only in file 07 (§3.3, §4) and absent from 01-03's contract treatment. Builder needs it to
  encode the integration test `test_backtest_status_keeps_pipeline_health_advisory_until_complete`.

### MINOR (should still be fixed)

- **M1 — 3-token enum in REPORT.md display block.** 01 L126 and 03 §2.3 render
  `pass | blocked | advisory` (no `not_applicable`) in the report-display context. Mirrors the
  spec's own §8 block but should be normalized to 4-token for safety. NOT the CRITICAL.
- **M2 — File 03 §4.6 actively argues against the 6th ref.** Beyond omitting it (C1), 03 gives
  a 4-point rationale for NOT creating `hardening-output-contract.md` (folding H5 + verdict into
  the hub). The builder must be told to disregard this argument in favor of spec §4.1.
- **M3 — SKILL.md insertion-seam naming varies (Wave 4.5 vs sub-wave vs Wave 5 pre-step).**
  Files 01 §5 and 05 §E offer 2-3 different insertion strategies. Not a gap (all are viable and
  heading-anchored), but the builder should pick one explicitly to avoid an under-specified item.

---

## Depth Assessment

**Expected depth (Deep tier, source→protocol transformation):** data-flow-level insertion
points, verbatim spec schemas, FR→test maps, convention extraction. **Achieved:** file 07 is
exemplary (full verbatim extraction, all maps, OI correction, enum guard). Files 05/06 are
solid and v1.1.0-aligned (cross-validation tags, sync mechanics, lint config). Files 01/03/04
are deep on SKILL.md structure / ref conventions / MDTM encoding but keyed to a stale spec
layout. **Missing depth element:** a single reconciled "canonical file/field inventory" the
builder can trust without having to detect which research files are v1.1.0-aligned.

---

## Recommendations (pre-build reconciliation)

1. **Pin the file/ref/field inventory to file 07 + file 05.** Instruct the builder to treat
   07's §2.1 (6 refs) and §4 (11 fields) as authoritative over 01/02/03's 5-ref / 8-field
   enumerations. (Closes C1, I1, I4.)
2. **Add `hardening-output-contract.md` as the 6th ref** with the verdict truth table + waiver
   latch + downstream-obligations content, per spec §4.6 group 2 / §4.7 component 1 — do NOT
   fold it into the hub ref as file 03 recommends. (Closes C1, M2.)
3. **Override file 06's "TESTING_REQUIREMENTS = NONE."** Encode the 23 net-new tests + the new
   `test_h2_sibling_sweep_required_when_concept_shared` + the `tests/troubleshoot/` dir creation
   per spec §8 / file 07 §9-§10. (Closes I2.)
4. **Re-anchor 01-04's spec-section citations to v1.1.0** (§4.1/§4.2/§5.4/§5.5/§5.6/§5.7) when
   the builder copies their insertion points, so it does not chase stale §6.2/§7/§8/§9 anchors.
   (Closes I3.)
5. **Normalize the REPORT.md verdict render to 4-token** `pass | blocked | advisory |
   not_applicable`. (Closes M1.)
6. **Carry forward the correct items file 07 already nailed:** OI-2/OI-3/OI-5 = HALT,
   OI-1/4/6 = resolved; G1-HALT gate; FR-12↔NFR-4 pairing; the 4-token enum guard.

---

## VERDICT: FAIL

**Breadth is materially complete in aggregate (every required area appears in at least one
file), but it is NOT builder-safe as-is:** the structural-map files the builder relies on
(01/02/03) are keyed to a stale spec layout, undercount the refs (5 vs 6) and the contract
fields (8 vs 11), and one file (06) gives a test instruction that directly contradicts the
spec. 1 CRITICAL + 4 IMPORTANT + 3 MINOR gaps. Reconcile per the 6 recommendations above —
chiefly by pinning the inventory to files 07 + 05 — before the rf-task-builder runs.

---
