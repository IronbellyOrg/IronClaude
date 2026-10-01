# Fan-out FM3 — Report Template + Remediation-Handoff + QA/Fidelity + A.10 Fold-in

**Partition:** REPORT TEMPLATE items, remediation-handoff item, QA/M4-fidelity/Phase-4-lens items, acceptance-criteria, plus the A.10 tasklist-structure findings fold-in.

**Inputs read (full):**

- Refactored spec: `.dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-spec.md` (§5.2, §6.1, §6.2, §7-H0..H5, §8, §10 acceptance 1-15)
- Change-set: `.dev/troubleshoot-meta/20260610T141100Z/spec-critique-adjudication.md` (CS-1..CS-m1, 13 edit clusters)
- Tasklist: `TASK-RF-troubleshoot-hardening-20260610-144537.md` (Steps 1.1-5.5 + Post-Completion Actions)
- A.10 findings: `qa/qa-task-validation-consolidated.md` (C1/I1/I2/M1/M2/M3 → referenced as A10-*)

**Scope boundary note:** This fan-out OWNS the report-template, remediation-handoff, QA/fidelity, and A.10 items. It also flags (does not own) the SKILL.md output-contract item (Step 2.8) and hub-ref item (Step 2.1) where they embed the now-changed verdict enum and the §6.2 contract, because the QA lenses cross-check those surfaces; the SKILL/refs partition fan-out should make the primary edits there. Wherever the verdict enum or contract fields are flagged below, the SINGLE source of truth is the refactored spec §6.2 (enum = `{pass, blocked, not_applicable}`; per-gate `status ∈ {PASS|FAIL|NA|NOT_PROVEN}`).

---

## OVERARCHING SPEC DELTA (drives every item below)

The refactored spec changed five things that ripple through this partition:

1. **Verdict enum dropped `advisory`** → now exactly `{pass, blocked, not_applicable}` (CS-3 / C1+C3, spec §6.2 L112, §8 L368, acceptance 11). **The old GF-5 "divergence note" is now OBSOLETE** — the spec §8 block (L363) now explicitly carries all three tokens AND `not_applicable`, and §8 states the verdict is "identical to §6.2." There is no longer a §8-vs-§6.2 divergence to reconcile.
2. **Per-gate `status` token** `{PASS|FAIL|NA|NOT_PROVEN}` is now a FIRST-CLASS field distinct from `*_card_path` (CS-7 / M7, spec §6.2 L113-121). The report lines (§8 L356-359) now read `PASS | FAIL | NA | NOT_PROVEN` (four tokens), not `PASS|FAIL|N/A`.
3. **Per-gate `rationale` field** required when status is `NA`; a bare `NA` is invalid → renders `NOT_PROVEN` (CS-3b / M3, spec §8 L356-359, L366).
4. **Verdict invariant (C2)** — verdict is a total function of gate statuses; `pass` is unreachable unless every mandatory gate is `PASS` w/ non-null path, zero `NOT_PROVEN`, off-path satisfied; an all-null run is `blocked` not `pass` (spec §6.2 L129-135, acceptance 12). Plus the **off-path→verdict line** (M2, §8 L360) and **firing-triggers/mandatory-gate-set line** (§8 L355).
5. **`NOT_PROVEN`** is now a first-class gate STATUS token (not prose), forcing `blocked` (spec §8 L370, acceptance 14). The old report used the prose token `NOT PROVEN` (two words) as a verdict-only blocker.

Every item that embeds the §8 report block, the §6.2 contract, or the verdict enum must be updated for items 1-5. Every QA/fidelity lens that asserts the OLD enum must be re-pointed at the NEW invariants.

---

## A. REPORT TEMPLATE ITEMS

### Step 2.12 — `report-template.md` `## Pipeline Hardening Closure` section (INSIDE four-backtick fence)

