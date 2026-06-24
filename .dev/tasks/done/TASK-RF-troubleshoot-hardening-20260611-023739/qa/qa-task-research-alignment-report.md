# QA Report — Task ↔ Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-11
**Stance:** ADVERSARIAL (assume builder dropped/misrepresented findings)

**Task file:** TASK-RF-troubleshoot-hardening-20260611-023739.md
**Authoritative spec:** troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)
**Authoritative research:** 08-v1.1.0-deliverable-reconciliation.md, 07-release-spec-structure.md, 05-doc-crossvalidation-spec-vs-code-v2.md
**Superseded (must NOT be inherited):** 01/02/03/04/06

---

## Method

Read in full: task file (511 lines, all 8 phases / 40+ checklist items), research 08
(RECON-1..7 + supersession summary), research 07 (FR-1..13, §3.1 matrix, §4.1/§4.5/§4.6/§4.7,
§5.4 7-row truth table, §5.5 11-field schema, §5.6 5 artifact schemas, §5.7 grammar, §8 test
plan, §11 OI items), research 05-v2 (code anchors + CODE-VERIFIED/CONTRADICTED tags). Verified
each authoritative finding maps to a checklist item; reverse-checked items for fabrication;
grep-confirmed counts and token leakage. Stance: adversarial (assume builder dropped findings).

---

## Checklist Results

### 1. All 6 refs from 08 RECON-1 (incl. the 6th, hardening-output-contract.md) — PASS

All six ref-authoring items are present, one per ref, matching 08 RECON-1 and 07 §4.1 exactly:

| RECON-1 ref | Task item | Status |
|---|---|---|
| pipeline-hardening-closure.md | Step 2.1 | PRESENT |
| hardening-output-contract.md (THE 6th) | Step 2.2 | PRESENT — explicitly flagged "the file a prior build got wrong" |
| runtime-entrypoint-verification.md | Step 3.1 | PRESENT |
| contract-enumeration.md | Step 3.2 | PRESENT |
| effective-input-proof.md | Step 3.3 | PRESENT |
| unmask-and-sweep.md | Step 4.1 | PRESENT |

The stale-03 "5 refs / argue against a 6th" conclusion was NOT inherited. §4.6 group ordering
(group 1 = closure skeleton, group 2 = output-contract before downstream wiring, group 3 = 3
parallel refs H1/H2/H4, group 4 = H3 after group 3) is faithfully reproduced in Phases 2/3/4.

### 2. All 10+1 contract fields from 08 RECON-2 — PASS

Step 2.2 (author hardening-output-contract.md) AND Step 5.2 (wire into SKILL.md Output Contract)
both enumerate the full additive field set verbatim, including the three fields stale research
omitted: `contract_version` (semver default 1.0.0), `waiver_status` (none|latched), and
`backtest_status` (not_run|partial|complete). The 4-token `pipeline_hardening_verdict` enum
(`pass|blocked|advisory|not_applicable`), `off_path_review_decision`, the 4 path fields, and
`known_escapes_caught` are all present with correct types/defaults matching 07 §5.5 (L427-439).
grep: contract_version ×7, backtest_status ×6, success_with_hardening ×9 across the task.
NFR-6 backward-compat (`test_output_contract_backward_compat`) wired at Step 7.10.

### 3. All 18 tests + 6 E2E incl. NEW FR-6 test + FR-12↔NFR-4 pairing + dir creation — PASS

- `tests/troubleshoot/` dir + `__init__.py` creation: Step 7.1 (PRESENT; cites CODE-CONTRADICTED
  absence from 05-v2 and the `parents[2]` / `tests/skills/` content-assertion pattern).
- 13 unit tests across Steps 7.2-7.7 (H0×2, H1×1, H2×2 incl. new, H3×3, verdict×3) +
  the NEW `test_h2_sibling_sweep_required_when_concept_shared` (Step 7.4, explicitly tagged
  G-PRE-1 / FR-6, closing the indirect-coverage gap from 07 §10).
- 5 integration tests across Steps 7.8-7.12, including
  `test_downstream_success_cannot_override_latched_hardening_verdict` (Step 7.9, explicitly the
  FR-12↔NFR-4 pairing, citing §10 L596 "highest-risk task").
- 6 E2E backtest scenarios (E1-E5 + Waiver re-green) in Steps 7.13-7.18, written to
  `e2e-backtest-scenarios.md`.
- Module set pinned to EXACTLY 7 (overview L67, Step 7.12, Step 8.13) — matches 08 RECON-3 / 07 §8.

Counts reconcile: 13 unit + 5 integration = 18 (matches 08 "18 unit/integration"); +6 E2E.

### 4. §5.4 truth table / §5.5 schema / §5.6 artifact schemas / §5.7 grammar reflected — PASS

- §5.4 7-row truth table with advisory rows 5/6: Step 2.2 (author), Step 7.8
  (`test_verdict_aggregation_from_h_statuses` asserts all 7 rows incl. BOTH advisory rows),
  Step 8.8 (domain lens), Step 8.15 (reflect). Report-language strings reproduced verbatim.
