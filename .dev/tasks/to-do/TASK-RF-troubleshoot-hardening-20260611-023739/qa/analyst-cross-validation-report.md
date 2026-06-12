# Cross-Validation Completeness Report

**Analysis type:** completeness-verification (lens: cross-validation)
**Topic:** Pipeline Hardening Closure mode (H0-H5) tasklist for sc:troubleshoot-protocol
**Date:** 2026-06-11
**Authoritative spec:** troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)
**Files analyzed:** 01, 02, 03, 04, 05-v2, 06, 07

---

## Files in scope

| File | Date | Origin | Status | Role |
|------|------|--------|--------|------|
| 01-skill-structure-inventory.md | 2026-06-10 | carried-over | Complete | SKILL.md structural map + insertion points |
| 02-command-and-contract-integration.md | 2026-06-10 | carried-over | Complete | command + output-contract integration |
| 03-refs-conventions-and-report-template.md | 2026-06-10 | carried-over | Complete | refs house style + report-template/handoff |
| 04-mdtm-template-and-examples.md | 2026-06-10 | carried-over | Complete | MDTM template house style (not spec-content) |
| 05-doc-crossvalidation-spec-vs-code-v2.md | 2026-06-11 | FRESH | Complete | code crossval vs RELEASE-SPEC |
| 06-sync-verify-and-tests.md | 2026-06-10 | carried-over | Complete | Makefile/lint/tests verification surface |
| 07-release-spec-structure.md | 2026-06-11 | FRESH | Complete | authoritative spec extraction (v1.1.0) |

NOTE: file 04 is MDTM-template house style, not spec-content; not material to lenses 1-5.

---

## Lens 1 — Verdict enum + field names + insertion points + report-template `Closure verdict` enum

### 1a. Verdict enum tokens — CONSISTENT across all files (no contradiction)

The 4-token enum `pass | blocked | advisory | not_applicable` is authoritative from 07 (§4.5 L311, §5.4 rows 5-6, §5.5 L431).

| File | Enum as written | advisory present? | Verdict |
|------|-----------------|-------------------|---------|
| 07 (spec) | `pass\|blocked\|advisory\|not_applicable` (4-token, 7-row table, rows 5+6 = advisory) | YES | AUTHORITATIVE |
| 05-v2 | `pass\|blocked\|advisory\|not_applicable`; "advisory is MANDATED ... do NOT drop it" | YES | AGREES |
| 01 | `pass\|blocked\|advisory` (§6 L126); recipe L138 maps to 4-token form | YES | AGREES* |
| 02 | `pass`/`blocked`/`advisory`/`not_applicable` (§4 L194) | YES | AGREES |
| 03 | report block `Closure verdict: pass \| blocked \| advisory` (L142) | YES | AGREES* |

*Carried-over 01 and 03 write the 3-token shorthand `pass | blocked | advisory` in their illustrative blocks (omit `not_applicable`). NOT a contradiction — `advisory` is present in both; `not_applicable` is the skip sentinel handled via section omission (03 L131 already specifies omit-when-not-applicable). Builder must encode the FULL 4-token enum; expand 03's L142 illustrative block to 4-token. Flagged MINOR.

### 1b. Field names / paths — CONSISTENT