- **Item ID:** Step 2.12
- **Change type:** EDIT (rewrite the embedded §8 block content + the GF-5 note)
- **Directive:** The embedded report-block content in this item is stale on five axes. Replace it to match refactored spec §8 (L350-368) verbatim:
  1. **Add the firing-triggers line:** `- Firing triggers / mandatory gate set: T... → H...` (spec §8 L355). Currently absent from the item's bullet enumeration.
  2. **Change every gate line to four-token status + rationale:** each of the four gate lines must read `PASS | FAIL | NA | NOT_PROVEN — <card path> — rationale (required if NA): <…>` (spec §8 L356-359). The item currently specifies `PASS|FAIL|N/A — <card path>` (three tokens, no `NOT_PROVEN`, no rationale clause).
  3. **Rewrite the off-path line with the verdict consequence:** `- Off-path review decision: required | performed | waived_with_rationale | not_required — (if required and not performed/waived_with_rationale ⇒ verdict = blocked)` (spec §8 L360, M2 co-location).
  4. **Constrain known-escapes to the pattern:** `- Known escapes this would have caught: E... (each \`^E\d+$\` or \`E\d+\+\`)` (spec §8 L362, CS-m1).
  5. **Closure verdict line = three tokens only:** `- Closure verdict: pass | blocked | not_applicable` (spec §8 L363). **Remove `advisory`.**
  6. **DELETE the GF-5 note** the item currently instructs ("...`Closure verdict: pass | blocked | advisory | not applicable per GF-5`"). Per A10-M2 this note is now obsolete; replace any GF-5/`advisory` reference with the C1/C3 mapping note: "the closure verdict enum is exactly `{pass, blocked, not_applicable}`, identical to §6.2; there is no `advisory`" (spec §8 L368).
  7. **Add the status/path/rationale rule reference:** include the spec §8 L366 rule that a `null`/absent path is permitted only when status is `NA` or `NOT_PROVEN`, and a bare `NA` (no adjacent rationale) renders `NOT_PROVEN`.
  - Keep: the conditional-render sentence (render only when `pipeline_hardening_applicable=true`), placement inside the four-backtick fence between `## Follow-up tasks` and `## Grounding Gaps`, no nested three-backtick fence.

### Step 2.13 — `report-template.md` `## Pipeline Hardening Closure rule` (append after EOF, OUTSIDE fence)

- **Item ID:** Step 2.13
- **Change type:** EDIT (upgrade NOT_PROVEN from prose-verdict to first-class status token + verdict invariant)
- **Directive:** The item currently frames `NOT PROVEN` (two-word prose) as a verdict-blocker only. Refactored spec §8 L370 + acceptance 14 make `NOT_PROVEN` (underscore) a first-class gate STATUS. Update the appended rule section to state:
  1. The literal token is `NOT_PROVEN` (underscore, first-class gate status — NOT "NOT PROVEN" prose, NOT "low confidence", NOT "unverified"); a gate that ran but produced no artifact is `NOT_PROVEN`, never silent `null` (spec §6.2 L125 M7 + §8 L366).
  2. **Per the verdict invariant (C2):** `Closure verdict: blocked` whenever ANY gate is `NOT_PROVEN`, ANY mandatory gate is `FAIL`, a required `NA` lacks a rationale, OR off-path is `required` and not performed/waived (spec §6.2 L133, §8 L370). State that `pass` is a total function of gate statuses and is unreachable for an all-`NA`/all-null run (acceptance 12 — vacuous-pass hole closed).
  3. A bare `NA` with no adjacent rationale MUST be rendered `NOT_PROVEN` (spec §8 L366).
  - Keep: placement OUTSIDE the four-backtick fence after `## Behavior-is-documented rule`; cross-links to the 4 gate refs + hub ref; MD024 non-duplicate heading.

### Step 2.1 — hub ref `pipeline-hardening-closure.md` (CONTAINS report cross-ref + §6.2 table + verdict enum)

- **Item ID:** Step 2.1 (report-template-adjacent; primary owner is the SKILL/refs partition, flagged here for the verdict/report surface)
- **Change type:** EDIT (drop `advisory`; add status/rationale/invariant; remove GF-5 note)
- **Directive (report/verdict surface only):**
  1. `## Output contract fields` — the §6.2 table must now use the THREE-token enum `pass | blocked | not_applicable` for `pipeline_hardening_verdict` (NOT the "FULL enum `pass | blocked | advisory | not_applicable` per GF-5" the item currently instructs). Add the per-gate `status` column/rows (`PASS|FAIL|NA|NOT_PROVEN`) and the `gate_na_rationale` map field (spec §6.2 L113-121). **The "per GF-5" instruction is obsolete (A10-M2) — strike it.**
  2. `## Closure verdict + NOT PROVEN rule` — rename concept to `NOT_PROVEN` first-class status; encode the C2 verdict invariant (verdict is a total function; `pass` requires all-mandatory-`PASS` + zero `NOT_PROVEN` + off-path satisfied; else `blocked`); keep "intentionally stronger than ordinary confidence language."
  3. `## Remediation gating` — the item currently gates the Tier-3 offer on `pipeline_hardening_verdict ∈ {pass, advisory}`. **Change to `pipeline_hardening_verdict ∈ {pass, not_applicable}`** (advisory removed; a `not_applicable` zero-trigger run is non-blocking — see spec §6.2 invariant + acceptance 11). This must agree with Step 2.11(b) and Step 2.14(a) below.
  4. `## Report section` cross-ref — ensure it points at the updated Step 2.12 block (three-token verdict, status+rationale lines).

