# Fanout FM2 — Spec-Change → New-Ref-Creation-Item Mapping

**Partition:** The 5 NEW REF creation items (Phase 2 Steps 2.1–2.5).
**Date:** 2026-06-10
**Author role:** spec-delta → tasklist-item refactor mapper (read-only; no team coordination).

## Inputs read

- Refactored spec (post-adjudication): `troubleshoot-pipeline-hardening-spec.md` — read FULLY. The spec already has ALL CS edits applied (per-gate `status` tokens, `NOT_PROVEN`, verdict invariant C2, trigger→gate map T1–T9, M11 manifest, M9 fixpoint, M10 fixture, M5 no-op, enum without `advisory`).
- Change-set: `spec-critique-adjudication.md` — CS-1..CS-m1 (13 edit clusters).
- Tasklist: `TASK-RF-troubleshoot-hardening-20260610-144537.md` — read FULLY (Steps 2.1–2.5 are the partition; Phase 4/5 QA gates consume ref content).

## CRITICAL CROSS-CUTTING FINDING (applies to ALL 5 items)

The 5 new-ref creation items (Steps 2.1–2.5) and their downstream QA-gate prompts (Phase 4/5) were authored against a **PRE-ADJUDICATION** spec snapshot. The CURRENT spec on disk has all 13 CS edits applied, but the tasklist directives still encode the OLD spec. Three systemic divergences appear in every affected item:

1. **Stale verdict enum.** Steps 2.1, 2.8, 2.9, 2.12 and QA Steps 4.3/4.10-style consistency lenses + GF-5 direct the executor to use the FULL enum `pass | blocked | advisory | not_applicable` "per GF-5". **CS-3 (C1+C3) DELETED `advisory`.** The current spec §6.2 line 112 and §8 line 368 are explicit: enum is exactly `{pass, blocked, not_applicable}`; `advisory` "was removed because it had no selection criterion and no defined consumer contract." Every item that says "FULL enum … advisory … per GF-5" now produces a SPEC-INFIDELITY ref. GF-5 itself is superseded by CS-3.

2. **Missing per-gate `status` token (CS-7/M7).** The spec §6.2 now carries, for EACH gate, a `*_status` enum `{PASS|FAIL|NA|NOT_PROVEN}` DISTINCT from the `*_card_path`. The new-ref items reference only the path fields / old 8-field framing. The output-contract table is no longer 8 fields — it now has paired status+path fields plus `gate_na_rationale`. Items 2.1 ("8-field output-contract table") must be re-scoped.

3. **Stale absolute line numbers.** The critique's line citations (e.g. "spec lines 270-280", "spec line 314") and the tasklist's embedded line refs (e.g. 2.2 "spec lines 130-163 / 136-151", 2.5 "spec lines 241-253") reference the PRE-CS spec. The current spec is longer (CS edits inserted ~120 lines). The tasklist already warns line numbers are off-by-one trailing-newline artifacts (GF-1); the real delta is much larger than one line. All five items must anchor on TEXT/section-name, never line number — which the items already say in principle but then contradict with explicit line cites.

These three are the dominant refactor drivers. Per-item specifics below.

---

## Item 1 — HUB: pipeline-hardening-closure.md (Step 2.1)

**Item ID:** Step 2.1 (`#### File: pipeline-hardening-closure.md (NEW — Hub ref)`).

This is the heaviest-impacted item. The HUB must now encode (a)–(g) from the partition brief, almost NONE of which the current Step 2.1 directive captures.

### REQUIRED added content (cite current-spec section the ref must reproduce)

