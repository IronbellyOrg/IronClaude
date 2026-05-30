# Refactoring Plan — V1 (base) + integrations from V2, V3

## Base: V1 (Agent A)

V1's structure preserved:
1. Header with substrate + mechanism files
2. Theory 1 — arithmetic-mean dilution
3. Theory 2 — evidence-grounding source/runtime conflation
4. Theory 3 — stripped-context (REPLACED, see below)
5. Cross-theory implications (KEPT, EXTENDED)

## Integrations from V2

### V2-Strength-1: Channel-failure disclosure as methodology section
- **Source**: V2 §1 "Reflection invocation evidence" + §3 "Reflection-vs-direct-read divergence"
- **Target location**: New top-level § "## Methodology & Channel Disclosure" after header, before Theory 1.
- **Rationale (debate evidence)**: Debate scoring matrix row "Channel-failure disclosure: V2, 1.00 confidence — required for the merge's methodology section". The merged output is a 3-channel investigation; the merge MUST disclose what each channel actually delivered vs intended.
- **Integration approach**: Verbatim adaptation of V2 §1 and §3 with C-channel-degradation note (V3 §3 "Pipeline degradation surfaced") added.
- **Risk level**: Low — pure additive section.

### V2-Strength-2: Verdict-direction asymmetry as the canonical Theory 3
- **Source**: V2 §T3 "Verdict-direction asymmetry"
- **Target location**: REPLACE V1's Theory 3 (stripped-context). V2's T3 self-rates 0.78 vs V1's T3 at 0.65; V1 itself steelmans V2's T3 as "sharper than mine."
- **Rationale (debate evidence)**: V1 advocate concession: "B's 'verdict-direction asymmetry' T3 is sharper than mine." V3 advocate concession: "B's verdict-direction T3 is a better T3 than mine." Two of three variants explicitly cede this slot.
- **Integration approach**: Lift V2's T3 verbatim into Theory 3 slot. Move V1's stripped-context theory to "## Secondary mechanisms (defense-in-depth)" with reduced prominence.
- **Risk level**: Low — V1 explicitly concedes.

### V2-Strength-3: Sharper fix formulas
- **Source**: V2 systemic-fix one-liners (gated minimum; 6th rubric dimension; verdict-direction modifier).
- **Target location**: Replace V1's fix one-liners where V2's is more rubric-actionable.
- **Rationale (debate evidence)**: Debate matrix T1 winner = V2 ("most actionable fix: gated minimum"); T2 winner = V2 ("6th rubric dimension more concrete").
- **Integration approach**: Insert V2's fix formulas in the "Systemic fix" subsections; retain V1's formula as alternative where the alternative is meaningfully different.
- **Risk level**: Low.

## Integrations from V3

### V3-Strength-1: Eval-suite silent-green theory (NEW theory slot)
- **Source**: V3 §C2 "Calibrator eval suite has silent-green coverage of structurally-unverifiable predicates"
- **Target location**: NEW Theory 4 (Meta-defect: validation didn't probe the failure mode).
- **Rationale (debate evidence)**: Debate matrix "Eval-suite silent-green (T2-C): V3, 0.85 — only V3 surfaces this meta-defect; complements rather than competes with V1/V2's mechanism theories." A merge that drops this loses methodological depth.
- **Integration approach**: Adapt V3's §C2 into a new Theory 4 section with full mechanism / evidence / per-theory confidence / fix structure to match V1's template.
- **Risk level**: Low — additive, no conflict with existing theories.

### V3-Strength-2: Recursion-of-the-same-anti-pattern observation
- **Source**: V3 §3 "Meta-observation (why running troubleshoot ON the calibrator was load-bearing)"
- **Target location**: Cross-theory implications section (V1's existing § extended).
- **Rationale (debate evidence)**: Debate matrix "Recursion observation: V3, 0.95 — methodological multiplier." V1's cross-theory section is the natural home.
- **Integration approach**: Add new bullet to V1's cross-theory implications: "The calibration system fails the same way the code it was calibrating was failing — the pin-test absence at production-code scope (pr86's helper-not-uppercasing) is isomorphic to the eval-suite absence at calibrator scope (Theory 4). The recursion is itself a verification."
- **Risk level**: Low.

### V3-Strength-3: Wave landing summary (omitted — too pipeline-specific)
- **Source**: V3 §3 "Where the troubleshoot tiers landed"
- **Decision**: NOT integrated. This is pipeline-execution metadata that doesn't generalize to the merged thesis; lives only in `variant-3-original.md` for reference.

## Base weaknesses addressed

### V1-Weakness-1: T3 (stripped-context) self-rated 0.65 with `[partially uncited]` flag
- **Better variant**: V2's verdict-direction T3 (0.78).
- **Fix approach**: REPLACE per V2-Strength-2 above. V1's stripped-context theory moved to "Secondary mechanisms."

### V1-Weakness-2: No channel-failure disclosure
- **Better variant**: V2.
- **Fix approach**: Insert V2's §1+§3 as new methodology section per V2-Strength-1.

### V1-Weakness-3: No eval-suite-silent-green theory
- **Better variant**: V3.
- **Fix approach**: Add V3's §C2 as new Theory 4 per V3-Strength-1.

## Changes NOT being made (and why)

- **V1's "Cross-theory implications ¶5 (substrate-vs-H3 fidelity caveat)"**: KEPT. V2 doesn't have it, V3 doesn't have it; V1's reasoning about what dimensional pattern would produce H3 vs pr86 is structurally important and not redundant.
- **V2's "Theory B3 — Verdict-direction asymmetry"** (vs V1's stripped-context T3): REPLACING per above; V1's stripped-context theory preserved in "Secondary mechanisms" rather than discarded outright.
- **V3's "Pipeline degradation surfaced in Grounding Gaps"**: KEPT in V3-channel methodology section (cross-references V2's channel-failure disclosure).

## Review

Auto-approved per `--depth quick` (interactive not set).