---

## B. REMEDIATION-HANDOFF ITEM

### Step 2.14 — `remediation-handoff.md` precondition subsection + failure-mode row

- **Item ID:** Step 2.14
- **Change type:** EDIT (drop `advisory` from the gating set; add verdict-invariant + NOT_PROVEN-status reference)
- **Directive:** §5.2 failure-state wiring is unchanged in PRINCIPLE (the handoff still must not offer Tier-3 when an escape is unremediated), but it is now backed by the C2 verdict invariant and the first-class `NOT_PROVEN` status. Update:
  1. **(a) precondition subsection** — the item currently gates the offer on `pipeline_hardening_verdict ∈ {pass, advisory}`. **Change to `pipeline_hardening_verdict ∈ {pass, not_applicable}`** (advisory removed). Add a one-line back-reference to the C2 verdict invariant: "a `blocked` verdict (any required gate `NOT_PROVEN`/`FAIL`, or a `NA` without rationale, or off-path `required`-but-not-satisfied) mechanically BLOCKS the chain — see `refs/pipeline-hardening-closure.md` verdict invariant." Keep the cross-link to the authoritative §5.2 rule in the hub ref (do not duplicate).
  2. **(b) failure-modes row** — update the row trigger from "`pipeline_hardening_verdict ∈ {blocked}` or any required gate is `NOT PROVEN` / `N/A`-without-rationale" to use the first-class status spelling `NOT_PROVEN` and the invariant: "`pipeline_hardening_applicable=true` ∧ `pipeline_hardening_verdict = blocked` (any mandatory gate `FAIL`/`NOT_PROVEN`, required `NA` lacking rationale, or off-path `required` ∧ ¬performed/¬waived)". Behaviour text otherwise unchanged (do NOT offer; escape NOT remediated; surface the `NOT_PROVEN` gate(s) + verdict `blocked`; `remediation_accepted=false`).
  - Net: the handoff item DOES need the verdict-invariant reference and the enum/token corrections; the principle is unchanged.

---

## C. QA / M4 FIDELITY / PHASE-4 LENS ITEMS

All Phase-4/Phase-5 lens prompts that assert "the FULL enum `pass | blocked | advisory | not_applicable` (GF-5)" are now ASSERTING A SPEC-VIOLATION and will produce false PASS / false FAIL against the refactored spec. Every such assertion must flip to the three-token enum + the new invariants.

### Step 4.3 — rf-qa structural lens: internal-consistency

- **Item ID:** Step 4.3
- **Change type:** EDIT (enum flip + add status/invariant cross-checks)
- **Directive:** The embedded prompt asserts "`pipeline_hardening_verdict` enum is consistently the FULL `pass | blocked | advisory | not_applicable` everywhere (GF-5)." **Change to:** verify the enum is consistently `pass | blocked | not_applicable` everywhere (§6.2 ≡ §8, C1/C3) and that `advisory` appears NOWHERE. ADD cross-checks: the per-gate `status` field (`PASS|FAIL|NA|NOT_PROVEN`) appears in SKILL.md contract, hub ref, report section, and remediation-handoff with consistent field names (`*_status` alongside each `*_card_path`); the `gate_na_rationale` field is present and named consistently.

### Step 4.6 — rf-qa-qualitative content lens: spec-fidelity

- **Item ID:** Step 4.6
- **Change type:** EDIT (add new spec content to the fidelity surface)
- **Directive:** The prompt lists the §6.2 8-field table as a fidelity target. Update for the refactored §6.2, which is now LARGER: it must verify the per-gate `status` enum rows (`PASS|FAIL|NA|NOT_PROVEN`, spec §6.2 L113-120), the `gate_na_rationale` map (L121), the status/path rule M7 (L125), the `known_escapes_caught` pattern `^E\d+$`/`^E\d+\+$` (L123, CS-m1), and the three-token verdict enum (L112). Add the §8 report block to the byte-faithful set with the firing-triggers line, four-token gate status, rationale clause, off-path→verdict line, and three-token closure verdict (spec §8 L350-368). Add acceptance-criteria 11-15 as fidelity anchors.