| Brief item | Spec source the hub must reproduce | In Step 2.1 today? |
|---|---|---|
| (a) CS-1 §6.1 trigger→gate map T1–T9 | §6.1 table (T1–T9 → mandatory gate(s)) + "Mandatory-gate rule" + "union = mandatory gate set" | **NO.** 2.1 says reproduce "the §6.1 Trigger bullet list" — but §6.1 is no longer a bullet list; it is a 9-row T1–T9 trigger→gate TABLE plus the mandatory-gate rule. Must add the full table verbatim. |
| (b) CS-2 verdict invariant + mandatory-gate-set | §6.2 "Verdict invariant (C2 — apex)" three-clause definition (not_applicable iff / pass iff all-mandatory-PASS+zero-NOT_PROVEN+off-path / blocked otherwise) + the vacuous-pass-hole sentence | **NO.** 2.1 has no verdict-invariant directive. Must add C2 verbatim. |
| (c) CS-2b/M2 H5-mandatory + off-path→verdict | §6.2 "Off-path→verdict invariant (M2)" + Rule H5 "Mandatory status (M2)" paragraph (`off_path_review_decision=required ∧ ¬(performed ∨ waived) ⇒ verdict=blocked`) | **PARTIAL.** 2.1 loads §7 Rule H5 trigger/forms/waiver but NOT the new "H5 is NOT optional / joins mandatory gate set / required⇒blocked" invariant. Must add. |
| (d) CS-3 verdict enum WITHOUT advisory | §6.2 line 112 + "No `advisory` verdict (C3)" note + §8 line 368 | **WRONG.** 2.1 explicitly directs the FULL enum `pass\|blocked\|advisory\|not_applicable` "per GF-5". Must be changed to `{pass, blocked, not_applicable}` and the C3 rationale note added. |
| (e) CS-4 defaults | §6.2 table Default column + the `pipeline_hardening_applicable` "MUST be written by H0 before any read" rule + `gate_na_rationale` default `{}` | **NO.** 2.1 has no defaults directive. Must add the Default column / H0-writes-before-read rule. |
| (f) §4 six rejected-substitutions | §4 list (already in 2.1) | **YES** — 2.1 already maps the 6 items 1→H1,2→H4,3→H1,4→H3,5→H2,6→H4/H5. Keep. (Spec §4 list is unchanged by CS.) |
| (g) NOT_PROVEN convention | §6.2 "Status/path rule (M7)" + §8 NOT_PROVEN-is-first-class paragraph + "A `NA` without rationale ⇒ NOT_PROVEN" | **PARTIAL.** 2.1 §"Closure verdict + NOT PROVEN rule" mentions NOT PROVEN as a blocker but lacks: (i) `status ∈ {PASS|FAIL|NA|NOT_PROVEN}` as a FIRST-CLASS per-gate token, (ii) M7 path=null only when status∈{NA,NOT_PROVEN}, (iii) bare-NA⇒NOT_PROVEN. Must add. |

### Additional hub content gaps vs current spec (beyond a–g)

- **Output contract fields section (2.1 "§6.2 8-field table … columns Field/Type/Meaning"):** STALE. The §6.2 table now has MORE than 8 rows (each gate = status + path; plus `gate_na_rationale`, plus the unchanged `off_path_review_decision`, `known_escapes_caught`, the two top-level fields). The hub must reproduce the CURRENT §6.2 table (Field/Type/Default/Meaning) including every `*_status` row, the M7 status/path rule, and the C2 invariant. The "8-field" count is wrong and the column set (no Default) is wrong.
- **`known_escapes_caught` pattern (CS-m1):** §6.2 constrains items to `^E\d+$` or `^E\d+\+$` (so `E6+` valid). 2.1 does not mention the pattern. Add.

### Embedded acceptance/verification criteria — MUST CHANGE?

**YES — the item's embedded directive must change** in five places: (1) drop `advisory` from every enum instruction; (2) replace "8-field output-contract table" with the full current §6.2 table incl. status tokens + Default column + M7 rule + C2 invariant; (3) add the §6.1 T1–T9 trigger→gate map (replacing "Trigger bullet list"); (4) add CS-2b H5-mandatory/off-path→blocked invariant; (5) add CS-4 defaults + CS-m1 `known_escapes_caught` pattern. The item's "remediation gating" line currently gates the Tier-3 offer on `pipeline_hardening_verdict ∈ {pass, advisory}` — **`advisory` is dead**; must become `∈ {pass, not_applicable}` (matching Step 2.11(b) Wave-6 precondition `∈ {pass, not_applicable}`, which is already correct in the tasklist — an internal contradiction the hub item must resolve toward the no-advisory side).

---

## Item 2 — contract-enumeration.md (H2) (Step 2.3)

**Item ID:** Step 2.3 (`#### File: contract-enumeration.md (NEW — Wave H2)`).

### REQUIRED added content

