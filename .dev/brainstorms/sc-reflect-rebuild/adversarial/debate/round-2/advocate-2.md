# Round 2 — Advocate for Variant 2 (Compressed Parallel)

## Responses to R1 Criticisms Against V2

### R-1. Re: "Drop everything that fits neither Grounded nor `[INFERRED]` is too strict" (R1 advocate-1, lines 117-121)

The critique misreads the binary. V2 §11.1 does not drop *hedged observations*; it drops *findings the reviewer could not tag either way*. The path for "this looks anomalous but I can't cite a contrary example" is **`[INFERRED]`**, not drop. The `[INFERRED]` tag exists precisely to host hedged observations without smuggling them in as Grounded prose (V2 §11.1: "a claim the reviewer reached without direct citation"). A reviewer who cannot decide *whether the claim is grounded or inferred* is making a meta-failure — not a hedge — and the drop rule is the right response to meta-failure.

The R1 advocate-1 critique also concedes the underlying mechanism in its own §10: it asks the merge to "adopt the tag and the per-report counter, without V2's 'drop unclassifiable' rule." The drop rule is what makes the tag have teeth — without it, the tag becomes optional decoration that reviewers ignore under deadline pressure. This is the structural mechanism, not the tag.

**Position: HOLD the drop rule, but clarify in §11.1 that the binary is Grounded-or-`[INFERRED]`, with drop reserved for the meta-failure case where neither tag applies. This is already V2's intent; the clarification is editorial.**

### R-2. Re: "Hallucination guardrails section is design rationale that belongs in SPEC.md not SKILL.md" (R1 advocate-3, lines 67-73)

This critique is the load-bearing R1 attack on V2's structure, and it is wrong on three counts:

1. **Behavior, not rationale.** V2 §11.1 names a tagging contract reviewers must apply. V2 §11.2 names a status routing rule (`zero_drop_flag: true` marker). V2 §11.5 names a re-Read tool-call cadence. V2 §11.6 names a numeric threshold (`>50% inferred for >20 citations → WARN`). These are *execution instructions*, not design justifications. R1 advocate-3 conflates the *explanation* prose at §11.3-§11.4 (the calibration and ensemble rationale) with the *contract* prose at §11.1, §11.2, §11.5, §11.6. The fix is to trim §11.3-§11.4 to back-references — not to delete the whole section.

2. **SKILL.md is what the LLM reads at activation.** R1 advocate-3 argues "every line in SKILL.md costs session-context tokens." This is true. The cost is bounded: per V2 §16 "Refs loaded by the wave that needs them; never pre-loaded. Session-start footprint: SKILL.md only (~50 tokens via Claude Code skill loader)." The full body is loaded *on activation*, not at session start. The ~70 lines of §11 are loaded once when reflection runs, not once per session. The trade-off is "70 lines once at activation" vs "guardrails distributed across §5/§6/§7/§17 where a future PR can silently weaken one without noticing." The collocation is the structural insurance.

3. **SPEC.md is not LLM-readable at runtime.** A guardrail in SPEC.md does not influence Claude's behavior — only SKILL.md does. Moving §11 to SPEC.md transforms enforced contracts into aspirational documentation.

**Position: HOLD §11 in SKILL.md, but compress §11.3-§11.4 to one-line back-references to refs/reflection-rubric.md. Net savings: ~15 lines. This addresses R1 advocate-3's length critique without losing the contract.**

### R-3. Re: "4-class deviation taxonomy creates false certainty (no `unknown` escape)" (R1 advocate-4, lines 243-251)

R1 advocate-4 argues `unknown` is "safer for cases where evidence is insufficient or the source/work relationship does not cleanly fit the four labels." This conflates two distinct failure modes:

- **Insufficient evidence**: the reviewer cannot determine *whether* a hunk matches a category. V2's correct path is a **Grounding Gap** in the report (V2 §11.2: "the report's 'Grounding Gaps' section enumerates dropped citations and the original claim text"), with `status: partial`. The hunk is surfaced explicitly, not absorbed into a fifth category that downstream automation cannot route on.

- **Multi-signal ambiguity**: signals for two or more categories match. V2 §10.5's precedence rule (Regression > Drift > Necessary > Authorized) resolves this deterministically. R1 advocate-3 §C1 *concedes* this rule is "genuinely better" than V3's default-to-Drift. R1 advocate-5 §S2 concedes the precedence is "genuinely novel and should be adopted regardless of which variant wins the merge."

R1 advocate-4's `unknown` example ("missing task logs, ambiguous source contracts, external approval not present in artifacts") is exactly the *insufficient-evidence* case, which V2 handles via Grounding Gaps + `status: partial` — not via a fifth class. Adding `unknown` lets reviewers route ambiguous-but-classifiable cases to the escape hatch under deadline pressure, which is precisely what the precedence rule exists to prevent. R1 advocate-3 §S6 + §X-009 also reject `unknown`: "less actionable... `unknown` produces a report that says 'I found something but I don't know what it is.'"