### Step 4.7 — rf-qa-qualitative content lens: completeness-vs-spec-§7

- **Item ID:** Step 4.7
- **Change type:** EDIT (add the new §6.1/§6.2/§7 mandatory-content to the completeness checklist)
- **Directive:** The prompt currently checks §6.1 trigger list + skip rule and §7 H0-H5 presence. Refactored §6.1 is now a NINE-trigger table (T1-T9) with a `Mandatory gate(s) it pins` column and a trigger→gate map (CS-1/M1, spec §6.1 L86-98). Update the prompt to verify: (a) all 9 triggers T1-T9 present with their pinned-gate mapping; (b) the mandatory-gate-set rule + the non-overridable trigger-overrides-skip rule (§6.1 L100-103, CS-6/M6); (c) H2's consumer-discovery manifest requirement (§7 L211-214, M11) and "absent ⇒ NOT_PROVEN"; (d) H3's E3-style sibling-heading negative fixture as an explicit completion criterion (§7 L254-256, M10) and the fixpoint-after-discovery rule (§7 L258-260, M9); (e) H4's no-op-`NA` vs changes-with-empty-input-`FAIL` branches (§7 L298-307, M5); (f) H5's mandatory-status invariant (§7 L319, M2). These are NEW spec elements the original prompt does not name.

### Step 4.9 — rf-qa-qualitative content lens: blocking-rule-accuracy

- **Item ID:** Step 4.9
- **Change type:** EDIT (re-point to the C2 verdict invariant + NOT_PROVEN status)
- **Directive:** The prompt verifies the hub ref's `NOT PROVEN` rule and the calibration-style gate. Update to: (a) verify `NOT_PROVEN` is treated as a first-class gate STATUS (not prose) that forces `verdict=blocked` (spec §8 L370, C2); (b) verify the C2 verdict invariant is faithfully encoded (verdict = total function of statuses; all-null run = `blocked`, not `pass`; spec §6.2 L129-135); (c) verify the off-path→verdict consequence (`required ∧ ¬performed/¬waived ⇒ blocked`, M2); (d) verify the Wave-6/remediation precondition uses `{pass, not_applicable}` (NOT `{pass, advisory}`). Flag any surviving `advisory` token or any "NOT PROVEN" prose-only (non-status) treatment.

### Step 5.1 — M4 fidelity agent 1 (spec §4/§6/§8 + report/hub)

- **Item ID:** Step 5.1
- **Change type:** EDIT (enum flip + add new §6.2/§8 detail-preservation anchors)
- **Directive:** The prompt's detail-preservation clause says "full enum `pass|blocked|advisory|not_applicable` per GF-5." **Change to** `pass|blocked|not_applicable` (C1/C3; flag `advisory` as a phantom/regression if found). ADD to the fidelity surface: the per-gate `status` enum + `gate_na_rationale` (§6.2 M7/M3), the verdict invariant C2 (§6.2 L129-135), the §8 firing-triggers line + four-token gate status + rationale + off-path→verdict line (§8 L355-360). The §6.1 target should be the 9-trigger table + trigger→gate map (M1), not the old bullet list. Add acceptance 11-15 as explicit fidelity checks.

### Step 5.2 — M4 fidelity agent 2 (spec §7 H1/H2/H3/H4 cards + gate refs)

- **Item ID:** Step 5.2
- **Change type:** EDIT (add the new H2/H3/H4 mandatory sub-content; line numbers shifted)
- **Directive:** The byte-faithful card/ledger targets (H1 13-field card, H2 9-row ledger, H4 10-field card) remain valid in shape, but the refactored spec ADDED content the prompt must now verify reproduced: (a) H2's consumer-discovery manifest block + "absent ⇒ NOT_PROVEN" (§7 L211-214/L221, M11) and the H2 `NOT_PROVEN` row; (b) H3's "Completion criteria" E3-style sibling-heading negative fixture + the M9 fixpoint-after-discovery paragraph (§7 L254-260); (c) H4's M5 no-op-vs-empty branches (§7 L298-307). **Also (A10-M3):** the spec line numbers cited in this prompt (136-151, 171-180, 241-253) have SHIFTED in the refactored spec — H1 card now spans roughly L164-179, H2 ledger L199-209, H4 card L284-296. Re-anchor on TEXT (card field names / ledger header) per GF-1; correct or drop the absolute line numbers.