- **CS-11 (M11) consumer-discovery manifest.** Current spec §7-H2 adds a "Required evidence — consumer-discovery manifest (M11)" block: the ledger MUST be accompanied by a machine-checkable manifest (exact search terms + symbol/reference-search queries + result sets), and **absence of the manifest ⇒ H2 `status = NOT_PROVEN` (not PASS)**, which forces `verdict = blocked`. The H2 blocking-rule list also gained a 4th bullet: "H2 = `NOT_PROVEN` if the consumer-discovery manifest is absent or not reproducible."
- Step 2.3 today directs ONLY: the 9-row ledger, the THREE-bullet blocking rule (lines 184-187), and escapes-caught. It has **NO manifest directive and is missing the 4th blocking bullet.**

### Embedded acceptance/verification criteria — MUST CHANGE?

**YES.** Step 2.3 must add: (1) a `## Consumer-discovery manifest` section (or fold into a Required-evidence section) reproducing the §7-H2 M11 block — exact-search-terms + symbol/ref queries + result sets requirement, and "absent ⇒ H2 = NOT_PROVEN"; (2) the 4th blocking-rule bullet (manifest absent/non-reproducible ⇒ NOT_PROVEN). The "three spec bullets at lines 184-187" instruction is now a FOUR-bullet rule. The ledger table itself (9 rows) is UNCHANGED by CS — keep that part as-is.

---

## Item 3 — unmask-and-sweep.md (H3) (Step 2.4)

**Item ID:** Step 2.4 (`#### File: unmask-and-sweep.md (NEW — Wave H3)`).

### REQUIRED added content

- **CS-9 (M9) fixpoint after discovery.** Current spec §7-H3 adds "Fixpoint after discovery (M9)": an H3 sweep that surfaces a NEW boundary/consumer MUST either (a) re-trigger H0 reclassification + H2 enumeration (recomputing the mandatory gate set), OR (b) be logged as an explicit follow-up escape with a named disposition; a sweep-discovered escape MUST NOT be recorded with no gate applied. The blocking-rule list also gained a 3rd bullet: "H3 fails (or its discovery is `NOT_PROVEN`) if a sweep-discovered new boundary/consumer is neither re-enumerated (H0/H2) nor logged as a dispositioned follow-up escape."
- **CS-10 (M10, narrowed) named E3-style negative fixture as completion criterion.** Current spec §7-H3 adds a "Completion criteria (explicit, not optional)" block: a passing **E3-style sibling-heading negative fixture** (same-token sibling heading in the full generated artifact that must NOT hard-fail) is an explicit H3 completion criterion; H3 cannot be `PASS` for any generated-artifact/heuristic-parser change without it.
- Step 2.4 today directs ONLY: Required-outputs 10-item list, Minimum-regression 4-item pattern, the TWO-bullet blocking rule (lines 220-223), and escapes-caught. It has **NO fixpoint directive, NO completion-criteria/E3-fixture directive, and is missing the 3rd blocking bullet.**

### Embedded acceptance/verification criteria — MUST CHANGE?

**YES.** Step 2.4 must add: (1) a `## Completion criteria` section naming the passing E3-style sibling-heading negative fixture as a mandatory H3 completion gate (CS-10); (2) a `## Fixpoint after discovery` section reproducing the M9 re-enter-H0/H2-OR-dispositioned-follow-up rule (CS-9); (3) the 3rd blocking-rule bullet (sweep-discovered new boundary neither re-enumerated nor dispositioned ⇒ FAIL/NOT_PROVEN). The "two spec bullets at lines 220-223" instruction is now a THREE-bullet rule. The 10-item Required-outputs list and 4-item Minimum-regression pattern are UNCHANGED — keep.

---

## Item 4 — effective-input-proof.md (H4) (Step 2.5)

**Item ID:** Step 2.5 (`#### File: effective-input-proof.md (NEW — Gate H4)`).

### REQUIRED added content

- **CS-5 (M5) no-op vs empty-with-changes branch.** Current spec §7-H4 adds "No-op vs empty-with-changes (M5 — define both branches)": **No runtime changes ⇒ H4 = `NA`** with a no-op proof + a required `gate_na_rationale` entry (legitimate, non-blocking); **changes present ∧ effective input empty ⇒ H4 = `FAIL`** (fail-closed). The blocking-rule list also gained a 3rd bullet: "H4 = `NA` (no-op) only with an explicit no-op proof + rationale; otherwise an empty input under known changes is `FAIL`, never `NA`."
- Step 2.5 today directs ONLY: the "Maps to R5" line, the Trigger sentence, the 10-field "Effective Input Proof" card, the TWO-bullet blocking rule (lines 255-258), and escapes-caught. It has **NO no-op/empty branch directive and is missing the 3rd blocking bullet.**