**Position: HOLD 4 categories + precedence rule. Add a clarification in §10 that insufficient-evidence cases route to Grounding Gaps + `status: partial`, not to a hypothetical 5th class. This is editorial.**

### R-4. Re: "Inferred-claim audit is a soft signal that allows >50% inference reports to ship as `success`" (R1 advocate-5, lines 113-115)

The critique is partially correct: V2 §11.6 is a soft WARN, not a hard gate. But the framing — that V5/V3 have "harder gates" — confuses different mechanisms.

V5's harder gate (per R1 advocate-5: "evidence-validator drops unfounded items") is the same gate V2 has at §11.2 ("`≥1 dropped` → `status: partial`"). V3's harder gate ("inline validation marks `status: partial` on any drop") is *less* strict than V2's because V3 has no `[INFERRED]` tagging at all — V3 drops ungrounded claims silently without surfacing the inference ratio. V2's `citations_inferred` counter + the §11.6 WARN is the only mechanism across all five variants that catches the case where the report is *internally clean by every drop-based gate but is mostly speculation*.

The right repair is not to convert §11.6 to a hard gate (which would force reflection to drop legitimately inferred-but-valuable observations whenever a report crosses the threshold). The right repair is to **add a status-routing rule**: if `citations_inferred > citations_total / 2` AND `citations_total > 20`, force `status: partial` (not just WARN). This preserves the inferred surface (the observations still ship in the report) but signals to downstream automation that the report should not be auto-consumed.

**Position: STRENGTHEN §11.6 — convert the soft WARN to a `status: partial` forcing rule on the same threshold. This is an additive change that addresses R1 advocate-5's critique without weakening the inferred tag.**

---

## Updated Assessment

The R1 critiques against V2 cluster into three families:

1. **Length critique** (R1 advocate-3): "§11 is rationale, not protocol; move to SPEC.md." — **Partially valid for §11.3-§11.4 (calibration+ensemble explanation); invalid for §11.1, §11.2, §11.5, §11.6 (execution contracts).** Mitigation: compress §11.3-§11.4 to back-references (~15 lines saved).

2. **Strictness critique** (R1 advocate-1, advocate-4): "Drop rule and 4-class taxonomy are too rigid; need escape valves." — **Invalid.** Both critiques mistake meta-failure (drop) and insufficient-evidence (Grounding Gap) cases for the cases the structural rules are designed for. V2's mechanism already has the right escape: `[INFERRED]` for hedged observations; Grounding Gap + `status: partial` for insufficient evidence. Adding `unknown` or relaxing drop creates the exact rubber-stamp failure mode the protocol exists to prevent.

3. **Soft-signal critique** (R1 advocate-5): "Inferred audit allows >50% inference reports to ship as `success`." — **Valid.** Convert the §11.6 WARN to a `status: partial` forcing rule (additive change, no surface lost).

Net assessment: V2's structural mechanisms survive R1 rebuttal. The required edits are one additive strengthening (R-4) and one compression (R-2). The R1 contributions worth absorbing into V2 — V1's `spec_is_wrong` asymmetric flag, V1's retroactive-escalation rule, V4's Testability Map, V5's env-var Wave 0 check, V5's Ops Integration (to ref, not inline), V3's Kill List — are all additive to V2's frame.

---

## New Evidence (R1 cross-references confirming V2 mechanisms)

- **R1 advocate-1 §10 concedes**: "V1 implicitly treats every claim as Grounded (via evidence-validator re-Read), which means findings that *should* be tagged as inferred are either smuggled in as if grounded or dropped silently." — This is exactly the smuggling failure mode V2 §11.1 prevents. The base-V1 advocate concedes V1 lacks the structural defense.

- **R1 advocate-3 §C1 + §C3 concede**: V3 lacks the precedence rule AND the hallucination guardrails. Combined with the §S2 concession that the binary tag is "a low-cost, high-value structural guard that V3 should adopt," the V3 advocate's own merge recommendation imports V2's §11.1 + §11.2 + §10.5.

- **R1 advocate-4 §126 concedes**: "Import V2's deviation precedence rule into V4's taxonomy because `unknown` solves insufficient evidence but does not solve multi-signal precedence when evidence is sufficient." — V4's own advocate admits `unknown` does not solve the precedence problem. The precedence rule is independently load-bearing.

- **R1 advocate-5 §S2 concedes**: V5 lacks the precedence rule, lacks the dedicated guardrails section, and the V5 advocate explicitly endorses adopting V2's §10.5 + §11.