- §5.5 schema: Steps 2.2 + 5.2 (covered in #2 above).
- §5.6 artifact schemas: H0 6 fields (Step 2.1 + 7.2), H1 11 fields (Step 3.1 + 7.3), H2 6 fields
  (Step 3.2 + 7.4), H3 10 fields (Step 4.1 + 7.6), H4 8 field-groups (Step 3.3 + 7.5). Each
  authoring item reproduces the exact field names from 07 §5.6.
- §5.7 grammar (4 rules, small formal allow-list, NOT CommonMark / NOT substring): Step 4.1
  (author) + Step 7.6 (`test_h3_small_grammar_rejects_setext_and_decorated_verdicts`).

### 5. remediation-handoff item carries hardening fields (08 RECON-4) — PASS (with one note, see Gap G2)

Step 6.2 adds `pipeline_hardening_verdict` + `waiver_status` to the BUILD_REQUEST, surfaces the
latched blocker in the user-offer, and reconciles the line-3 "loaded only on success" gate with
the `success_with_hardening_blocker`/`success_with_hardening_advisory` rendering. This matches
RECON-4. RECON-4 also mentions `success_with_hardening_*` — see G2 below for scope note.

### 6. Heading-text anchoring + v1.1.0 §-numbers (no draft §6.2/§7/§9 leakage) — PASS

- Discovery Steps 1.3/1.4 capture anchors by HEADING TEXT; wiring Steps 5.1/5.2/6.1/6.2 all
  instruct "anchor on HEADING TEXT, NOT line numbers." Matches 05-v2 anchor caution.
- grep for draft §6.2/§7/§9: the only §9 hits are legitimate references to the v1.1.0 spec's
  §9 Migration/Rollout section (which exists at spec L582-586) and the explicit discipline note
  (L135) WARNING against draft §6.2/§7/§9. No item uses draft section numbers as if authoritative.
  Section-number discipline (use §3/§4/§5/§8) is stated as a Key Constraint (L135).

### 7. OI-2/3/5 HALT items grounded in §11; OI-1/4/6 NOT HALT — PASS

Steps 1.5/1.6/1.7 author OI-2/OI-3/OI-5 as `needs_human_decision` PENDING+HALT markers, each
citing spec §11 and the project rule (write PENDING, halt dependent mutation, never auto-default).
Each downstream-dependent item references its marker (Step 3.2→OI-2, Step 3.1→OI-3, Step 2.2→OI-5
contract_version-vs-target_release distinction). Key Constraint L134 + overview correctly state
OI-1/OI-4/OI-6 are RESOLVED in-spec (§5.4/§5.7) and NOT HALT items — matching 07 §11's explicit
correction to the original task-brief framing. The G1 gate is correctly classified as a
PREREQUISITE, not a needs_human_decision item (Step 1.1, L88).

### 8. FABRICATION CHECK — PASS (no fabricated files/fields/tests/sections found)

Every file path, field name, test name, and §-anchor in the task traces to the spec or
authoritative research. Spot-checked: all test names match 07 §8.1/§8.2 verbatim; all 6 ref
filenames match §4.1; all schema field names match §5.6; the `success_with_hardening_*` tokens
trace to §5.4 L411; E2E scenarios trace to §8.3. No invented artifacts detected.

### 9. ADVISORY enum (4-token, no silent 3-token) — PASS

Every verdict-touching item references the 4-token enum with `advisory` REQUIRED. The overview
(L71), Key Constraint (L130), Steps 2.2/5.2/6.1/6.2/7.7/7.8, the Step 8.8 domain lens, and the
Step 8.15 reflect literal-enum check form triple+ coverage against the prior 3-token regression.
No item silently uses a 3-token enum. This is the strongest-guarded invariant in the task.

---

## Adversarial Gaps Found

Per the adversarial mandate (find ≥3), the following are genuine alignment gaps/risks. None rise
to CRITICAL — the task faithfully carries the authoritative inventory — but each is a real
deviation a careful reviewer should weigh.

### G1 — LOW/MINOR: §4.5 "15-variable" registry count never reproduced as an explicit assertion

07 §4.5 (and the registry table) pins **15 state variables** including the 6 `h0..h5_status`
vars and the 4 path vars counted individually. The task authors all the FIELDS (Step 5.2) and the
verdict/latch invariants (Step 2.2), but no item asks the builder to reproduce or assert the
"15 variables" registry total, nor to author the `h0..h5_status` enum (`PASS|FAIL|N/A`, with
"N/A only with recorded rationale; FAIL sticky") as a first-class registry artifact. The h-statuses
are referenced implicitly (truth table inputs, phase-contract YAML), but the §4.5 invariants
"set-once `pipeline_hardening_applicable`" and "FAIL is sticky" for h-statuses are not pinned to a
test the way the waiver latch is. Impact: low — the behavior is covered indirectly via the truth
table tests — but the §4.5 registry as a discrete deliverable is under-anchored vs. 07's emphasis.
Recommendation: add to Step 2.2 (or 2.1) an explicit instruction to reproduce the §4.5 state
registry incl. the `h0..h5_status` enum + set-once/sticky invariants, OR note it is intentionally
folded into the truth-table coverage.

### G2 — LOW/MINOR: `success_with_hardening_*` is a rendered downstream STATUS but is not represented in any output-contract FIELD enum

The task correctly carries the §5.4 L411 rule that downstream renders
`success_with_hardening_blocker`/`success_with_hardening_advisory` (Steps 2.2, 6.2, 7.9). However,
neither 07 §5.5 nor the task defines WHERE this rendered token lives — it is a downstream success
enum value (task-builder/reflect/adversarial), not a troubleshoot output-contract field. This is
faithful to the spec (the spec also leaves it as a rendering rule, not a field), so it is NOT a
fabrication or a drop. The residual risk is only that
`test_downstream_success_cannot_override_latched_hardening_verdict` (Step 7.9) must assert the
TOKENS appear in the markdown RULE TEXT (the only verifiable surface at this stage; the actual
downstream enum lives in other skills, out of scope). The item's wording ("asserts the
`success_with_hardening_*` tokens AND the no-override rule are present") is correctly scoped to
rule-text presence. Flagging for visibility; no change strictly required.

### G3 — LOW/MINOR: §3.1 escape→FR matrix not authored as a consolidated traceability artifact; only embedded per-item

07 §1.1 reproduces the §3.1 Escape/Wave/Evidence/Backtest traceability matrix verbatim (E1-E5 →
waves → FRs → cards → backtest). The task threads this mapping through individual items
(E1→Step 3.1/3.2, E4→Step 7.16, etc.) and Step 8.7 (cross-ref chain QA traces it), but no
authoring item asks the builder to reproduce the §3.1 matrix itself inside `pipeline-hardening-closure.md`
or `hardening-output-contract.md`. 08 RECON-1 row 1 lists "verdict-aggregation pointer" and the
H0 schema for the closure ref but not the escape matrix. Impact: low — the QA chain (Step 8.7)
will catch a broken link — but the single consolidated traceability surface that 07 §1.1
emphasizes is not a named deliverable. Recommendation: consider adding the §3.1 matrix to the
closure ref, or confirm it is intentionally deferred to the E2E scenarios file (which covers the
backtest column only).

### G4 — INFORMATIONAL: NFR-2 / NFR-3 explicitly deferred (correctly), but no guard asserts the deferral boundary

The task correctly scopes NFR-2 (applicability false-positive rate) and NFR-3 (added cost) OUT to
backtest milestone M5 (L96, L450). 07 §6 lists both. This is a correct scoping decision matching
07 §13 (M5 deferred), not a gap — noting only that the task relies on prose ("deferred to M5")
rather than any guard. No action needed; recorded for completeness.

---

## Inherited-Staleness Check (files 01/02/03/04/06 SUPERSEDED banners)

Confirmed the task did NOT inherit any of the five stale design conclusions:

| Stale claim | Source | Task state |
|---|---|---|
| "5 refs / argue against a 6th" | 03 | REJECTED — 6 ref items present (Step 2.2 is the 6th) |
| "8-field output contract" | 01,02 | REJECTED — 10+1 fields incl. contract_version/waiver_status/backtest_status |
| "TESTING_REQUIREMENTS = NONE" | 06 | REJECTED — 18 unit/int + 6 E2E + tests/troubleshoot/ creation |
| draft §6.2/§7/§9 anchors | 01-04 | REJECTED — v1.1.0 §3/§4/§5/§8 used; L135 warns against draft anchors |
| "advisory removed" / 3-token enum | (prior build) | REJECTED — 4-token enum triple-guarded |

The task explicitly cites the SUPERSEDED-banner files as "anchors ONLY" (L109, L120, R-005) and
routes design conclusions to 07/08/05-v2. This is exactly the RECON-0 read-order discipline.

---

## VERDICT: PASS

All 9 research-alignment checklist items PASS. Every significant finding in the authoritative
research (08 RECON-1..7, 07 §3-§11, 05-v2 code anchors) has a corresponding checklist item; no
task item fabricates actions ungrounded in research/spec; and none of the five stale design
conclusions from the SUPERSEDED files (01/02/03/04/06) were inherited.

The four adversarial gaps found (G1-G4) are all LOW/MINOR or INFORMATIONAL — they are
under-anchoring / scoping-clarity observations, not dropped findings or fabrications. They do not
block the task. The dominant invariant (4-token advisory enum + §5.4 rows 5/6) is the most
heavily guarded element in the entire tasklist.

**Severity-rated gaps:**
- G1 (LOW): §4.5 15-var registry + h0..h5_status enum not reproduced as a discrete deliverable.
- G2 (LOW): `success_with_hardening_*` correctly scoped as rule-text, not a field — note only.
- G3 (LOW): §3.1 escape→FR matrix embedded per-item, not authored as one consolidated artifact.
- G4 (INFO): NFR-2/NFR-3 deferral is prose-only (correctly deferred to M5).

Recommendation: PASS as-is. Optionally fold G1 (state-registry reproduction) into Step 2.1/2.2 and
G3 (§3.1 matrix) into the closure ref for completeness, but neither is required for spec fidelity.

---