### Embedded acceptance/verification criteria — MUST CHANGE?

**YES.** Step 2.5 must add: (1) a `## No-op vs empty-with-changes` section reproducing both M5 branches (no-op ⇒ NA+proof+rationale; changes∧empty ⇒ FAIL fail-closed); (2) the 3rd blocking-rule bullet (NA only with no-op proof+rationale, else FAIL). The "two spec bullets at lines 255-258" is now a THREE-bullet rule. The 10-field card and Trigger sentence are UNCHANGED — keep byte-faithful.

---

## Item 5 — runtime-entrypoint-verification.md (H1) (Step 2.2)

**Item ID:** Step 2.2 (`#### File: runtime-entrypoint-verification.md (NEW — Gate H1)`).

### REQUIRED added content — assessment

H1's card (13 fields), blocking rule (2 bullets), and escapes-caught mappings are **substantively UNCHANGED** by the CS set. CS-3's negative-control list bullet "advisory as fatal" in the H1 blocking rule is an E4-EXAMPLE negative control (a forbidden interpretation H1 must catch) — it is NOT a verdict enum value, so it stays as-is (the partition brief confirms this: "keep, that's an E4 example not our verdict"). Step 2.2's card/blocking-rule/escapes directives remain faithful.

**However** — one gap from the CS-7/M7 status-token change touches H1 indirectly:

- **Per-gate status output.** Under CS-7, H1 now emits a first-class `runtime_entrypoint_status ∈ {PASS|FAIL|NA|NOT_PROVEN}` distinct from `runtime_entrypoint_card_path`, governed by the M7 status/path rule (path=null only when status∈{NA,NOT_PROVEN}; a gate that ran but produced no artifact is NOT_PROVEN). Whether the H1 ref must REPRODUCE this depends on the ref's scope: the card itself (spec §7-H1) does not embed the status token (status lives in §6.2). The current Step 2.2 directive (card + blocking rule + escapes-caught) does NOT mention the status token.

### Embedded acceptance/verification criteria — MUST CHANGE?

**LIGHT / CONDITIONAL.** The H1 card content is unchanged — Step 2.2's core directive holds. Recommended ADDITIVE change: add a brief `## Status output` note stating H1 emits `runtime_entrypoint_status ∈ {PASS|FAIL|NA|NOT_PROVEN}` paired with (but distinct from) `runtime_entrypoint_card_path` per the M7 rule, so the gate ref is consistent with the §6.2 contract the hub now reproduces. This is the only material change for H1; if scope is kept minimal the status convention can live solely in the hub (Item 1) — but then the hub MUST own it (see Item 1 gap (g)). Flag: do NOT add `advisory` anywhere in H1's "advisory as fatal" negative control becoming a verdict — it is and stays a forbidden-interpretation example.

---

## Coverage gaps — new ref-content requirements with NO tasklist coverage

The following CS-introduced ref-content requirements have **ZERO directive coverage** in the current Steps 2.1–2.5 and would be silently dropped if the items run as written:

1. **CS-3 enum correction (drop `advisory`)** — UNCOVERED and actively MIS-directed (items + GF-5 mandate the wrong enum). Highest-priority fix; affects Items 1, plus SKILL/report items 2.8/2.9/2.12/2.14 (out of this partition but flagged).
2. **CS-7/M7 per-gate status tokens + status/path rule** — UNCOVERED in Items 1 (hub §6.2 table), 5 (H1). The "8-field table" framing structurally cannot express paired status+path+rationale.
3. **CS-2 verdict invariant (C2)** — UNCOVERED in Item 1. No item reproduces the pass/blocked/not_applicable total-function definition or the vacuous-pass-hole closure.
4. **CS-1 §6.1 trigger→gate map (T1–T9)** — UNCOVERED in Item 1. The item references a "Trigger bullet list" that no longer exists.
5. **CS-2b H5-mandatory / off-path→blocked invariant** — UNCOVERED in Item 1 (only the old trigger/forms/waiver lists are loaded).
6. **CS-4 defaults + H0-writes-before-read** — UNCOVERED in Item 1.
7. **CS-11 consumer-discovery manifest** — UNCOVERED in Item 2 (H2).
8. **CS-9 fixpoint after discovery** — UNCOVERED in Item 3 (H3).
9. **CS-10 named E3-style negative fixture completion criterion** — UNCOVERED in Item 3 (H3).
10. **CS-5 no-op vs empty-with-changes** — UNCOVERED in Item 4 (H4).
11. **CS-m1 `known_escapes_caught` pattern** — UNCOVERED in Item 1.