The 4 path fields `runtime_entrypoint_card_path / contract_ledger_path / unmask_sweep_path / effective_input_card_path` appear identically in 07 (§4.5,§5.5), 05-v2 (§E), 01 (§3), 02 (§2.2/§4). `off_path_review_decision`, `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, `waiver_status`, `known_escapes_caught`, `contract_version`, `backtest_status` consistent. No field-name divergence.

### 1c. Field COUNT discrepancy — IMPORTANT FLAG

- 07 §5.5 = **10 distinct fields (11 rows)**; §4.5 = **15 state variables** (incl. `waiver_status`, `backtest_status`, `contract_version`, `h0..h5_status`).
- 01 (§3) + 02 (§2.2,§4) describe **"8 new fields"** to append: `pipeline_hardening_applicable`, `pipeline_hardening_verdict`, 4× `*_path`, `off_path_review_decision`, `known_escapes_caught`.

The carried-over "8 fields" OMIT `contract_version` (FR-13 AC1), `waiver_status` (FR-12 latch), `backtest_status` (NFR-1) from the SKILL.md append list — these are driven by an earlier draft exposing only 8 fields. 05-v2 §E catches it ("No `contract_version` field today — net-new"). **Builder must append the FULL field set from 07 §5.5, NOT just the 8 from 01/02.** See Compiled Gaps.

### 1d. Insertion points — CONSISTENT, anchor-drift caveat shared

01 and 05-v2 converge: seam = after Tier-1 (Wave 1.7), after Tier 2 (Waves 3-4), before report closure (Wave 5) → `### Wave 4.5: Pipeline Hardening Closure`. Both warn: anchor on heading TEXT not line numbers. 03 gives report-template insertion (after `## Follow-up tasks`, before `## Grounding Gaps`). No divergence.

### 1e. report-template `Closure verdict` enum — code-state CONFIRMED net-new

05-v2 §C: NO existing `Closure verdict` block / `pass|blocked|advisory` enum / `NOT PROVEN` token in report-template.md today ([CODE-CONTRADICTED] = net-new). 03 §2.3 inserts the §8 block with `Closure verdict: pass | blocked | advisory`. AGREE that the enum is net-new and additive. (Apply 1a expansion to 4-token.)

---

## Lens 2 — DRAFT vs RELEASE-SPEC section-number conflict (THE PRINCIPAL FINDING)

### Verified RELEASE-SPEC section structure (grep of header lines)

| RELEASE-SPEC § | Title |
|----------------|-------|
| §3 | Functional Requirements (FR-1..FR-13) |
| §3.1 | Escape/Wave/Evidence Traceability Matrix |
| §4 | Architecture — §4.1 New Files, §4.2 Modified Files, §4.5 State Registry, §4.6 Impl Order, §4.7 Validation Arch |
| §5 | Interface Contracts — §5.1 CLI, §5.2 Guard table, §5.3 Phase Contracts, §5.4 Verdict Truth Table, §5.5 Output Contract Field Schema, §5.6 Artifact Schemas, §5.7 Parser Decision |
| §6 | Non-Functional Requirements (NFR-1..NFR-6) |
| §7 | Risk Assessment |
| §8 | Test Plan (§8.1 unit, §8.2 integration, §8.3 E2E) |
| §9 | Migration & Rollout |
| §10 | Downstream Inputs (§10 For sc:tasklist L594) |
| §11 | Open Items (OI-1..OI-6) |
| §12 | Brainstorm Gap Analysis |

07 cites this structure correctly throughout (verified — 07 is faithful to RELEASE-SPEC).

### The conflict: carried-over 01/02/03 use a DIFFERENT (DRAFT/brainstorm) section map

The carried-over files systematically cite a section scheme that does NOT match the RELEASE-SPEC:

| Carried-over cite (01/02/03) | What they mean it to be | RELEASE-SPEC authoritative location (per 07) |
|------------------------------|-------------------------|----------------------------------------------|
| "spec §5.1" (command behavioral-summary advertise) | command advertise + CLI surface | §4.2 Modified Files (troubleshoot.md row) + §5.1 CLI Surface |
| "spec §5.2" (skill wire failure states / insertion seam) | skill changes + remediation gating | §4.2 Modified Files (SKILL.md row) + FR-1/FR-12 + §5.4 downstream no-override |
| "spec §6 / §6.1" (mode trigger) | applicability trigger | §3 FR-1 (Applicability Gate) + §5.6 H0 boundary-scan schema |
| "spec §6.2" (8 output-contract fields) | output contract field list | §5.5 Output Contract Field Schema (10 fields) + FR-13 |
| "spec §7" (the gate cards H1/H2/H3/H4/H5) | per-gate card schemas | §5.6 Required Artifact Schemas + §3 FR-3..FR-11 |
| "spec §8 (lines 299-312)" (report closure section) | REPORT.md closure block | §5.5/§4.2 report-template + FR-13 AC3 |
| "spec §9 (lines 329-333)" (5 new ref filenames) | new files | §4.1 New Files (lists 6 refs, not 5 — see Lens 2c) |
| "spec line 314" (NOT PROVEN) | NOT PROVEN blocker mandate | §3 FR-13 AC3 (L245) |
| line numbers 130-163, 136-151, 171-180, 241-253 | H1/H4 card line spans | DRAFT line numbers — do NOT resolve in RELEASE-SPEC |