Four of five R1 transcripts converge on importing V2's §10.5 + §11.1 + §11.2. This is consensus, not advocacy — V2's hallucination contract is the load-bearing structural contribution that survives independent review.

---

## Final Concessions

1. **R1 advocate-1's `spec_is_wrong` asymmetric flag (advocate-1 §C2 + advocate-2 §C2) is genuinely missing from V2.** V2 has `cannot_validate_without_user_input`, `regression_present`, `unauthorized_deviation_present` but not the "code right, spec wrong" routing flag. Concede and absorb into V2 §9.1.

2. **R1 advocate-1's retroactive-escalation rule (V1 Wave 3 step 4) addresses a real V2 gap.** V2's rubric is purely forward; V1's "if calibrated confidence < 0.85 after evidence pass → upgrade tier_planned to 2" catches scope-safe-on-paper cases that turn out fragile. Concede and absorb into V2 §5.

3. **R1 advocate-4's Testability Map (V4 §16) is additive and strengthens every V2 contract.** V2 has no per-decision assertion mapping. Concede and absorb as V2 §17.

4. **R1 advocate-5's env-var Wave 0 check (V5 §4 Wave 0 step 6) closes a real V2 gap.** V2 silently assumes `ANTHROPIC_DEFAULT_*` aliases resolve. Concede.

5. **R1 advocate-3's Kill List discipline (V3 §13) is additive.** V2 §7.2 partially does this for the rejected agents but does not enumerate other excluded features. Concede and expand.

6. **R1 advocate-5's Ops Integration content** belongs in a ref (e.g., `refs/ops-integration.md`), not in SKILL.md body — the protocol behavior is unchanged, but operator workflow becomes discoverable. Concede with ref-extraction.

---

## Additional Cross-R1 Pattern Analysis

### R1 advocate-1's V2-specific critique cluster (lines 117-128)

Advocate-1 levels two critiques specifically at V2: (a) the binary is too strict, (b) the 0.90 T1 floor is too low. These are in tension. The binary is "too strict" only if reviewers face cases that *should* ship as inferred but get dropped; the 0.90 floor is "too low" only if reviewers face cases that *should* escalate but don't. V2's mechanism aligns these: the `[INFERRED]` tag is for hedged-but-shippable observations; the 0.90 floor plus structural signals (`S_scope`, `S_domains`, `S_dev_density`) ensure cases with hedged claims also have the structural signals that force escalation. R1 advocate-1's critique cluster collapses into one position — "V2 is too strict somewhere and too loose somewhere else" — without identifying a case where both fail simultaneously.

### R1 advocate-3's "design rationale vs execution" critique applied to other variants

If R1 advocate-3's critique against V2 §11 ("design rationale belongs in SPEC.md, not SKILL.md") is consistently applied, it falls equally hard on V4's §16 Testability Map (which R1 advocate-3 itself §S4 endorses adopting) and V3's own §13 Kill List (which contains paragraphs of *rationale* for excluded features). The inconsistency suggests the real concern is length, not rationale-vs-execution. V2's response (compress §11.3-§11.4) addresses the length concern without sacrificing the contract.

### R1 advocate-4's `unknown` escape hatch in light of advocate-4's own merge recommendations

R1 advocate-4 §126 writes: "Import V2's deviation precedence rule into V4's taxonomy because `unknown` solves insufficient evidence but does not solve multi-signal precedence when evidence is sufficient." This concession is structurally devastating to the `unknown` defense — advocate-4 admits the 5th class does not do the work the precedence rule does. The remaining argument for `unknown` is "safety valve for insufficient evidence," which V2's Grounding Gaps + `status: partial` already handles. The result: `unknown` is a redundant fifth class whose job is already done by two existing V2 mechanisms.

### Convergence pattern across R1

Counting concessions across the five R1 transcripts:

- 4/5 advocates endorse V2's classification precedence rule (§10.5) — advocate-1 §10, advocate-3 §S2 + §X-010, advocate-4 §126, advocate-5 §S2.
- 4/5 advocates endorse V2's `[INFERRED]` tag — advocate-1 §10, advocate-3 §S2 + §C3, advocate-4 §159 implicitly, advocate-5 §C4.
- 3/5 advocates endorse V2's zero-drop-as-flag rule — advocate-1 §S2 (concession), advocate-3 §S2, advocate-4 §126.
- 5/5 advocates implicitly accept V2's 4-class taxonomy as the base (V4 adds `unknown` as a 5th but does not remove the 4).

V2's three load-bearing mechanisms (`[INFERRED]` binary, zero-drop flag, precedence rule) command majority or supermajority endorsement across the field. The minority positions (drop binary too strict, `unknown` safety valve, soft-not-hard inferred audit) are addressable via the additive repairs proposed in R-1, R-3, R-4 above.