### Step 4.4 — markdownlint-compliance lens (CONFIRM no change)

- **Item ID:** Step 4.4
- **Change type:** NO CHANGE (confirm)
- **Directive:** Pure structural lint lens; unaffected by spec-content changes. Leave as-is.

### Phase 3 validation items (Steps 3.1-3.4) — CONFIRM no change

- **Item IDs:** Steps 3.1 (sync-dev), 3.2 (verify-sync), 3.3 (markdownlint), 3.4 (staging discipline)
- **Change type:** NO CHANGE (confirmed)
- **Directive:** The validation phase is purely mechanical (sync-dev / verify-sync `✅ All components in sync.` / markdownlint on the 9 src files / `.claude/` staging-discipline grep). None of these parse spec content or the verdict enum. **No change required** — confirmed as asked.

---

## D. A.10 STRUCTURAL FINDINGS FOLD-IN

### A10-C1 — POST-reflect not penultimate (CRITICAL)

- **Item ID:** `## Post-Completion Actions` (lines 360-370; the POST-reflect item is L366, Task Summary L368, Update-status L370)
- **Change type:** REORDER (split/move)
- **Directive:** Current order: verify-outputs (L360) → no-testing rationale (L362) → re-confirm M3/M4 (L364) → **POST-reflect SELF-RUN (L366)** → **Task Summary (L368)** → Update-status-to-Done (L370). Move the POST-reflect SELF-RUN item so it is IMMEDIATELY before Update-status-to-Done. New order: verify-outputs → no-testing rationale → re-confirm M3/M4 → **Task Summary** → **POST-reflect SELF-RUN** → Update-status-to-Done. (POST-reflect must be penultimate per task-builder checklist.)

### A10-I1 — Step 5.5 atomicity (IMPORTANT)

- **Item ID:** Step 5.5
- **Change type:** SPLIT (into 5.5a / 5.5b / 5.5c)
- **Directive:** Step 5.5 currently spawns 2 verification agents AND embeds the consolidate→re-fix→re-verify 3-cycle loop in one item. Split, mirroring Phase 4's 4.12/4.13/4.14:
  - **5.5a** — spawn the 2 fidelity verification agents (1 rf-qa + 1 rf-qa-qualitative), `fix_authorization: false`, write `qa-fidelity-verification-structural.md` + `qa-fidelity-verification-content.md`.
  - **5.5b** — consolidate the verification findings + spawn ONE serialized fidelity fix agent `fix_authorization: true` (only if either verification FAILED), re-run `make sync-dev`.
  - **5.5c** — loop-control: read both verification verdicts; IF both PASS record M4 gate PASS in `qa-m4-gate-verdict.md`; IF either FAIL repeat 5.3-5.5b up to MAX 3 cycles; on exhaust HALT + escalate to Open Questions / Task Log.
  - Each its own self-contained `- [ ]` item with the full embedded prompt.

### A10-I2 — Step 2.11 atomicity (IMPORTANT)

- **Item ID:** Step 2.11
- **Change type:** SPLIT (into 2.11a / 2.11b / 2.11c)
- **Directive:** Step 2.11 makes THREE distinct SKILL.md modifications in one item (TB-Add-5 violation). Split:
  - **2.11a** — add the "Pipeline-hardening completeness gate (hard precondition for closure)" block modeled on the Tier-2 calibration gate (MUST NOT set `pipeline_hardening_verdict=pass`/mark remediated unless required H1/H2/H3/H4 cards exist on disk and pass; on-disk verification step; force `blocked`/`status: partial` on any `NOT_PROVEN`/`FAIL`/`NA`-without-rationale).
  - **2.11b** — tighten the Wave-6 remediation precondition to additionally require `pipeline_hardening_verdict ∈ {pass, not_applicable}` (NOT `{pass, advisory}` — fold in the C3 enum change here).
  - **2.11c** — append the `## Will Not Do` bullet ("Mark a pipeline escape remediated when a required H-gate is missing, FAIL, or NA without rationale").
  - Each self-contained. NOTE the enum-flip (advisory→not_applicable) lands in 2.11b and must agree with Step 2.1/2.14.

### A10-M1 — Step 1.3 G1 acknowledgement missing OQ back-reference (MINOR)