**VERDICT on which to trust: 07 / the RELEASE-SPEC is AUTHORITATIVE.** The carried-over 01/02/03 §-numbers and line-numbers come from the PRIOR build's DRAFT spec (a brainstorm/design doc with a §5/§6/§7/§8/§9 layout), NOT the v1.1.0 RELEASE-SPEC. The *structural code findings* in 01/02/03 (SKILL.md line numbers, insertion points, house style, field-naming precedents) remain VALID and useful — those are code observations, not spec citations. Only the **spec §-number and spec-line-number citations** in 01/02/03 are stale and must be remapped to RELEASE-SPEC §3/§4/§5/§8 before the builder relies on them.

### 2c. Material consequence: "5 new refs" vs §4.1's "6 new files"

03 (§4) and 01 (§5) say **5 new refs** (citing DRAFT "§9 lines 329-333"). The RELEASE-SPEC **§4.1 lists 6 new ref files** (07 §2.1): the 5 named in 03 PLUS **`hardening-output-contract.md`** (verdict truth table + waiver latch propagation). 03 §4.6 even argues "5 new refs exactly (matching spec §9)" and folds H5 into the hub — but that argument is built on the DRAFT's 5-file inventory, NOT the RELEASE-SPEC's 6-file inventory. The RELEASE-SPEC §4.6 implementation order (07 §2.5) explicitly builds `hardening-output-contract.md` as step 2 ("resolves OI-1/OI-6 before downstream wiring"). **This is a real divergence: the builder must create 6 refs (incl. `hardening-output-contract.md`), not 5.** Flagged IMPORTANT. (03's H5-folds-into-hub reasoning is still fine; the missing file is the separate output-contract ref, which is additional to the H5 decision.)

---

## Lens 3 — 05-v2 (code crossval) vs 07 (spec): file existence / net-new

| Question | 05-v2 (code) | 07 (spec) | Agree? |
|----------|--------------|-----------|--------|
| 4 MODIFIED files exist (SKILL.md, troubleshoot.md, report-template.md, remediation-handoff.md) | all [CODE-VERIFIED] exist | §4.2 lists exactly these 4 | YES |
| New ref files absent (builder must CREATE) | all absent [CODE-VERIFIED absent] | §4.1 net-new | YES (but count: see Lens 2c) |
| `tests/troubleshoot/` exists? | [CODE-CONTRADICTED] — does NOT exist; CREATE dir + `__init__.py` + 7 files | §4.7 L347 / §8 puts tests under `tests/troubleshoot/` | YES — both treat it as net-new |
| `contract_version` field exists today? | NO — net-new (FR-13) | §5.5 requires it | YES |
| Sibling pytest dirs exist | `tests/skills/`, `tests/contracts/`, `tests/roadmap/` exist | (n/a) | consistent w/ 06 |

**No divergence between 05-v2 and 07 on file existence or `tests/troubleshoot/` net-new status.** 05-v2 names 6 refs absent in its §A Claim 2 list — wait: 05-v2 §A Claim 2 lists exactly **6** absent refs INCLUDING `hardening-output-contract.md`. So 05-v2 (fresh) AGREES with 07 (spec) on 6 refs, while carried-over 03/01 say 5. **05-v2 corroborates the Lens 2c finding: the authoritative count is 6.** This is the decisive cross-check — the fresh code crossval independently confirms 6 net-new refs.

06 (sync/tests) independently agrees: `tests/troubleshoot/` not referenced by any existing test (TESTING_REQUIREMENTS analysis), sync-dev auto-mirrors all refs (no count assertion), so 5-vs-6 does not break verify-sync — but the builder must still author all 6 to satisfy §4.1.

---

## Lens 4 — ADVISORY INVARIANT (the prior-build poison check)

**CRITICAL CHECK: Is "advisory removed" / "advisory forbidden" present in ANY research file?**

Grep + full-read result: **NO file removes, forbids, or contradicts the `advisory` token.** Evidence:

- 07 §3.0: explicit ⚠️ "do NOT drop `advisory`"; 7-row truth table rows 5+6 emit `advisory`; "Any claim that 'advisory was removed' is FALSE."
- 05-v2 §E/§C: "advisory is MANDATED by the spec (§4.5, §5.4 rows 5-6, FR-13) — do NOT drop it."
- 01 §6: lists `pass|blocked|advisory` as house-style verdict — advisory PRESENT.
- 02 §4: mirror recipe includes `advisory`.
- 03 §2.3/§2.4: `Closure verdict: pass | blocked | advisory` — advisory PRESENT.
- 06 / 04: do not touch the verdict enum.

**The prior build's poison (hallucinated "advisory removed") is ABSENT from this research set.** Both fresh files (05-v2, 07) actively inoculate against it with explicit "do NOT drop advisory" language. The carried-over files independently carry `advisory` in every verdict mention. **PASS on the advisory invariant — no CRITICAL flag.**

Minor residue (already noted in 1a): 01/03 sometimes write the 3-token shorthand `pass|blocked|advisory` (advisory present, `not_applicable` omitted). This is the OPPOSITE of the prior poison — they drop the skip sentinel, never `advisory`. Builder uses the full 4-token enum from 07.

---

## Lens 5 — FR→test mapping consistency (07 vs gap actions G-PRE-1, FR-12↔NFR-4)

| Item | 07 (spec extraction) | Consistency |
|------|----------------------|-------------|
| G-PRE-1 new test | §10: `test_h2_sibling_sweep_required_when_concept_shared` in `tests/troubleshoot/test_hardening_h2.py`, validates FR-6 (§3 FR-6 AC1 L162) | INTERNALLY CONSISTENT — file matches §8.1 H2 home (`test_hardening_h2.py`), FR-6 is the H2 sibling-sweep FR |
| FR-12 ↔ NFR-4 pairing | §9.6 + §10: pair FR-12 with `test_downstream_success_cannot_override_latched_hardening_verdict` (§8.2 #2); reinforced §10 L596 "FR-12 is highest-risk — pair with NFR-4 test" | CONSISTENT — NFR-4 (no-re-green durability) maps to integration #2, which is the FR-12 downstream-no-override test |
| FR→test map completeness | §9.4: all 13 FRs mapped to unit/integration/E2E; FR-6 flagged GAP (only indirect) → G-PRE-1 closes it | CONSISTENT — the gap and its fix are coherent |

The FR→test mapping in 07 is internally consistent and the two gap actions (G-PRE-1 new FR-6 test; FR-12↔NFR-4 pairing) are coherent with the §8 test plan. The carried-over 06 confirms NO existing test parses the skill, so the new `tests/troubleshoot/` files are genuinely net-new and additive (no collision). **No FR→test inconsistency between 07 and the gap actions.**

One nuance: 06 concluded TESTING_REQUIREMENTS = NONE for its own scope (sync/verify/markdownlint — no test parses the troubleshoot skill metadata). That is NOT in conflict with 07's §8 test plan: 06 is saying "adding refs won't break EXISTING tests," while 07 is saying "the spec MANDATES 12 unit + 5 integration NEW tests under `tests/troubleshoot/`." These are different statements (existing-test-breakage vs spec-mandated-new-tests) and both are true. **Builder must author the §8 tests regardless of 06's no-existing-test finding** — 06's scope was breakage, not the spec's net-new test mandate. Flagged so the builder does not misread 06 as "no tests needed."

---

## Contradictions Found (cross-file)

| # | Contradiction | Files | Severity | Resolution |
|---|---------------|-------|----------|------------|
| C1 | New ref count: **5** vs **6** | 03/01 say 5 (cite DRAFT §9); 05-v2/07 say 6 (incl. `hardening-output-contract.md`, RELEASE-SPEC §4.1) | IMPORTANT | TRUST 07/05-v2: **6 refs**. Two fresh files independently agree on 6. |
| C2 | Output-contract field count: **8** vs **10+3** | 01/02 say "8 new fields" (DRAFT §6.2); 07 §5.5 = 10 fields, §4.5 = 15 state vars (adds `contract_version`, `waiver_status`, `backtest_status`) | IMPORTANT | TRUST 07: append FULL field set; 05-v2 §E corroborates `contract_version` net-new. |
| C3 | Spec §-numbering scheme | 01/02/03 cite §5.1/§5.2/§6/§6.1/§6.2/§7/§8/§9 (DRAFT); 07 cites §3/§4/§5/§8 (RELEASE-SPEC) | IMPORTANT (systematic) | TRUST 07/RELEASE-SPEC. Carried-over CODE findings stay valid; only their SPEC citations are stale. |
| — | Verdict enum / advisory | none — all files agree advisory is present | — | No contradiction (Lens 4 PASS) |

No CRITICAL contradiction. C1/C2/C3 are all "carried-over file used the prior DRAFT spec; fresh files + RELEASE-SPEC are authoritative." None of them poisons the build IF the builder anchors on 07 + 05-v2.

---

## Compiled Gaps

### Critical Gaps (block synthesis/build) — NONE

No gap blocks the build outright. The advisory-poison check (the prior build's failure mode) is PASS. All authoritative content is present in 07.

### Important Gaps (affect correctness — builder MUST heed)

- **G1 — 6 refs, not 5.** Builder must create `hardening-output-contract.md` IN ADDITION to the 5 in 03/01. Source: RELEASE-SPEC §4.1 (07 §2.1), corroborated by 05-v2 §A Claim 2 (6 absent). 03/01's "5 refs" come from the DRAFT.
- **G2 — Full output-contract field set.** Builder must append `contract_version`, `waiver_status`, `backtest_status` to the SKILL.md Output Contract IN ADDITION to the 8 fields in 01/02. Source: RELEASE-SPEC §5.5/§4.5/FR-12/FR-13 (07 §4, §2.4); 05-v2 §E confirms `contract_version` net-new.
- **G3 — Remap stale spec §-citations.** Builder must NOT propagate 01/02/03's DRAFT §-numbers (§5.1/§5.2/§6/§7/§8/§9) or DRAFT line numbers (130-163, 136-151, 171-180, 241-253, 299-312, 329-333) into the tasklist. Re-cite against RELEASE-SPEC §3/§4/§5/§8 using 07's line numbers.
- **G4 — Author the §8 test suite.** 06's "TESTING_REQUIREMENTS = NONE" is scoped to existing-test-breakage only. The spec MANDATES 12 unit + 5 integration + 6 E2E tests under net-new `tests/troubleshoot/` (07 §9), PLUS the G-PRE-1 FR-6 test. Builder must not read 06 as "no tests needed."

### Minor Gaps (must still be fixed)

- **G5 — 4-token enum everywhere.** Expand 03's illustrative `Closure verdict: pass | blocked | advisory` (L142) to the full 4-token `pass | blocked | advisory | not_applicable`, OR keep section-omission semantics for `not_applicable` (03 L131 already does). Encode the full 4-token enum in the contract field.
- **G6 — H5-fold reasoning rests on DRAFT.** 03 §4.6's "5 refs exactly" argument for folding H5 into the hub is sound on its own merits (H5 is a Rule producing a decision token), but its "matching spec §9" justification is stale. Keep the H5-fold decision; drop the "§9 = 5 files" justification (the RELEASE-SPEC §4.1 has 6 files because of the separate output-contract ref, not because of H5).

---

## Depth Assessment

**Expected depth:** Deep (spec-faithful extraction + code crossval for a multi-file build tasklist).
**Actual depth achieved:** Strong. 07 is a faithful, line-cited extraction of every authoritative structure (verdict truth table, 15-var registry, 5 artifact schemas, full FR/escape/NFR→test maps). 05-v2 is a clean code-vs-spec crossval with explicit [CODE-VERIFIED]/[CODE-CONTRADICTED] tags. The carried-over 01/02/03/06 provide accurate code-side structural maps (SKILL.md line numbers, insertion points, house style, lint gates) that remain valid.

**Missing depth elements:** None at the spec level. The only weakness is that carried-over 01/02/03 were not re-baselined against the RELEASE-SPEC's section numbering when 07 was produced — hence the stale §-citations (G3). The fresh files (05-v2, 07) compensate by independently establishing the authoritative 6-ref / full-field-set / 4-token-enum facts.

---

## Recommendations

1. **Anchor the tasklist on 07 + 05-v2** for all spec content (§-numbers, line numbers, field set, ref count, verdict enum). Treat 01/02/03/06 as CODE-side structural references only (SKILL.md insertion points, house style, lint/sync gates) — accurate for code, stale for spec citations.
2. **Create 6 refs** (G1): the 5 in 03 PLUS `hardening-output-contract.md`.
3. **Append the full output-contract field set** (G2): 8 from 01/02 PLUS `contract_version`, `waiver_status`, `backtest_status`.
4. **Remap DRAFT §-citations to RELEASE-SPEC §3/§4/§5/§8** (G3) before they enter the tasklist DoD lines.
5. **Author the full §8 test suite** + G-PRE-1 FR-6 test (`test_h2_sibling_sweep_required_when_concept_shared`) + pair FR-12 with the NFR-4 test (G4).
6. **Encode the 4-token enum** with advisory mandatory (G5) — the advisory-poison check is PASS, keep it that way.
7. Honor the G1-HALT (07 §12): build the tasklist, but implementation items stay gated behind G1 approval; OI-2/OI-3/OI-5 authored as `needs_human_decision` HALT items.

---

## VERDICT: PASS (with 4 important + 2 minor gaps to heed — no CRITICAL, no advisory-poison)

The research set is internally cross-consistent on every load-bearing invariant once the authority order is applied: **07 + 05-v2 (fresh, RELEASE-SPEC-aligned) over 01/02/03 (carried-over, DRAFT-aligned).** The advisory invariant is PASS — the prior build's "advisory removed" poison is ABSENT and actively inoculated against by both fresh files. The contradictions found (C1 5-vs-6 refs, C2 8-vs-full field set, C3 stale §-numbering) all resolve cleanly in favor of the RELEASE-SPEC, and the fresh code crossval (05-v2) independently corroborates the authoritative side of C1 and C2. The builder can proceed PROVIDED it anchors on 07/05-v2 and heeds gaps G1-G4.

**Gap list (for the build gate):** G1 (6 refs not 5, IMPORTANT), G2 (full field set incl. contract_version/waiver_status/backtest_status, IMPORTANT), G3 (remap DRAFT §-citations, IMPORTANT), G4 (author §8 test suite + G-PRE-1 + FR-12↔NFR-4, IMPORTANT), G5 (4-token enum, MINOR), G6 (drop stale H5-fold §9 justification, MINOR).