**Downstream QA risk:** Phase 4 Step 4.3 (internal-consistency lens) and Step 4.6/5.1 (spec-fidelity lenses) explicitly instruct agents to check the enum is "the FULL `pass | blocked | advisory | not_applicable` everywhere (GF-5)". With the current spec, those lenses would FLAG correct (no-advisory) refs as failures and PASS incorrect (advisory-bearing) refs — i.e. the QA gates are inverted on the enum. The QA prompts (4.3, 4.6, 5.1) and GF-5 must be corrected in lockstep with the ref items, or the gate will enforce the stale spec.

---

## Mapping table

| CS-id | Ref item (Step) | Change type | Directive |
|---|---|---|---|
| CS-3 (C1+C3) | 2.1 hub (+2.2 H1 negative-control wording check) | CORRECTION (enum) | Drop `advisory`; enum = `{pass, blocked, not_applicable}` everywhere; add C3 rationale note; fix remediation-gating to `∈ {pass, not_applicable}`. Supersede GF-5. |
| CS-7 (M7) | 2.1 hub; 2.2 H1 (light) | ADDITION (status token) | Replace "8-field table" with current §6.2 table incl. each `*_status ∈ {PASS\|FAIL\|NA\|NOT_PROVEN}`, `gate_na_rationale`, Default column, and the M7 status/path rule. H1 gets optional `## Status output` note. |
| CS-2 (C2) | 2.1 hub | ADDITION (invariant) | Add verbatim C2 verdict invariant (not_applicable/pass/blocked total function) + vacuous-pass-hole closure sentence. |
| CS-1 (M1) | 2.1 hub | REPLACEMENT (trigger) | Replace "Trigger bullet list" with the §6.1 T1–T9 trigger→gate MAP table + mandatory-gate rule + union-of-pinned-gates definition. |
| CS-2b (M2) | 2.1 hub | ADDITION (H5 mandatory) | Add H5-is-mandatory-on-trigger + `off_path required ∧ ¬(performed∨waived) ⇒ verdict=blocked` invariant; H5 joins mandatory gate set. |
| CS-4 (M4) | 2.1 hub | ADDITION (defaults) | Add §6.2 Default column + `pipeline_hardening_applicable` MUST-be-written-by-H0-before-read + `gate_na_rationale` default `{}`. |
| CS-m1 (m1) | 2.1 hub | ADDITION (pattern) | Constrain `known_escapes_caught` items to `^E\d+$` or `^E\d+\+$` (E6+ valid). |
| CS-11 (M11) | 2.3 H2 | ADDITION (manifest) | Add `## Consumer-discovery manifest` (search terms + symbol/ref queries + result sets); absent ⇒ H2 `status=NOT_PROVEN`; add 4th blocking bullet. |
| CS-9 (M9) | 2.4 H3 | ADDITION (fixpoint) | Add `## Fixpoint after discovery`: sweep-discovered new boundary ⇒ re-enter H0/H2 OR dispositioned follow-up; add 3rd blocking bullet. |
| CS-10 (M10) | 2.4 H3 | ADDITION (fixture) | Add `## Completion criteria` naming a passing E3-style sibling-heading negative fixture as mandatory H3 completion gate. |
| CS-5 (M5) | 2.5 H4 | ADDITION (no-op branch) | Add `## No-op vs empty-with-changes`: no-op⇒NA+proof+rationale; changes∧empty⇒FAIL; add 3rd blocking bullet. |
| (line refs) | 2.1–2.5 all | ANCHOR FIX | Strip all absolute spec-line citations (pre-CS); anchor on section name / heading text only. |
| CS-3/GF-5 | QA 4.3, 4.6, 5.1 (downstream, flagged) | CORRECTION (gate) | Re-point enum checks to `{pass, blocked, not_applicable}`; QA prompts currently enforce the stale advisory enum and would invert. |