- **Item ID:** Step 1.3
- **Change type:** EDIT (add back-reference)
- **Directive:** Add to Step 1.3's Context an explicit "(see Open Question 1 — G1 halt condition)" back-reference (TB-Add-3).

### A10-M2 — GF-5 verdict-enum divergence note (MINOR) — **OBSOLETE / FLAGGED**

- **Item IDs:** Step 2.12 (report-template) and Step 2.1 (hub ref) — the items A10-M2 originally targeted
- **Change type:** OBSOLETE (the finding's remedy is superseded; the underlying note must be DELETED, not added)
- **Directive + FLAG:** A10-M2 asked to ADD a note to the report-template item and the hub-ref item saying "Use the full §6.2 verdict enum incl. `not_applicable`; the spec §8 report block omits it — intentional GF-5 additive reconciliation, NOT a fidelity defect." **This is now obsolete.** The refactored spec RESOLVED the divergence in-spec: §8 L363 now carries `pass | blocked | not_applicable` and §8 L368 states the enum is "identical to §6.2." There is no longer a §8-vs-§6.2 mismatch to reconcile, and `advisory` is gone entirely (C1/C3). **Action:** do NOT add the A10-M2 reconciliation note. Instead, the §2.12 and §2.1 directives in Section A above REMOVE the GF-5/`advisory` instructions and replace them with the C1/C3 identity ("§8 ≡ §6.2, enum = `{pass, blocked, not_applicable}`, no advisory"). A10-M2 is closed-as-obsolete; its anti-false-flag intent is now served by the QA-lens enum flips in Section C (Steps 4.3/4.6/5.1).

### A10-M3 — exact-line-number citations contradict GF-1 anchor-on-TEXT (MINOR)

- **Item IDs:** All Phase-2 edit items citing absolute line numbers as PRIMARY anchor — esp. Step 2.1 (cited H5 270-280/282-288/290-294), Step 2.2 (130-163, 136-151), Step 2.3 (165-194, 171-180), Step 2.4 (196-231), Step 2.5 (233-264, 241-253), Step 2.12 (300-312), Step 2.13 (314); and the Phase-5 fidelity prompts Step 5.1/5.2 (136-151/171-180/241-253)
- **Change type:** EDIT (make TEXT the primary anchor; line numbers advisory)
- **Directive:** For each item citing absolute line numbers as the primary anchor, add "(anchor on exact TEXT per GF-1; line numbers approximate)" and name the verbatim text anchor (heading/card-field/row text) it edits against. **Additional caveat introduced by the REFACTOR:** the spec was rewritten and grew (it is now ~444 lines vs the ~314 the original task assumed), so EVERY absolute line number in the tasklist is now stale, not just off-by-one. Do not recompute each number; just demote all of them to advisory and rely on TEXT anchors. Correct the Step 2.1 H5 numbers to the refactored spec's H5 block (roughly L321-344) or drop them. This caveat is co-owned with the SKILL/refs fan-out for Steps 2.2-2.5.

---

## ACCEPTANCE-CRITERIA IMPACT (spec §10, items 11-15 are NEW)

The refactored spec added acceptance criteria 11-15 (verdict-enum identity; vacuous-pass closed; trigger→gate map; per-gate status/rationale/NOT_PROVEN; H2-manifest/H3-fixture/H4-no-op). The tasklist's **Key Objectives** and **Open Questions** reference the OLD acceptance set and the OLD GF-5 reconciliation:

- **Open Question 2 (tasklist L151):** states refs/report use "the FULL §6.2 enum `pass | blocked | advisory | not_applicable`" and frames the §8-vs-§6.2 `not_applicable` omission as "additive reconciliation." **EDIT:** rewrite OQ2 to reflect C1/C3 — the enum is now `{pass, blocked, not_applicable}` everywhere, `advisory` removed, §8 ≡ §6.2 (no divergence). This OQ is the textual root of the obsolete GF-5 framing and must be corrected or the QA lenses inherit the stale assumption.
- **No new top-level checklist item is required** for acceptance 11-15: they are verified through the updated QA lenses (Steps 4.6/4.7/4.9) and M4 fidelity agents (Steps 5.1/5.2) per Section C. Acceptance 10 (sync-dev/verify-sync/markdownlint) is unchanged and already covered by Phase 3.

---

## MAPPING TABLE 1 — SPEC-CHANGE → TASKLIST ITEM

| Spec change (CS / spec ref) | Affected item(s) | Change type |
|---|---|---|
| CS-3 / C1+C3 — drop `advisory`, enum `{pass,blocked,not_applicable}` (§6.2 L112, §8 L363/L368, acc 11) | 2.12, 2.13, 2.1, 2.14, 2.8*, 2.11b, 4.3, 4.6, 4.9, 5.1; OQ2 | EDIT |
| CS-7 / M7 — per-gate `status` token distinct from path (§6.2 L113-121, §8 L356-359) | 2.12, 2.1, 2.8*, 4.3, 4.6, 5.1, 5.2 | EDIT |
| CS-3b / M3 — per-gate `rationale`; bare `NA`→`NOT_PROVEN` (§8 L356-359/L366) | 2.12, 2.13, 4.6, 4.9, 5.1 | EDIT |
| CS-2 / C2 (⊇M8) — verdict invariant; vacuous-pass=blocked; NOT_PROVEN⇒blocked (§6.2 L129-135, §8 L370, acc 12/14) | 2.13, 2.1, 2.11a, 4.9, 5.1 | EDIT |
| CS-2b / M2 (⊇m2) — H5 mandatory; off-path→verdict line (§8 L360, §7 L319) | 2.12, 4.7, 4.9, 5.1 | EDIT |
| CS-1 / M1 — 9-trigger table + trigger→gate map (§6.1 L86-98, acc 13) | 4.7, 5.1 | EDIT |
| CS-6 / M6 — trigger-overrides-skip, non-overridable (§6.1 L100-103) | 4.7 | EDIT |
| CS-11 / M11 — H2 consumer-discovery manifest; absent⇒NOT_PROVEN (§7 L211-214/L221) | 4.7, 5.2 | EDIT |
| CS-10 / M10 — H3 E3-style sibling-heading negative fixture completion criterion (§7 L254-256) | 4.7, 5.2 | EDIT |
| CS-9 / M9 — H3 fixpoint-after-discovery re-enumerate/disposition (§7 L258-260) | 4.7, 5.2 | EDIT |
| CS-5 / M5 — H4 no-op-`NA` vs changes-empty-`FAIL` (§7 L298-307) | 4.7, 5.2 | EDIT |
| CS-m1 — `known_escapes_caught` pattern `^E\d+$`/`E\d+\+` (§6.2 L123) | 2.12, 4.6, 5.1 | EDIT |
| §5.2 failure-state backed by verdict invariant (unchanged in principle) | 2.14 (verdict-invariant ref + enum), 2.11a/2.11b | EDIT |
| Validation phase (sync-dev/verify-sync/markdownlint) | 3.1, 3.2, 3.3, 3.4, 4.4 | NO CHANGE |

\* Step 2.8 (SKILL.md output-contract) is owned by the SKILL/refs fan-out; flagged here because its enum/status rows feed the QA lenses.

## MAPPING TABLE 2 — A.10 FINDING → TASKLIST ITEM

| A.10 finding | Severity | Affected item(s) | Change type | Note |
|---|---|---|---|---|
| A10-C1 — POST-reflect not penultimate | CRITICAL | Post-Completion Actions (L360-370) | REORDER | Move POST-reflect (L366) to immediately before Update-status (L370); Task Summary moves before POST-reflect |
| A10-I1 — Step 5.5 atomicity | IMPORTANT | Step 5.5 | SPLIT → 5.5a/5.5b/5.5c | Mirror Phase-4 4.12/4.13/4.14 |
| A10-I2 — Step 2.11 atomicity | IMPORTANT | Step 2.11 | SPLIT → 2.11a/2.11b/2.11c | Fold enum-flip (advisory→not_applicable) into 2.11b |
| A10-M1 — Step 1.3 missing OQ back-ref | MINOR | Step 1.3 | EDIT | Add "(see Open Question 1 — G1 halt condition)" |
| A10-M2 — GF-5 divergence note | MINOR | Step 2.12, Step 2.1 | OBSOLETE | Spec resolved divergence in-spec; DO NOT add the note; DELETE GF-5/advisory instructions instead (see Section A) |
| A10-M3 — line-number citations vs GF-1 | MINOR | All Phase-2 line-citing items (2.1-2.5, 2.12, 2.13) + 5.1/5.2 | EDIT | Demote line numbers to advisory; spec REWRITE means all numbers stale (not just off-by-one); TEXT anchors primary |