---

## Updated Per-Point Positions

### X-001 (T1 coverage floor)

**V2 says ≥0.90.** R1 advocate-1 argues for 0.95; R1 advocate-3 argues for 0.85; R1 advocate-4 argues for 1.00. **HOLD at 0.90.** The 0.90 floor matches CLAUDE.md global rule 3 (≥90% confidence to proceed) — alignment between the global confidence rule and the tier rubric is itself a quality signal. R1 advocate-3's §X-001 *concedes* "0.90 is the better floor" for the default path. R1 advocate-5's §X-001 independently endorses 0.90. Three of five variants converge here; the outliers (V1 at 0.95, V3 at 0.85, V4 at 1.00) are each opposed by their own concessions.

### X-003 (convergence PASS threshold)

**V2 says 0.75.** R1 advocate-1 endorses 0.75; R1 advocate-4 concedes 0.75; R1 advocate-3 §X-003 concedes "≥0.75 = PASS." Only R1 advocate-5 holds 0.65. **HOLD at 0.75** — sc-adversarial's documented default, and the caller (sc:reflect) should not silently override the called skill's threshold. V5's "classification merge tolerates lower convergence" argument has merit but should be argued in sc-adversarial's docs, not overridden at the caller.

### X-005 (think_about_* status)

**V2 says CURRENT, scripted nudges, NOT load-bearing (V2 §6.4).** R1 advocate-1 endorses V1's identical position. R1 advocate-3 advocates elimination; R1 advocate-4 advocates mandatory checkpoints + frontmatter; R1 advocate-5 concedes V1/V3 elimination is cleaner. **HOLD V2's middle position.** The 200-token nudge has measurable audit value (R1 advocate-5 §X-005 admits this) without making the protocol depend on a contested tool surface (R1 advocate-3's elimination loses the value; R1 advocate-4's frontmatter declaration over-commits). V2 captures the value, never gates on it.

### X-009 (4-cat deviation taxonomy completeness)

**V2 holds 4 classes + precedence.** R1 advocate-3 endorses 4 classes + precedence. R1 advocate-5 endorses 4 classes + precedence. Only R1 advocate-4 advocates `unknown`. **HOLD 4 classes + §10.5 precedence rule + add clarification routing insufficient-evidence cases to Grounding Gaps.** Four of five variants converge here; the `unknown` outlier is R1 advocate-4's stance and is structurally weaker (see R-3 above).

### A-001 (user reads 400-700 line SKILL.md)

**QUALIFY.** V2 at 650 lines fits the band. Reducing to ~620 by R-2's §11.3-§11.4 compression makes V2 the second-shortest after V3.

### A-002 (env-var aliases remain set)

**ACCEPT as a real V2 gap.** Absorb V5's Wave 0 step 6.

### A-003 (`.dev/reflect/` parent dir)

**ACCEPT.** Consensus across all variants.

### A-004 (60/40 train/test split)

**QUALIFY.** Defensible for small-N; should be made explicit in V2 §12.

### A-005 (single-repo/single-project scope)

**ACCEPT** as v1 scope boundary.

---

## Closing Statement

V2's load-bearing contribution — the hallucination contract — survives R1 rebuttal on its three structural defenses (Grounded-or-`[INFERRED]` binary, zero-drop-as-flag, 4-class taxonomy with precedence rule). Four of five R1 advocates concede at least one of these mechanisms is "genuinely novel" or "should be adopted regardless of which variant wins the merge" (R1 advocate-3 §S2, R1 advocate-5 §S2 + §S2, R1 advocate-1 §10, R1 advocate-4 §126).

The valid R1 critiques against V2 — `spec_is_wrong` flag missing, retroactive-escalation missing, env-var check missing, Testability Map missing, Ops content missing — are all *additive* gaps that the merge can absorb without compromising V2's structural frame. The invalid critiques — "drop rule too strict," "4-class taxonomy needs `unknown`," "guardrails belong in SPEC.md" — each rest on misreadings of which V2 mechanism handles which failure mode.

The merge should adopt V2 as the base for §10 (deviation taxonomy with precedence), §11 (hallucination guardrails, compressed §11.3-§11.4 + strengthened §11.6), and §9 (return contract with `spec_is_wrong` added). The merge should absorb V1's retroactive-escalation rule into V2 §5, V4's Testability Map as V2 §17, V5's env-var check into V2 Wave 0, V5's Ops content into `refs/ops-integration.md`, and V3's Kill List discipline into V2 §7.2.

The structural mechanisms that make reflection *not confirm its own conclusions* are V2's contribution. Every other variant either lacks them, distributes them, or weakens them. The merge that omits §11 ships a reflection skill with confirmation bias by design.
